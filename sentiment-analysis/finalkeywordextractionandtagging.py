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

from sklearn.svm import SVC

from skmultilearn.problem_transform import BinaryRelevance
from sklearn.naive_bayes import GaussianNB

from autocorrect import Speller
from rake_nltk import Rake

import yake

#Cleanse data for better analysis
stopwords = set(stopwords.words("english"))
spell = Speller(lang='en')

def freq_words(x, terms = 30):
  all_words = ' '.join([text for text in x])
  all_words = all_words.split()
  
  fdist = nltk.FreqDist(all_words)
  words_df = pd.DataFrame({'word':list(fdist.keys()), 'count':list(fdist.values())})
  
  # selecting top 20 most frequent words
  d = words_df.nlargest(columns="count", n = terms) 
  print(d)
  
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

def select_columns(data_frame, column_names):
    new_frame = data_frame.loc[:, column_names]
    return new_frame

# import spaCy's language model
nlp = spacy.load('en')

# Lemmatize the reviews
lemmatizer = WordNetLemmatizer()
def lem(line):
    mwords = []
    for word in line.split(" "):
      line = lemmatizer.lemmatize(word)
      mwords.append(line)
    return ' '.join(mwords)

def default_data_keyword_extract(line):
    lineVal = str(line)
    data = []
    keywordList = []
    normal = 1
    ######gensim - -- dataKeys = keywords(lineVal)

    if normal == 1:
      ######rake
      r.extract_keywords_from_text(lineVal)
      dataKeys = r.get_ranked_phrases()[:5]
      if len(dataKeys) > 0:
        for w in dataKeys[0].split(" "):
          data.append(w)
          if len(data) != 0:
            adjective = nltk.pos_tag(data)
            for wtype in adjective:
              if wtype[1] in ['JJ', 'JJR', 'JJS']:
                spellChkWord = spell(wtype[0])
                if spellChkWord not in feature_list:
                  feature_list.append(spellChkWord)
                if spellChkWord not in keywordList and spellChkWord !="pron" and spellChkWord != "PRON":
                  keywordList.append(spellChkWord)
    
    return keywordList

def data_keyword_extract(line):
    lineVal = str(line)
    data = []
    keywordList = []
    ######yake
    kw_extractor = yake.KeywordExtractor(lan="en", n=2, dedupLim=0.9, top=10, features=None)
    dataKeys = kw_extractor.extract_keywords(lineVal)[:2]
    #print(dataKeys)
    keywordList = list(map(lambda x: x[0], dataKeys))
    
    return keywordList
    
    
def build_model():
    url_data = (r'https://raw.githubusercontent.com/rps2ff23/CourseProject/main/sentiment-analysis/Coursera_reviews_subset.csv')
    
    coursedata_train = pd.read_csv(url_data, engine='python', error_bad_lines=False).dropna()
    coursedata_train = coursedata_train.drop_duplicates(subset = ['reviews', "course_id"])

    #print(coursedata_train.columns.tolist())

    url_data = (r'https://raw.githubusercontent.com/rps2ff23/CourseProject/main/sentiment-analysis/spreadsheet.csv')
    proffessordata_train = pd.read_csv(url_data, engine='python',header='infer',error_bad_lines=False).dropna()
    proffessordata_train = proffessordata_train.drop_duplicates(subset = ['comment'])
    #print(proffessordata_train.columns.tolist())

    data_train_1 = select_columns(coursedata_train, ['reviews']) #Course Feedback
    data_train_2 = select_columns(proffessordata_train, ['comment']).rename(columns = {'comment' : 'reviews'}) #Professor feedback

    #Combine professor feedback and course feedback
    data_train_1 = data_train_1.append(data_train_2)
    data_train = data_train_1

    #print(len(data_train_1), len(data_train_2))
    data_train.replace(to_replace=r'[\n\r\t]', value='', regex=True, inplace=True)

    data_train['Cleaned Reviews'] = data_train['reviews'].apply(data_cleanse)

    final_data = select_columns(data_train, ['Cleaned Reviews'])
    #print(final_data)
    #freq_words(final_data['Cleaned Reviews'], 100)

    #print(data_train)

    final_data = final_data.drop_duplicates(subset="Cleaned Reviews")
    #print(final_data)



    final_data['Cleaned Reviews'] = final_data['Cleaned Reviews'].apply(lem)


    #print(final_data['Cleaned Reviews'])

    # Key word extraction
    feature_list = []

    # Uses stopwords for english from NLTK, and all puntuation characters by
    # default
    r = Rake()

    #print(final_data['Cleaned Reviews'])


    final_data['keyword'] = final_data['Cleaned Reviews'].apply(data_keyword_extract)

    #print(final_data)


    # Using keyword based multilable binarizer
    multilabel_binarizer = MultiLabelBinarizer()
    multilabel_binarizer.fit(final_data['keyword'])
    y = multilabel_binarizer.transform(final_data['keyword'])
    #print(y)

    tfidf = TfidfVectorizer(max_df=0.8, max_features=10000)
    #print(tfidf.get_feature_names_out())
    #print(len(tfidf.get_feature_names_out()))
    #print(features)

    # split dataset into training and validation set

    xtrain, xval, ytrain, yval = train_test_split(final_data['Cleaned Reviews'],y, test_size=0.2, random_state=9)

    #print(xtrain.shape)
    #print(xval.shape)

    xtrain_tfidf = tfidf.fit_transform(xtrain)
    xval_tfidf =  tfidf.transform(xval)


    #print(xtrain_tfidf.shape, xval_tfidf.shape, ytrain.shape, yval.shape)

    lr = LogisticRegression()
    clf = BinaryRelevance(GaussianNB())

    # fit model on train data
    clf.fit(xtrain_tfidf, ytrain)
    
    # save the model to disk
    filename = 'finalized_model.sav'
    pickle.dump(clf, open(filename, 'wb'))


def infer_tags(q):
    result = []
    interim = []
    q = data_cleanse(q)
    q_vec = tfidf.transform([q])
    q_pred = clf.predict(q_vec)
    interim = multilabel_binarizer.inverse_transform(q_pred)
    if len(interim) != 1:
      result = interim
    else:
      if not interim[0]:
        result = data_keyword_extract(q)
      else:
        result = interim
    return result


if __name__ == "__main__":

    build_model()
    
    quest = "great lecturer way teaching highly engaging visual well make system programming fun interesting"
    print("Original Review Text: ", quest, "\nPredicted keyword: ", infer_tags(quest), "\n")