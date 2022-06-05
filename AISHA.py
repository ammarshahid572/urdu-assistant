from wolfram import wolf_answer

from nnnlp import classify
from youtubesearchpython import *
test= "weather right now"

numbers_en=['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine','ten', 'eleven', 'twelve']
numbers_ur=['aik', 'do', 'teen' , 'chaar', 'paanch', 'che','saat', 'aath' , 'no', 'das' , 'giara', ' bara' ]

def numberGoThrough(text, translated):
    out_number=0
    urduExist=False
    engExist=False
    numberExist=False
    for urduNum in  numbers_ur:
        if urduNum in text:
            urduExist=True
            break
    for engNum in  numbers_en:
        if engNum in translated:
            engExist=True
            break
    detectedNumber=0
    for number in  range(0,13):
        if str(number) in translated:
            detectedNumber=number
            numberExist=True
    ret= (urduExist and engExist) or numberExist
    if engExist:
        out_number= numbers_en.index(engNum)+1
    elif numberExist:
        out_number= detectedNumber
    return ret, out_number

def timeCalc(text, number):
    if "PM" in text or "pm" in text or "p.m" in text:
        if number<12:
            number=number+12
        elif number==12:
            number= number
    elif ("AM" in text or "a.m" in text) and number==12:
        number==0
    else:
        pass
    return number


def Aisha(text, urduText):
    text= text.lower()
    response=""
    action=""
    inputc = text
    inputc= inputc.lower()
    print(inputc)
    ret, number= numberGoThrough(text, inputc)
    
    if 'aisha' in text or 'aisha' in inputc or 'ayesha' in inputc:
        action="aisha"
        p_class,response=classify(inputc)
    elif "open" in inputc and "whatsapp" in inputc:
        action="open"
        response="openning whatsapp "
    elif 'who are you' in text or 'what is this ' in text or 'who is this' in text or "what's this" in text or "your name" in text or "creator" in text or "created you" in text or "built you" in text or "made you" in text:
        action="aisha"
        p_class,response=classify(inputc)
    elif 'batao' in text or 'tell' in inputc or 'kia' in text or 'what' in inputc:
        action="query"
        response=wolf_answer(inputc)
    elif ret:
        
        if 'alarm' in inputc:
            snumber=timeCalc(inputc, number)
            action="alarm"
            response= ("alarm for "+str(snumber))
        elif 'remind' in inputc:
            snumber=timeCalc(inputc, number)
            action="reminder"
            response= ("reminder for "+str(snumber))
    elif "picture" in text or "camera" in text or "picture" in inputc or "camera" in inputc:
        action="camera"
        response="Open Camera"
    elif "weather" in text:
        inputc=inputc+ " Karachi"
        action="query"
        response=wolf_answer(inputc)
    elif "time" in text:
        inputc= inputc+ "  in Karachi"
        action="query"
        response=wolf_answer(inputc)
    elif "open" in inputc or "kholo" in text :
        action="open"
        print("opening an app")
        
        if "youtube" in inputc:
            response="Openning Youtube"
        elif "facebook" in inputc:
            response="Openning Facebook"
        elif "stackoverflow" in inputc or "stack overflow" in inputc:
            response="Openning stackoverflow"
        
    elif "song" in text or "gaana" in text or "play" in text:
        urduText=urduText.replace("\u0633\u0648\u0646\u06af", "")
        urduText=urduText.replace(" \u067e\u0644\u06d2", "")
        text=text.replace("play", "")
        text=text.replace("song", "")
        text=text.replace("the", "")
        
        videosSearch = VideosSearch(text, limit = 1)
        videoID=videosSearch.result()['result'][0]["id"]
        action="song"
        response='https://www.youtube.com/watch?v='+videoID
    
    else :
        action="query"
        response=wolf_answer(inputc)
    

    return action,response

if __name__=='__main__':
    print(Aisha(test, test))

