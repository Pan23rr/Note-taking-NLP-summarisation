import math
import nltk 
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def generatefreqMatrix(sentences: list):
    freqMatrix={}
    stopWords=set(stopwords.words('english'))
    ps=PorterStemmer()
    for sent in sentences:
        words=nltk.word_tokenize(sent)
        freqTable={}
        for word in words:
            word=word.lower()
            word=ps.stem(word)
            if word in stopWords:
                continue
            if word in freqTable:
                freqTable[word]+=1
            else:
                freqTable[word]=1
        freqMatrix[sent]=freqTable
    return freqMatrix


def termfreqMatrix(freqMatrix):
    tfMatrix={}
    for sent,freqTable in freqMatrix.items():
        tfTable={}
        wordCount=sum(freqTable.values())

        for word,count in freqTable.items():
            tfTable[word]=count/wordCount
        
        tfMatrix[sent]=tfTable
    
    return tfMatrix

def documentsperWord(freqMatrix):
    wordsentFreq={}
    
    for sent,freqTable in freqMatrix.items():
        for word,count in freqTable.items():
            if word in wordsentFreq:
                wordsentFreq[word]+=1
            else:
                wordsentFreq[word]=1
    
    return wordsentFreq


def generateIDFMatrix(freqMatrix,wordsentFreq):
    totalSent=len(freqMatrix)

    idfMatrix={}

    for sent,freqTable in freqMatrix.items():
        idfTable={}

        for word in freqTable:
            idfTable[word]=math.log10((totalSent)/float(wordsentFreq[word]))
        
        idfMatrix[sent]=idfTable
    
    return idfMatrix


def tfIDFmatrix(tfMatrix:dict, IDFMatrix:dict):
    tfIDFMatrix={}
    for (sent1,freqTable1),(sent2,freqTable2) in zip(tfMatrix.items(),IDFMatrix.items()):
        tfIDFTable={}
        for (word1,freq1),(word2,freq2) in zip(freqTable1.items(),freqTable2.items()):
            tfIDFTable[word1]=freq1*freq2
        tfIDFMatrix[sent1]=tfIDFTable
    return tfIDFMatrix

def scoreSentence(tfIDFMatrix):
    sentenceVals={}

    for sent,tfIDFTable in tfIDFMatrix.items():
        sentenceScore=0
        totalWeight=len(tfIDFTable)
        
        for word,count in tfIDFTable.items():
            sentenceScore+=count
        sentenceVals[sent]=sentenceScore/totalWeight if totalWeight else 0
    
    return sentenceVals

def thresholdScore(sentenceVals):
    score=0
    for sent,vals in sentenceVals.items():
        score+=vals

    return score/len(sentenceVals) if sentenceVals else 0

def summary(sentenceVals,threshold):
    summ=''
    for sentence,vals in sentenceVals.items():
        if vals>=threshold:
            summ+=sentence +" "
    return summ.strip()

def mainSummary(paragraph):
    sentences=nltk.sent_tokenize(paragraph)

    freqMat=generatefreqMatrix(sentences)

    tfMat=termfreqMatrix(freqMat)

    wordFreq=documentsperWord(freqMat)

    idfMat=generateIDFMatrix(freqMat,wordFreq)

    tfidfMat=tfIDFmatrix(tfMat,idfMat)

    sentenceMat=scoreSentence(tfidfMat)

    thres=thresholdScore(sentenceMat)

    return summary(sentenceMat,thres)

