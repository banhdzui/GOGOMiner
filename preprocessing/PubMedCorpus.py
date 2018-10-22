'''
Created on 22 Oct 2018

@author: danhbuithi
'''
from metapub import PubMedFetcher

import xml.etree.ElementTree as ET
import re 

class PubMedCorpus(object):
    '''
    classdocs
    '''

    def __init__(self, api_key):
        '''
        Constructor
        '''
        self.cache_dir = 'cache_dir/'
        self.api_key = api_key
        
    def removeHtmlTags(self, text):
        if text is None: return ''
        return re.sub('<[^<]+?>', '', text)
    
    
    def downloadAbstract(self, keywords, file_name,max_return=1e+6):
        fetcher = PubMedFetcher(cachedir=self.cache_dir, api_key=self.api_key)
        pmids = fetcher.pmids_for_query(keywords, retmax=max_return)
        
        corpus = ET.Element('corpus')
        keywords_item = ET.SubElement(corpus, 'keywords')
        keywords_item.text = keywords
        
        for pmid in pmids:
            print(pmid)
            fetcher._eutils_article_by_pmid(pmid)
            doc = fetcher.article_by_pmid(pmid)
            title_str = self.removeHtmlTags(doc.title)
            abstract_str = self.removeHtmlTags(doc.abstract)
            
            if abstract_str == '':
                continue
            
            doc_item = ET.SubElement(corpus, 'article')
            doc_item.set('id', pmid)
            
            title_item = ET.SubElement(doc_item, 'title')
            title_item.text = title_str

            abstract_item = ET.SubElement(doc_item, 'abstract')
            abstract_item.text = abstract_str
            
        corpus_in_string = ET.tostring(corpus)
        xml_file = open(file_name, 'wb')
        xml_file.write(corpus_in_string)
                
    
    def load(self, file_name):
        corpus_tree = ET.parse(file_name)
        root = corpus_tree.getroot() 
        
        result = []
        for doc in root.findall('article'):
            title = doc.find('title').text
            abstract = doc.find('abstract').text
            print(title)
            print('--------------------')
            result.append((title, abstract))
        return result