import numpy as np
import pandas as pd
import string
#import timeit
import pickle

import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize, FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity

#open files saved in pickles
with open('./python/ref_data.pickle', 'rb') as file:
        ref_data = pickle.load(file)

with open('./python/edu_vectorizer.pickle', 'rb') as file:
        edu_vectorizer = pickle.load(file)
        
with open('./python/exp_vectorizer.pickle', 'rb') as file:
        exp_vectorizer = pickle.load(file)

stp_wrds_list = stopwords.words('english')
stp_wrds_list += list(string.punctuation)

other_wrds = ['ltd','eg', 'etc', 'inc', 'de']
stp_wrds_list += other_wrds

num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
stp_wrds_list += num_list

def tokenize_text(corpus, stops):
    
    pattern = "([a-zA-Z]+(?:'[a-z]+)?)"
    raw_tokens = nltk.regexp_tokenize(corpus, pattern)
    token_text = [tok.lower() for tok in raw_tokens]
    
    clean_tokens = [tok for tok in token_text if tok not in stops]
    
    return clean_tokens

def convert_corpus(corpus, stops):
    tokens = tokenize_text(corpus, stops)
    reduced_corpus = ' '.join(tokens)
    
    return reduced_corpus

def recommend_business_school(education, experience):
    
    #start = timeit.default_timer()
    edu = education
    exp = experience
    
    edu_corpus = convert_corpus(edu, stp_wrds_list)
    exp_corpus = convert_corpus(exp, stp_wrds_list)
    
    edu_vec = edu_vectorizer.transform([edu_corpus])
    exp_vec = exp_vectorizer.transform([exp_corpus])
    
    comp_list = []
    for prof in ref_data:
        comp_vec = {'id': prof['id'],
                    'edu_cos_sim': None,
                    'exp_cos_sim': None,
                    'agg_cos_sim': None,
                    'school_name': prof['MBA_School']}
        
        comp_vec['edu_cos_sim'] = cosine_similarity(prof['edu_vec'], edu_vec)
        comp_vec['exp_cos_sim'] = cosine_similarity(prof['exp_vec'], exp_vec)
        comp_vec['agg_cos_sim'] = comp_vec['edu_cos_sim']+comp_vec['exp_cos_sim']
   
        comp_list.append(comp_vec)
    
    order_comp = sorted(comp_list, key=lambda k: k['agg_cos_sim'], reverse=True) 
    
    topsch_list = [comp['school_name'] for comp in order_comp[:15]]
    
    #stop = timeit.default_timer()
    #print('Time: ', stop - start)
    
    return list(set(topsch_list))

