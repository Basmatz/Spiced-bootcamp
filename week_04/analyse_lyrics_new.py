#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 17:57:51 2020

@author: stazhe
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd


import stanza
from spacy_stanza import StanzaLanguage
# from spacy import displacy
# stanza.download('ru')
snlp = stanza.Pipeline(lang="ru")
nlp = StanzaLanguage(snlp)

with open("Кино: Братская любовь.txt", 'r') as textfile:
    text =textfile.read()
doc = nlp(text)
# displacy.render(doc, style="ent")

