'''
Created on 29 Oct 2018

@author: danhbuithi
'''

import numpy as np 
import xml.etree.ElementTree as ET

from common.TextPreprocessing import tokenizeUnigrams, cosineSimilarity,\
    getStringBetween

'''
Object representing GO term. It includes id, name, definition, and synonyms (in stemmed form)
'''
class GOTerm(object):
    
    def __init__(self, descriptions=None):

        self.synonyms = []
        if descriptions is None: return
        
        self.id = descriptions['id']
        self.name = descriptions['name']
        
        self.name_words = tokenizeUnigrams(descriptions['name'])
    
        self.def_words = tokenizeUnigrams(descriptions['def'])
        
        for text in descriptions['synonym']:
            self.synonyms.append(tokenizeUnigrams(text))
           
    def similarity(self, word_set):
        values = []
        values.append(cosineSimilarity(self.name_words, word_set))
        values.append(cosineSimilarity(self.def_words, word_set))
        for synonym in self.synonyms:
            values.append(cosineSimilarity(synonym, word_set))
        return np.max(values)
        
    def getAllKeywords(self):
        keywords = []
        keywords.extend(self.name_words)
        keywords.extend(self.def_words)
        for syn in self.synonyms:
            keywords.extend(syn)
            
        return set(keywords)
    
    def printTerm(self):
        print(self.id)
        print(self.name_words)
        print(self.def_words)
        print(self.synonyms)
        
class GOCollection(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.go_terms = []
        self.term_id_name_dict = {}
        
    def addTerm(self, term):
        self.go_terms.append(term)
        self.term_id_name_dict[term.id] = term.name
        
    def extractFeatures(self):
        feature_list = []
        for term in self.go_terms:
            feature_list.extend(term.getAllKeywords())  
        
        feature_list = list(set(feature_list))
        return {feature_list[i]: i for i in range(len(feature_list))} 
        
    def extractFromObo(self, file_name):
        self.go_terms = []
        term = None
        i = 0
        with open(file_name, 'r') as obo_file:
            for line in obo_file:
                if line == '': continue
                if '[Term]' in line:
                    if term is not None:
                        self.addTerm(GOTerm(term))
                        if i % 100: print('#GO(s): ' + str(i))
                       
                    term = {'id': '', 'name': '', 'def' : '', 'synonym':[]}
                elif term is not None:
                    index = line.strip().find(':')
                    if index == -1: continue
                    key_str = line[:index].strip()
                    value_str = line[index+1:].strip()
                    
                    if key_str not in term: continue
                    if key_str == 'def':
                        term[key_str] = getStringBetween(value_str,'\"')
                    elif key_str == 'synonym':
                        term[key_str].append(getStringBetween(value_str, '\"'))
                    else:
                        term[key_str] = value_str
        if term is not None:
            self.addTerm(GOTerm(term))
            
        print(len(self.go_terms))
            
    def saveAsXML(self, file_name):
        go_list = ET.Element('GOList')
        
        for term in self.go_terms:
            
            term_item = ET.SubElement(go_list, 'term')
            term_item.set('id', term.id)
            term_item.set('text', term.name)
            
            name_item = ET.SubElement(term_item, 'name')
            name_item.text = ','.join(term.name_words)

            def_item = ET.SubElement(term_item, 'def')
            def_item.text = ','.join(term.def_words)
            
            for syn in term.synonyms:
                syn_item = ET.SubElement(term_item, 'synonym')
                syn_item.text = ','.join(syn)
            
        go_list_in_string = ET.tostring(go_list)
        xml_file = open(file_name, 'wb')
        xml_file.write(go_list_in_string)
        
    def loadFromXml(self, file_name):
        go_list = ET.parse(file_name)
        root = go_list.getroot() 
        
        self.go_terms = []
        for doc in root.findall('term'):
            term = GOTerm(None)
            term.id = doc.get('id')
            term.name = doc.get('text')
            
            term.name_words = (doc.find('name').text).split(',')
            term.def_words = (doc.find('def').text).split(',')
            term.synonyms = []
            for syn in doc.findall('synonym'):
                c = syn.text
                if c is None: continue
                term.synonyms.append(c.split(','))  
            self.addTerm(term)
        print('end of loading....')