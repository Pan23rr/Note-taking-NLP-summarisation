import nltk
import math
import re
from nltk.corpus import stopwords

def createVertices(sentences):
    vertices={}
    stpw=set(stopwords.words('english'))
    for sent in sentences:
        wordsSet=set()
        sent=re.sub('[^a-zA-Z]',' ',sent)
        words=nltk.word_tokenize(sent)
        for word in words:
            word=word.lower()
            if word in stpw:
                continue
            if word.isalnum() and word not in wordsSet:
                wordsSet.add(word)
        vertices[sent]=wordsSet
    
    return vertices


def similarity(vertices):
    edgeSet={}
    for sent1,words1 in vertices.items():
        for sent2,words2 in vertices.items():
            if sent1==sent2:
                continue
            edgeScore=len(words1.intersection(words2))
            edgeScore=edgeScore/(math.log(len(words1)+len(words2))) if (math.log(len(words1)+len(words2)))>0 else 0
            edgeSet[tuple(sorted([sent1,sent2]))]=edgeScore
    return edgeSet


def textrank(vertices,edgeSet,damp=0.85,threshold=1e-4,max_iterations=100):
    
    scores={sent:1.0 for sent in vertices.keys()}

    outScore={}

    for sent1 in vertices.keys():
        score=0.0
        for sent2 in vertices.keys():
            if sent1==sent2:
                continue
            score+=edgeSet.get(tuple(sorted([sent1,sent2])),0)
        outScore[sent1]=score

    for _ in range(max_iterations):
        newScores={}
        for sent1 in vertices.keys():
            score=0.0
            for sent2 in vertices.keys():
                weight=edgeSet.get(tuple(sorted([sent1,sent2])),0)
                if outScore.get(sent2,0)>0:
                    score+=(weight/outScore[sent2])*scores[sent2]
            newScores[sent1]=(1-damp) +(damp *score)

        if all(abs(newScores[sent1]-scores[sent1])<threshold for sent in vertices.keys()):
            break

        scores=newScores
    
    return scores


def summarise(sentences,scores, top_n=5):
    

    ranked_sentences = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    top_sentences = [sent for sent, score in ranked_sentences[:top_n]]

    sorted_summary = [sent for sent in sentences if sent in top_sentences]
    
    summary = '\n'.join(top_sentences)

    return summary


def mainSummary(paragraph):
    sentences=nltk.sent_tokenize(paragraph)


    vertices=createVertices(sentences)

    similarityMat=similarity(vertices)

    scores=textrank(vertices,similarityMat)

    return summarise(sentences,scores,5)


