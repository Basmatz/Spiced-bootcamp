#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 17:57:51 2020

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

# # import spacy

# # import stanza
# # from spacy_stanza import StanzaLanguage
# # # from spacy import displacy
# # snlp = stanza.Pipeline(lang="ru")
# # nlp = StanzaLanguage(snlp)

# mystem = Mystem()

# with open("Кино: Асфальт.txt", 'r') as textfile:
#      text =textfile.read()
# # doc = nlp(text)


#Create lemmatizer and stopwords list
mystem = Mystem() 
russian_stopwords = stopwords.words("russian")

#Preprocess function
def preprocess_text(text):
    """
    Takes a string of russian text and lemmatises it
    
    taken from https://www.kaggle.com/alxmamaev/how-to-easy-preprocess-russian-text
    

    Parameters
    ----------
    text : TYPE
        DESCRIPTION.

    Returns
    -------
    text : TYPE
        DESCRIPTION.

    """
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords\
              and token != " " \
              and token.strip() not in punctuation]
    
    text = " ".join(tokens)
    
    return text

preprocess_text(text)




# import spacy
# import ru2

# nlp = ru2.load_ru2('ru2')

# sample_sentences = "Привет Миру! Как твои дела? Сегодня неплохая погода."


# nlp.add_pipe(nlp.create_pipe('sentencizer'), first=True)
# doc = nlp(sample_sentences)
# for s in doc.sents:
#  	print(list(['lemma "{}" from text "{}"'.format(t.lemma_, t.text) for t in s]))

#  # -m spacy link "~/Desktop/Spiced/logistic-lemongrass-student-code/week_04/180.zip" "rusvec"
