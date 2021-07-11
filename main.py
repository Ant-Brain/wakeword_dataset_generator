from os import listdir
import os
from random import choice , sample
import random
#from siri import voices as siri_voices
#from azure_tts import voices as azure_voices
import siri
import azure_tts
from baseClasses import genders
from requests.exceptions import ConnectionError

siri_voices = siri.voices
azure_voices = azure_tts.voices

combinedVoices = dict()

def sendAlert(title:str,comment:str):
    alert_command = (f"osascript -e \'display alert \"{title}\" message \"{comment}\"\'")
    os.system(alert_command)

for country in siri_voices.keys() :
    for gender in siri_voices[country].keys():
        if(country not in combinedVoices.keys()):
            combinedVoices[country] = dict()
        if(gender not in combinedVoices[country].keys()):
            combinedVoices[country][gender] = []
        for voice in siri_voices[country][gender]:
            combinedVoices[country][gender].append(
                {
                    "name":voice,
                    "engine":"siri"
                }
            )

for country in azure_voices.keys() :
    for gender in azure_voices[country].keys():
        if(country not in combinedVoices.keys()):
            combinedVoices[country] = dict()
        if(gender not in combinedVoices[country].keys()):
            combinedVoices[country][gender] = []
        for voice in azure_voices[country][gender]:
            combinedVoices[country][gender].append(
                {
                    "name":voice,
                    "engine":"azure"
                }
            )


#pprint(combinedVoices)

words = open("./finalizedWordList.txt",'r').read().split("\n")
countries = combinedVoices.keys()
word_count = len(words)

START_FROM = len(listdir("dataset/"))#0
sendAlert("Starting datasysnthesis","Ensure stable internet connection")
try:
    for i, word in enumerate(words[START_FROM:]):
        print("Progress:",100*(i+START_FROM)/word_count)
        randomlyChoosenCountries:list = sample(countries,5)
        for country in randomlyChoosenCountries :
            gender = choice([genders.male,genders.female])
            voice = choice(combinedVoices[country][gender])
            if(voice["engine"]=="siri"):
                siri.getAudioSample(word,voice["name"])
            else: #if not siri then azure
                azure_tts.getAudioSample(word,voice["name"])
    sendAlert("Dataset Synthesis Completed","Dont run code again")
except ConnectionError :
    sendAlert("Siameses dataset synthesis terminated","Unable to communicate to server , please run again") 
