'''
Created on 30 Oct 2018

@author: danhbuithi
'''

from nltk.tokenize import sent_tokenize
from common.TextPreprocessing import stemmedTokens

class GOExtractor(object):
    '''
    classdocs
    '''

    def __init__(self, go_collector):
        '''
        Constructor
        '''
        self.go_collector = go_collector
        
    def extractFromSentence(self, text, threshold = 0.45):
        go_ids = []
        text_words = stemmedTokens(text)
        for term in self.go_collector.go_terms:
            c = term.similarity(text_words)
            if c >= threshold: 
                #print(c)
                #print(','.join(text_words))
                #print(self.go_collector.term_dict[term.id])
                #print('-----------------')
                go_ids.append(term.id)
        return go_ids
    
    def extract(self, document):
        go_ids = self.extractFromSentence(document.title)
        
        sent_tokens = sent_tokenize(document.abstract)
        for sent in sent_tokens:
            go_ids.extend(self.extractFromSentence(sent))
        return list(set(go_ids))
            