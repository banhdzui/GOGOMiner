'''
Created on 29 Oct 2018

@author: danhbuithi
'''
import math
import re 

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def stemmedTokens(text):
 
    clean = re.sub(r"[(=):,.;@#?!&$><]+\ *", " ", text.lower())

    tokens = nltk.word_tokenize(clean)
    tokens = [word for word in tokens if word not in stopwords.words('english')]

    result = []
    ps = PorterStemmer()
    for word in tokens:
        result.append(ps.stem(word))
    return list(set(result))

def cosineSimilarity(word_set_1, word_set_2):
    if word_set_1 is None or word_set_2 is None: return 0
    inter_words = set(word_set_1) & set(word_set_2)
    
    a = len(inter_words)
    if a == 0: return 0
    
    b = math.sqrt(len(word_set_1))
    c = math.sqrt(len(word_set_2)) 
    return a / (b * c)


def getStringBetween(s, mark):
    return s[s.find(mark)+1: s.rfind(mark)]