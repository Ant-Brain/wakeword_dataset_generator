import pprint
import eng_to_ipa as ipa
from time import sleep

class WordPronunciationPairs :
    def __init__(self,word:str):
        self.word = word;
        self.pronunciation = ipa.convert(word)
    def __repr__(self):
        return self

def cleanbaby():
    inpFile = open("./wordlist/babynames.txt",'r')

    lines = inpFile.read().split("\n") # splitting doc into lines
    names = [x.split(",")[1][1:-2] for x in lines if(x!="")] # splitting lines into names of format 123,"123",...
    longnames = [ x for x in names if(len(x)>5) ] # just handpicking names size > 5
    longnames = sorted(set(longnames)) # sorting and removing duplicates

    open("./wordlist/cleanedbabynames1.txt",'w').write("\n".join(longnames))# writing back to the doc

    return None

def cleanGoogle():
    inpFile = open("./wordlist/googleWords.txt",'r')

    lines = inpFile.read().split("\n") # splitting doc into lines
    #names = [x.split(",")[1][1:-2] for x in lines if(x!="")] # splitting lines into names of format 123,"123",...
    longnames = [ WordPronunciationPairs(x) for x in lines if(len(x)>5) ] # just handpicking names size > 5
    longnames = sorted(set(longnames),key=lambda x:x.pronunciation) # sorting and removing duplicates
    uniqueWords = []
    i = 0
    while i < (len(longnames)):
        #sleep(0.1)
        srcWord = longnames[i]
        uniqueWords.append(srcWord)
        pronunciation = ipa.convert
        minMatchCount = int(0.8*len(srcWord.pronunciation))
        print(i)
        for j in range(i+1,len(longnames)):
            if srcWord.pronunciation[:minMatchCount] != longnames[j].pronunciation[:minMatchCount] :
                #uniqueWords.append(longnames[j])
                i=j
                break
            else:
                i+=1
        if(i==len(longnames)-1):
            uniqueWords.append(longnames[i])
            i+=1
    

    open("./wordlist/cleanGoogleWords.txt",'w').write("\n".join([x.word for x in longnames]))# writing back to the doc
    open("./wordlist/cleanGoogleWords2.txt",'w').write("\n".join([x.word for x in uniqueWords]))# writing back to the doc

      
    return None

cleanGoogle()