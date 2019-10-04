import numpy as np
import pandas as pd
import string
import pickle

import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#open files saved in pickles
with open('./python/school_info_dict.pickle', 'rb') as file:
    school_info_dict = pickle.load(file)

with open('./python/core_df.pickle', 'rb') as file:
        core_df = pickle.load(file)

with open('./python/core_edu_vectorizer.pickle', 'rb') as file:
        edu_vectorizer = pickle.load(file)
        
with open('./python/core_exp_vectorizer.pickle', 'rb') as file:
        exp_vectorizer = pickle.load(file)

stp_wrds_list = stopwords.words('english')
stp_wrds_list += list(string.punctuation)

other_wrds = ['ltd','eg', 'etc', 'inc', 'de']
stp_wrds_list += other_wrds

num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
stp_wrds_list += num_list

tag_dict = {"J": wordnet.ADJ,
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "R": wordnet.ADV}

lemmatizer = WordNetLemmatizer()
scaler = MinMaxScaler()

def tokenize_text(corpus, stops):
    
    pattern = "([a-zA-Z]+(?:'[a-z]+)?)"
    raw_tokens = nltk.regexp_tokenize(corpus, pattern)
    token_text = [tok.lower() for tok in raw_tokens]
    
    lemma_tokens = []
    for tok in token_text:
        if tok not in stops:
            tok_tag = nltk.pos_tag([tok])[0][1][0]
            lemma_tokens.append(lemmatizer.lemmatize(tok, tag_dict.get(tok_tag, wordnet.NOUN)))
            
    return lemma_tokens

def convert_corpus(corpus, stops):
    tokens = tokenize_text(corpus, stops)
    reduced_corpus = ' '.join(tokens)
    
    return reduced_corpus

def recommend_business_school(edu_hist, exp_hist):
    
    edu = edu_hist
    exp = exp_hist
    
    edu_corpus = convert_corpus(edu, stp_wrds_list)
    exp_corpus = convert_corpus(exp, stp_wrds_list)
    
    edu_vec = edu_vectorizer.transform([edu_corpus])
    exp_vec = exp_vectorizer.transform([exp_corpus])
    
    core_df['edu_cos_sim'] = core_df['edu_vec'].apply(lambda x: cosine_similarity(x, edu_vec)[0][0])
    core_df['exp_cos_sim'] = core_df['exp_vec'].apply(lambda x: cosine_similarity(x, exp_vec)[0][0])
    
    core_df['edu_cos_sim'] = scaler.fit_transform(np.array(core_df['edu_cos_sim']).reshape(-1,1))
    core_df['exp_cos_sim'] = scaler.fit_transform(np.array(core_df['exp_cos_sim']).reshape(-1,1))
    
    core_df['sim_score'] = core_df['edu_cos_sim'] + core_df['exp_cos_sim']
    
    topsch_codes = list(set(list(core_df.sort_values(by='sim_score', ascending=False).head(15)['MBA_School'])))
    topsch_info = []
    for code in topsch_codes:
        #info = school_info_dict['School Name'][code]
        info = (school_info_dict['School Name'][code] + ' (' + school_info_dict['Location'][code] + ' - ' +
               school_info_dict['Country'][code] + ')')
        topsch_info.append(info)
        
    topsch_info.sort()
    
    return topsch_info