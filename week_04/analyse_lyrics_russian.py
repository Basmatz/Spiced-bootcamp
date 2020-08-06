#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 12:53:25 2020

@author: stazhe
"""
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity


# import spacy
from spacy.lang.ru import Russian
# from spacy.tokenizer import Tokenizer

def clean_text(review, model):
    """preprocess a string (tokens, stopwords, lowercase, lemma & stemming) returns the cleaned result
        params: review - a string
                model - a spacy model
                
        returns: list of cleaned tokens
    """
    
    new_doc = []
    doc = model(review)
    for word in doc:
        if not word.is_stop and word.is_alpha:
            new_doc.append(word.lemma_.lower())
            
    return new_doc


from spacy_russian_tokenizer import RussianTokenizer, MERGE_PATTERNS


nlp = Russian()

russian_tokenizer = RussianTokenizer(nlp, MERGE_PATTERNS)
nlp.add_pipe(russian_tokenizer, name='russian_tokenizer')

#nlp.tokenizer = russian_tokenizer


with open("Кино: Асфальт.txt", 'r') as textfile:
    contents =textfile.read() 
# doc =nlp(contents)         
corpus = [contents]

with open("Кино: Братская любовь.txt", 'r') as textfile:
    new_song =textfile.read()      

corpus.append(new_song)

with open("Кино: Война.txt", 'r') as textfile:
    new_song =textfile.read()      

corpus.append(new_song)

with open("Кино: Город.txt", 'r') as textfile:
    new_song =textfile.read()      

corpus.append(new_song)

cv = CountVectorizer(tokenizer = nlp.tokenizer)
# cv = CountVectorizer()
vec_corpus = cv.fit_transform(corpus)
df = pd.DataFrame(vec_corpus.todense(), columns=cv.get_feature_names(), index=['Асфальт', "Братская любовь", "Война", "Город"])
print(df)

tf = TfidfTransformer()
tf_corpus = tf.fit_transform(vec_corpus)
df2 = pd.DataFrame(tf_corpus.todense(), columns=cv.get_feature_names(), index=['Асфальт', "Братская любовь", "Война", "Город"])
print(df2)

doc=nlp(corpus[0])
for token in doc:
    print(token, token.lemma_, token.pos_, token.dep_, token.is_stop)

for token1 in doc:
    if not token1.is_stop:
        for token2 in doc:
            if not token2.is_stop:
                if token1.similarity(token2)>0.5:
                    print(token1.text, token2.text, token1.similarity(token2))
                    
doc2= clean_text(corpus[0], nlp)
print(doc2)
