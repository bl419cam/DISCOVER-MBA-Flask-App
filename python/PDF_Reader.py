import slate3k as slate
import pandas as pd
import numpy as np
import string
import pickle

def parse_pdf(file_path):
    
    with open(file_path,'rb') as file:
        extracted_text = slate.PDF(file)
        
    lines = []
    for page in extracted_text:
        lines += page.split('\n')
    
    index = 0
    for line in lines:
        if line == 'Experience':
            exp_start = index
        elif line == 'Education':
            exp_end = index
            edu_start = index+1
        index += 1
        
    exp_raw = lines[exp_start+1:exp_end]
    edu_raw = lines[edu_start:]
        
    exp_section = []
    for line in exp_raw:
        if '\xa0' not in line and '\x0c' not in line and 'Page' not in line:
            exp_section.append(line)
    
    exp_corpus = '\n'.join(exp_section)
        
    edu_section = []
    for line in edu_raw:
        if len(line) > 0 and 'Page' not in line:
            edu_section.append(line)    
    
    edu_corpus = '\n'.join(edu_section)
    
    return edu_corpus, exp_corpus