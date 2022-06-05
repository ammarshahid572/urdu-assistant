import os
import json
from flask import Flask, flash, request, redirect, url_for

from werkzeug.utils import secure_filename

from AISHA import Aisha

from gspeech import transcribe
from gtrans2 import translate_text

UPLOAD_FOLDER = 'files/'
ALLOWED_EXTENSIONS = {'wav'}

from google.cloud import storage

CLOUD_STORAGE_BUCKET="uassistantin"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '39fd2bb12a0cb11544e66997'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def root():
    return '''<!doctype html>
	<body>
	<a href="/forms"> Manual upload </a><br>
	<a href="/upload">upload endpoint</a>
	</body>'''

@app.route('/forms')
def form():
    form='''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=POST action="/upload" enctype=multipart/form-data>
          <label for="query">Query:</label><br>
          <input type="file" id="file" name="file"><br>
          <input type=submit value=Upload>
        </form>
        '''
    return form


@app.route('/upload', methods=['POST'])
def upload() -> str:
    """Process the uploaded file and upload it to Google Cloud Storage."""
    uploaded_file = request.files.get('file')
    x=dict()
    x["result"]="invalid"

    if not uploaded_file:
        x["message"]="No file uploaded"
        y=json.dumps(x)
        return y
    
    if uploaded_file and not allowed_file(uploaded_file.filename):
        x["message"]="Invalid file format only .wav supported"
        y=json.dumps(x)
        return y

    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(uploaded_file.filename)
    print()

    blob.upload_from_string(
        uploaded_file.read(),
        content_type=uploaded_file.content_type
    )

    # Make the blob public. This is not necessary if the
    # entire bucket is public.
    # See https://cloud.google.com/storage/docs/access-control/making-data-public.
    blob.make_public()

    gcs_uri="gs://"+CLOUD_STORAGE_BUCKET+"/"+str(uploaded_file.filename)
    stt=transcribe(gcs_uri)
    enStt=translate_text("en", stt)
    command , action=Aisha(enStt, stt)
    urdu_action=translate_text("ur", action)
    print(stt)
    
    x["result"]="valid"
    x["input_text"]=stt
    x["urdu"]= stt
    x["english"]=enStt
    x["en_action"]= action
    x["action"]=urdu_action
    x["command"]=command
    x["file"]=blob.public_url
    y=json.dumps(x)
    return y
if __name__ == '__main__':
   app.run(port=8080)


