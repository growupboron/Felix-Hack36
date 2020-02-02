from time import sleep


import httplib, urllib, base64
import signal
import numpy as np
import sys
import json
from os import system


def exit_gracefully(signum,frame):
    signal.signal(signal.SIGINT, original_sigint)
    sys.exit(1)


    

ms_api_key = "3ce370692850429d98d3bfb773bc37c2"


headers = {
    
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': ms_api_key,
}

params = urllib.urlencode({
    
    'visualFeatures': 'Description',
})

def saveTextFile(text):
    try:
        print(text)
        text_file = open("scene.txt","w+")
        text_file.write(text)
        text_file.close()
    except Exception, e:
        print ("Exception occured \n")
        print (e)
        pass

def read_image():
    pathToFileInDisk = r'scene.png'
    with open(pathToFileInDisk, 'rb') as f:
        data = f.read()
    return data

def analyze_image(data):
    try:
        conn = httplib.HTTPSConnection('centralindia.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, data, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return data

def tag_from_data(input):
    if input is not None:
      
        result = json.loads(input)
        description = result['description']['captions'][0]['text']
        print(data)
        # img = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)

       
        awsstring = "I think it is "
        awsstring += description
        awsstring += ". And the keywords are  "
        num_keywords = 5
        for i in range(num_keywords):
            awsstring += result['description']['tags'][i]
            if i != num_keywords - 1:
                awsstring += ', '

        return awsstring


if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT,exit_gracefully)
    img = read_image()
    data = analyze_image(img)
    text = tag_from_data(data)
    saveTextFile(text)

