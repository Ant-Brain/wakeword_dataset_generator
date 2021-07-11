import os, sys, random, time
import enum
from random import choice
from baseClasses import genders, Countries, fileName


voices = {
    Countries.Australian : {
        genders.male:["Lee"],
        genders.female:["Karen"]
    },
    Countries.Indian : {
        genders.male:["Rishi"],
        genders.female:["Veena"]
    },
    Countries.Irish : {
        genders.female:["Moira"]
    },
    Countries.South_Africa : {
        genders.female:["Tessa"]
    },
    Countries.British : {
        genders.male:["Daniel","Oliver"],
        genders.female:["Kate","Serena"]   
    },
    Countries.American : {
        genders.male:["Alex","Tom","Vicki"],
        genders.female:["Agnes","Allison","Ava","Samantha","Susan"]
    }    
}

def uniqueAudioFileNameGenerator()->str:
    pass

def getAudioSample(word:str,voice:str):
    if(not os.path.isdir(f"dataset/{word}")):
        os.mkdir(f"dataset/{word}")
    #voice = choice(list(voices[country][gender]))
    #print(voice)
    filePath = fileName%(word,voice,"SIRI")
    #print(filePath)
    os.system("say -v "+voice+" "+word+" -o" +filePath+".aiff")
    os.system("lame -b "+ filePath+".aiff "+filePath+".wav")
    os.system("rm "+filePath+".aiff")


if __name__ == "__main__" :
    getAudioSample("malware","Daniel")