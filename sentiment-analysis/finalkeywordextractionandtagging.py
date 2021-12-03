# -*- coding: utf-8 -*-
"""finalKeywordExtractionandTagging.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JW_u1yidoxgfR38wk0jxKkvxs4V0EjBM
"""
import wordcloud

import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

import numpy as np # linear algebra
import pandas as pd 
import re
import csv
import string

import spacy
from tqdm import tqdm
import time
import pickle
import tensorflow as tf
import tensorflow_hub as hub

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression

# Binary Relevance
from sklearn.multiclass import OneVsRestClassifier

# Performance metric
from sklearn.metrics import f1_score

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

from skmultilearn.problem_transform import BinaryRelevance
from sklearn.naive_bayes import GaussianNB

from autocorrect import Speller
from rake_nltk import Rake

import yake

#Cleanse data for better analysis
stopwords = set(stopwords.words("english"))
spell = Speller(lang='en')

def data_cleanse(line):
# Removes all special characters and numericals leaving the alphabets
    line = line.lower()
    line = re.sub('@', '', line)
    line = re.sub('\[.*?\]', '', line)
    line = re.sub('https?://\S+|www\.\S+', '', line)
    line = re.sub('<.*?>+', '', line)
    line = re.sub('[%s]' % re.escape(string.punctuation), '', line)
    line = re.sub('\n', '', line)
    line = re.sub('\w*\d\w*', '', line)
    line = re.sub(r"[^a-zA-Z ]+", "", line)
    
    #Tokenize the data
    line = nltk.word_tokenize(line)
    #Remove stopwords
    line = [w for w in line if w not in stopwords]
    line = [spell(w) for w in line]
    final = ' '.join(line)
    return final.lower()

def feature_buildtext(line):
    lineVal = str(line)
    data = []
    r.extract_keywords_from_text(lineVal)
    dataKeys = r.get_ranked_phrases()[:10]
    print(dataKeys[0])
    for w in dataKeys[0].split(): 
      data.append(w)
      if len(data) != 0:
        adjective = nltk.pos_tag(data)
        for nn_val in [item for item in adjective if item[1] == 'NN']:
          for jj_val in [item for item in adjective if item[1] in ['JJ', 'JJR', 'JJS']]:
            keyPhrase = jj_val[0] +' '+ nn_val[0];
            if keyPhrase not in allFeatures_list:
              allFeatures_list.append(keyPhrase) 
    return allFeatures_list
       
# Key word extraction
feature_list = []

r = Rake()
def data_keyword_extract(line):
    lineVal = str(line)
    data = []
    keywordList = []
    newPhraseList = []
    normal = 1
    r.extract_keywords_from_text(lineVal)
    dataKeys = r.get_ranked_phrases()[:5]
    if normal == 1:
      if len(dataKeys) > 0:
        for w in dataKeys[0].split(" "):
          data.append(w)
          if len(data) != 0:
            adjective = nltk.pos_tag(data)
            for nn_val in [item for item in adjective if item[1] == 'NN']:
              for jj_val in [item for item in adjective if item[1] in ['JJ', 'JJR', 'JJS']]:
                keyPhrase = jj_val[0] +' '+ nn_val[0];
                if keyPhrase not in newPhraseList:
                  if keyPhrase in selected_list:
                    newPhraseList.append(keyPhrase) 
      kw_extractor = yake.KeywordExtractor(lan="en", n=2, dedupLim=0.1, top=2, features=None)
      dataKeys = kw_extractor.extract_keywords(lineVal)[:2]
      for phrs in list(map(lambda x: x[0], dataKeys)):
        if phrs in selected_list:
          if phrs not in newPhraseList:
            newPhraseList.append(phrs)
    return newPhraseList

def data_keyword_extract_yake(line):
    lineVal = str(line)
    data = []
    keywordList = []
    ######yake
    kw_extractor = yake.KeywordExtractor(lan="en", n=2, dedupLim=0.9, top=2, features=None)
    dataKeys = kw_extractor.extract_keywords(lineVal)[:2]
    keywordList = list(map(lambda x: x[0], dataKeys))
    
    return keywordList

def feature_buildtext(line):
    lineVal = str(line)
    data = []
    r.extract_keywords_from_text(lineVal)
    dataKeys = r.get_ranked_phrases()[:10]
    #print(dataKeys[0])
    for w in dataKeys[0].split(): 
      data.append(w)
      if len(data) != 0:
        adjective = nltk.pos_tag(data)
        for nn_val in [item for item in adjective if item[1] == 'NN']:
          for jj_val in [item for item in adjective if item[1] in ['JJ', 'JJR', 'JJS']]:
            keyPhrase = jj_val[0] +' '+ nn_val[0];
            if keyPhrase not in allFeatures_list:
              allFeatures_list.append(keyPhrase) 
    return allFeatures_list


multilabel_binarizer = MultiLabelBinarizer()
tfidf = TfidfVectorizer(tokenizer=feature_buildtext,max_df=0.8, max_features=100000)

def infer_tags(q):
    
    filename = (r'https://raw.githubusercontent.com/rps2ff23/CourseProject/main/sentiment-analysis/finalized_model.sav')
    
    # load the model from disk
    loaded_model = pickle.load(open(filename, 'rb'))
    
    result = []
    interim = []
    q = data_cleanse(q)
    q_vec = tfidf.transform([q])
    q_pred = loaded_model.predict(q_vec)
    interim = multilabel_binarizer.inverse_transform(q_pred)
    if len(interim) != 1:
      result = interim
    else:
      if not interim[0]:
        result = data_keyword_extract(q)
        if len(result) == 0:
          result = data_keyword_extract_yake(q)
      else:
        result = interim
    return result

if __name__ == "__main__":
    
    quest = sys.argv[1]
    return infer_tags(quest)