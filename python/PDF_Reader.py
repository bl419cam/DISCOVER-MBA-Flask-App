import slate3k as slate
import pandas as pd
import numpy as np
import string
import pickle

import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize

fillers = ['page', 'years', 'months', 'year', 'month', 'january', 'february', 'march', 'april', 'june', 'july', 
           'august', 'september', 'october', 'november', 'december']

def parse_pdf(file_path):
    
    with open(file_path,'rb') as file:
        extracted_text = slate.PDF(file)
        
    tokens = []
    for page in extracted_text:
        tokens += word_tokenize(page)
        
    clean_tokens = [tok for tok in tokens if tok.lower() not in fillers]
    
    index = 0
    exp_section = []
    edu_section = []
    for tok in clean_tokens:
        if tok == 'Experience':
            exp_start = index
        elif tok == 'Education':
            exp_end = index
            edu_start = index+1
        
        index += 1
        
    exp_section = clean_tokens[exp_start:exp_end]
    edu_section = clean_tokens[edu_start:]
    
    edu_corpus = ' '.join(edu_section)
    exp_corpus = ' '.join(exp_section)
    
    return edu_corpus, exp_corpus