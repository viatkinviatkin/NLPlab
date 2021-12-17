#1 разбить на предложения
#2 разбить на токены
#3 нормализовать токены
#4 частотность токенов = FreqDist() кол-во вхождений
#5 словарь для предложений => key= порядковый номер предложения в тексте, value = сумма частотностей слов в предложении (вес)
#6 сортировка в словарь по убыванию веса
#7 Задать процент сжатия => и отфильтровать словарь, взять 0.1 от словаря
#8 отсортировать по key и выбрать из #1

import nltk
from nltk.probability import FreqDist
import pymorphy2
import string
from nltk.corpus import stopwords
from collections import OrderedDict

def WriteFile(fileName, sentences):
    with open(fileName, "w", encoding='utf-8') as output:
          [output.write(sentence+' ') for sentence in sentences] 

def ReadFile(fileName):
    with open(fileName, "r", encoding='utf-8') as file:
        return file.read()

def Tokens(text):
    tokens = nltk.word_tokenize(text)
    tokens = [i for i in tokens if (i not in string.punctuation)]
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '-', 'к', 'на', '...'])
    tokens = [i for i in tokens if (i not in stop_words)]
    return tokens

def Normalize(tokens):
     morph = pymorphy2.MorphAnalyzer()
     normalizedTokens = []
     for token in tokens:
         nToken = morph.parse(token)[0]
         normalizedTokens.append(nToken.normal_form) 
     return normalizedTokens

text = ReadFile("4 задание input.txt")
sentences = nltk.sent_tokenize(text, language="russian")

tokens = []
for sent in sentences:
    tokens.append(Tokens(sent))

normTokens = [Normalize(token) for token in tokens]

freqNormTokens = [FreqDist(normToken) for normToken in normTokens]

sentencesFreqs = {}
iterator = 0
for sent in freqNormTokens:
    sumWeight = 0
    for f in sent:
        print(f + ', ' + str(sent[f]) + ' ' )
        sumWeight += sent[f]
    sentencesFreqs[iterator]= sumWeight
    iterator+=1
    print(str(sumWeight)+'\n')

reversSortSentencesFreqs = {k: v for k, v in sorted(sentencesFreqs.items(), key=lambda item: item[1], reverse=True)}
print("Сортировка по убыванию веса: " + str(reversSortSentencesFreqs))

compression = 0.99
compressSortedSentencesFreqs = dict(list(reversSortSentencesFreqs.items())[:round(len(reversSortSentencesFreqs)*compression)])
print("Сжатие: " + str(compressSortedSentencesFreqs))

sortSentencesFreqs = OrderedDict(sorted(compressSortedSentencesFreqs.items(), key=lambda t: t[0]))

result = []
for i in sorted(sortSentencesFreqs.keys()):
    result.append(sentences[i])
print(result)
WriteFile('4 задание output.txt',result)







