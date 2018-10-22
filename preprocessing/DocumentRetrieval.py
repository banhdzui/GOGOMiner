'''
Created on 19 Oct 2018

@author: danhbuithi
'''
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class DocumentRetrieval(object):
    '''
    classdocs
    '''


    def __init__(self, query, pubmed_db):
        '''
        Constructor
        '''
        self.query = query
        self.document_db = pubmed_db
        
        
    def cosineScore(self, document):
        query_words = set(self.query.keys())
        doc_words = set(document.keys())
        
        inter_words = query_words & doc_words
        a = 0
        for w in inter_words:
            a += self.query[w] * doc_words[w]
        if a == 0: return 0
        
        b = np.linalg.norm(query_words.values())
        c = np.linalg.norm(doc_words.values())
        return a / (b * c)
    
    
    def corpus2Vectors(self):
        corpus = self.document_db.getCorpus()
        vectorizer = TfidfVectorizer(corpus, stop_words='english')
        X = vectorizer.fit_transform(corpus)
        feature_names = vectorizer.get_feature_names()
        
        documents = []
        _, m = X.shape
        for row in X: 
            doc = {feature_names[i]: row[i] for i in range(m) if row[i] > 0.0}
            documents.append(doc)
        return documents
                