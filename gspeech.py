# Imports the Google Cloud client library
from google.cloud import speech


# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
gcs_uri = "gs://uassistantin/test2.wav"
def transcribe(gcs_uri):
    ans=""
    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ur-PK",
    )

        # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        ans=result.alternatives[0].transcript
    return ans
if __name__=="__main__":
    print(transcribe(gcs_uri))
