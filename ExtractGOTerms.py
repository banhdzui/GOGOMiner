'''
Created on 29 Oct 2018

@author: danhbuithi
'''

import sys 
from common.CommandArgs import CommandArgs
from preprocessing.GOCollection import GOCollection
from preprocessing.PubMedCorpus import PubMedCorpus
from preprocessing.GOExtractor import GOExtractor

if __name__ == '__main__':
    config = CommandArgs({'input'   : ('', 'Path of document files'),
                          'go'      : ('', 'Path of GO terms'),
                          'output' : ('', 'Path of output file')
                          })    
    
    if not config.load(sys.argv):
        print ('Argument is not correct. Please try again')
        sys.exit(2)

    '''
    collector = GOCollection()
    collector.extractFromObo(config.get_value('input'))
    collector.saveAsXML(config.get_value('output'))
    
    '''
    corpus = PubMedCorpus(None)
    documents = corpus.load(config.get_value('input'))
    
    collector = GOCollection()
    collector.loadFromXml(config.get_value('go'))
    
    extractor = GOExtractor(collector)
    for document in documents:
        terms = extractor.extract(document)
        print(','.join([str((t, collector.term_dict[t])) for t in terms]))
        print('---------------')
        print('testing for branches')
    
