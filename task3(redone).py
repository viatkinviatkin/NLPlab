import math
import os
import nltk
import re
import string
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def getTf(freq, text):
    return freq / len(text)

def getIdf(word, corpus):
    return math.log10(len(corpus)/sum([1.0 for i in corpus if word in i]))

def getTfidf(wordFreq, text, corpus):
    print(wordFreq[0], ': ', getTf(wordFreq[1], text) * getIdf(wordFreq[0], corpus))

def getFileList(path):
    for root, dirs, files in os.walk(path):
        filelist = []
        for file in files: 
            filelist.append(os.path.join(root,file))
        return filelist

def clearTokens(tokens):
    stopWords = stopwords.words('russian')
    stopWords.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на'])
    tokens = [i for i in tokens if (i not in stopWords and re.match('\w', i) and not re.match('котор*', i))]
    return tokens

def getTokens(text):
    tokens = nltk.word_tokenize(text)
    tokens = [i for i in tokens if (i not in string.punctuation)]
    tokens = clearTokens(tokens)
    return tokens

def createBigText(filelist, bigText):
    for name in filelist:
        input = open(name, 'r', encoding='utf-8').read()
        tokens = getTokens(input.lower())
        bigText += tokens

def createCorpus(filelist, corpus):
    for name in filelist:
        input = open(name, 'r', encoding='utf-8').read()
        tokens = nltk.word_tokenize(input.lower())
        tokens = [i for i in tokens if (i not in string.punctuation and re.match('\w', i))]
        corpus.append(list(tokens))

def normalizeTokens(tokens):
    normalTokens = []
    for var in tokens:
        normalToken = morph.parse(var)[0]
        normalTokens.append(normalToken.normal_form)
    return normalTokens

def normalizeCorpus(corpus):
    normCorpus = []
    for text in corpus:
        normCorpus.append(normalizeTokens(text))
    return normCorpus

def getKeywords(bigTextFreq, percent):
    key = []
    i = 0
    for keyw in bigTextFreq.most_common(round(len(bigTextFreq)*0.10)):
        if(keyw[1] > len(normalBigText) * percent):
            key.append(keyw)
        else:
            break
    return key

path = 'corpus'
fileList = getFileList(path)

bigText = []
corpus = []

createBigText(fileList, bigText)
createCorpus(fileList, corpus)

normalBigText = normalizeTokens(bigText)
normalCorpus = normalizeCorpus(corpus)

bigTextFreq = FreqDist(normalBigText)
keywordsFreq = getKeywords(bigTextFreq, 0.0075)
keywords = []
for wordFreq in keywordsFreq:
    keywords.append(wordFreq[0])

print(keywords)

for keyword in keywordsFreq:
    getTfidf(keyword, normalBigText, normalCorpus)



##В каждом доке отдельно
for text in corpus:
    print()
    tokens = clearTokens(text)
    normalTokens = normalizeTokens(tokens)
    tokensFreq = FreqDist(normalTokens)
    keywsFreq = getKeywords(tokensFreq, 0.0015)
    keyws = []
    for wordFreq in keywsFreq:
        keyws.append(wordFreq[0])

    print(keyws)

    for keyword in keywsFreq:
        getTfidf(keyword, normalTokens, normalCorpus)
