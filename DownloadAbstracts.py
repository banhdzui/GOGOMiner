'''
Created on 22 Oct 2018

@author: danhbuithi
'''
import sys 
from common.CommandArgs import CommandArgs
from preprocessing.PubMedCorpus import PubMedCorpus

if __name__ == '__main__':
    config = CommandArgs({
                          'output' : ('', 'Path of output file'),
                          'limit'   : (100000, 'Number of maximum returned abstracts')
                          })    
    
    if not config.load(sys.argv):
        print ('Argument is not correct. Please try again')
        sys.exit(2)
        
    corpus = PubMedCorpus(api_key='6a2ee604e5f4598018ce6134ab6fc8851308')
    keywords = 'mycobacterium tuberculosis gene'
    corpus.downloadAbstract(keywords, file_name = config.get_value('output'), max_return=int(config.get_value('limit')))
