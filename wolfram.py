import wolframalpha
#from speak import Speak
import os
def wolf_answer(query):
    #os.system('omxplayer -o local Searching.mp3')
    client = wolframalpha.Client('72HGV2-62YQP9W3X2')
    answer="Could not find the answer."
    res=client.query(query)
    for i,pod in enumerate(res.pods):
        if i==1:
            for sub in pod.subpods:
                answer=sub.plaintext
    return answer+". "
         
