import nltk
import pymorphy2
import string
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem.snowball import SnowballStemmer

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

def NormalizeByStemmer(tokens):
     normalizedTokens = []
     stemmer = SnowballStemmer("russian")
     for token in tokens:
         nToken = stemmer.stem(token)
         normalizedTokens.append(nToken) 
     return normalizedTokens 
        
def WriteFile(fileName, freqDictionary):
    with open(fileName, "w", encoding='utf-8') as output:
           for f in freqDictionary:
               output.write(f + ', ' + str(freqDictionary[f]) + '\n' )

def ReadFile(fileName):
    with open(fileName, "r", encoding='utf-8') as file:
        return file.read()


## Задание 1
text = ReadFile("input.txt")
tokens = Tokens(text)
normalizedTokens = Normalize(tokens)
freqDictionary = FreqDist(normalizedTokens)
WriteFile("output.txt", freqDictionary)

#Задание 2 Stemmer для нормализации
print("Pymorphy2 normalize:", Normalize(tokens))
print("nltk.stemmer normalize:", NormalizeByStemmer(tokens))


