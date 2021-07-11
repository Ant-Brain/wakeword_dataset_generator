import requests
import os
from os import environ
from os.path import isdir
from os import mkdir
import enum
import time
from random import choice
from baseClasses import genders , Countries, fileName


voices = {
        Countries.Australian : {
            genders.female : ["en-AU-NatashaNeural"],
            genders.male : ["en-AU-WilliamNeural"]
            },
        Countries.Indian : {
            genders.male :["en-IN-PrabhatNeural"],
            genders.female:["en-IN-NeerjaNeural"]
            },
        Countries.British : {
            genders.male: ["en-GB-RyanNeural"],
            genders.female : ["en-GB-MiaNeural","en-GB-LibbyNeural"]
            },
        Countries.Irish : {
            genders.male : ["en-IE-ConnorNeural"],
            genders.female : ["en-IE-EmilyNeural"]
            },
        Countries.South_Africa : {
            genders.male : ["en-ZA-LukeNeural"],
            genders.female : ["en-ZA-LeahNeural"]
            },
        Countries.American : {
            genders.male : ["en-US-GuyNeural"],
            genders.female : ["en-US-JennyNeural","en-US-AriaNeural"]
            },
        Countries.Canada : {
            genders.male : ["en-CA-LiamNeural"],
            genders.female : ["en-CA-ClaraNeural"]
            },
        #Countries.HongKong : { #To be kicked out , just clones of other voices
        #    genders.male : ["en-HK-SamNeural"],
        #    genders.female : ["en-HK-YanNeural"]
        #    },
        Countries.Philippines : {
            genders.male : ["en-PH-JamesNeural"],
            genders.female : ["en-PH-RosaNeural"]
            },
        #Countries.Singapore : { #To be kicked out , just clones of other voices
        #    genders.female : ["en-SG-LunaNeural"],
        #    genders.male : ["en-SG-WayneNeural"]
        #    }
    }

ssml_string ="""
<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name=\"%s\">%s</voice>
</speak>
"""

class TextToSpeech(object):
    def __init__(self):
        self.subscription_key = environ["API_KEY"]
        self.tts = None
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None
        self.get_token()

    '''
    The TTS endpoint requires an access token. This method exchanges your
    subscription key for an access token that is valid for ten minutes.
    '''
    def get_token(self):
        fetch_token_url = "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def synthesizeVoice(self,words:str,voice:str) -> bool :
        #time.sleep(1)
        #print(list(voices[country].keys()))
        #voice = choice(list(voices[country][gender]))
        i=2
        while i>=0 :
            body:str = ssml_string%(voice,words)

            base_url = 'https://eastus.tts.speech.microsoft.com/'
            path = 'cognitiveservices/v1'
            constructed_url = base_url + path
            headers = {
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/ssml+xml',
                'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
                'User-Agent': 'HotwordGenerators'
            }

            response = requests.post(constructed_url, headers=headers, data=body)
            '''
            If a success response is returned, then the binary audio is written
            to file in your working directory. It is prefaced by sample and
            includes the date.
            '''
            if response.status_code == 200:
                filePath = fileName%(words,voice,"AZURE")
                with open(filePath+".wav", 'wb') as audio:
                    audio.write(response.content)
                    print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
                return
            else:
                if(response.status_code==429): #401
                    print("+++++++++++++++++++++")
                    print("Hit the limit, starting delay of 15 sec")
                    print("+++++++++++++++++++++")
                    time.sleep(15)
                elif(response.status_code==401):
                    print("#-#-#-#-#-#-#-#-#-#-#-")
                    print("Unauthourized!!, starting delay of 200 sec")
                    print("#-#-#-#-#-#-#-#-#-#-#-")
                    self.get_token()
                    time.sleep(10)
                    i-=1
                else:
                    print("Some other error bitch")
                i-=1
                print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
                print("Reason: " + str(response.reason) + "\n")


TTS_Engine:TextToSpeech = TextToSpeech()
#TTS_Engine.synthesizeVoice("Hello world",Countries.Indian)

def getAudioSample(word:str,voice:str):
    if(not os.path.isdir(f"dataset/{word}")):
        os.mkdir(f"dataset/{word}")
    TTS_Engine.synthesizeVoice(word,voice)

"""
for country in voices.keys():
    synthesizeVoice("I am angelina jolie",str(country)+"_female.wav",country,genders.female)
    synthesizeVoice("I am John Walker",str(country)+"_male.wav",country,genders.male)
"""
if __name__=="__main__":
    getAudioSample("bread","en-PH-JamesNeural")