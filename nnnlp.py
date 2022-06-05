import json
import random
f= open('intents.json')
data= json.load(f)

bagofWords=[]
classNames=[]
for i in data['intents']:
    for j in i["patterns"]:
        j=j.lower()
        j.replace("'", "")
        j.replace(",", "")
        j.replace("!","")
        j.replace("?","")
        words= j.split()
        for word in words:
            if word not in bagofWords:
                bagofWords.append(word)



classes=dict()
responses=dict()
for i in data['intents']:
    sentences=[]
    className= i["tag"]
    classNames.append(className)
    for j in i["patterns"]:
        j=j.lower()
        j.replace("'", "")
        j.replace(",", "")
        j.replace("!","")
        j.replace("?","")
        array=[]
        for a in range(0,len(bagofWords)):
            array.append(0)
        words= j.split()
        for word in words:
            index=bagofWords.index(word)
            array[index]=array[index]+1
        sentences.append(array)
    classes[className]=sentences;
    responses[className]=i["responses"]
f.close()

def distance(row1, row2):
    sum=0
    for e_row1, e_row2 in zip(row1,row2):
        sum=sum+abs(e_row1-e_row2)
    return sum



def classify(sentence):
    sentence= sentence.lower()
    sentence= sentence.replace("'", "")
    sentence= sentence.replace(",", "")
    sentence= sentence.replace("!", "")
    sentence= sentence.replace("?", "")
    array=[]
    for i in range(0,len(bagofWords)):
        array.append(0)
    words= sentence.split()
    for word in words:
        if word in bagofWords:
            index=bagofWords.index(word)
            array[index]=array[index]+1
    classDistances=[]
    for class_name in classes:
        lowestDist=10000
        classPatterns= classes[class_name]
        for pattern in classPatterns:
            p_dist= distance(array,pattern)
            if p_dist<lowestDist:
                lowestDist=p_dist
        classDistances.append(lowestDist)

    print(classDistances)
    output_name=""
    nearest_distance=10000
    for class_name, classDist in zip(classNames, classDistances):
        if classDist<nearest_distance:
            nearest_distance=classDist
            output_name=class_name

    availableResponses=responses[output_name]
    res=availableResponses[random.randrange(0,len(availableResponses))]
    return output_name, res

    
if __name__=='__main__':
    print(bagofWords)
    print(classNames)
    print(classes)
    print(responses)
    print(classify("thanks"))


