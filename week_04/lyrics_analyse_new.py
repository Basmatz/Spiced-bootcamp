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
    text : lemmatised version of the text without stop words or punctuation (str)

    """
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords\
              and token != " " \
              and token.strip() not in punctuation]
    
    text = " ".join(tokens)
    
    return text
