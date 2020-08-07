#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 12:55:24 2020

@author: stazhe
"""

from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
import nltk
from spacy.lang.ru import Russian
from spacy_russian_tokenizer import RussianTokenizer, MERGE_PATTERNS
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

mystem = Mystem() 
russian_stopwords = stopwords.words("russian")

#Preprocess function

def preprocess_text(text):
    """
    Takes a string of russian text and lemmatises it
    
    taken from https://www.kaggle.com/alxmamaev/how-to-easy-preprocess-russian-text
    

    Parameters
    ----------
    text : a string of text in russian

    Returns
    -------
    text : lemmatised version of the input text without stop words or punctuation (str)

    """
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords\
              and token != " " \
              and token.strip() not in punctuation]
    
    text = " ".join(tokens)
    
    return text

def make_lemmatized_corpus (artist):
    """
    Opens all lyrics files beginning with artist name, lemmatises them and adds each lyrics string to the corpus.

    Parameters
    ----------
    artist : str. name of artist to search for in current directory.

    Returns
    -------
    list of strings, each item is the lemmatised text of a song

    """
    
    corpus = []
    for file in os.listdir('.'):
            if fnmatch.fnmatch(file.lower(), artist.lower()+(":")+("*")):
                with open(file, 'r') as textfile:
                    contents =textfile.read()      
                    lemmatized_lyrics = preprocess_text(contents)
                    corpus.append(lemmatized_lyrics)
    return corpus


nlp = Russian()
russian_tokenizer = RussianTokenizer(nlp, MERGE_PATTERNS)
nlp.add_pipe(russian_tokenizer, name='russian_tokenizer')

lemmatiser = FunctionTransformer(preprocess_text)
cv = CountVectorizer(tokenizer = nlp.tokenizer, stop_words="russian")
tf = TfidfTransformer()




artists_corpora = {}
for artist in search_results_artists.keys():     
     artists_corpora[artist] = make_lemmatized_corpus(artist)   



# vec_corpus = cv.fit_transform(corpus)

# tf_corpus = tf.fit_transform(vec_corpus)
# df2 = pd.DataFrame(tf_corpus.todense(), columns=cv.get_feature_names(), index=['Асфальт', "Братская любовь", "Война", "Город"])
# print(df2)
