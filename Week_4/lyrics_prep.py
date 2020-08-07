# Aim: create corpus of women country musicians;
# analyse data (v. briefly);
# correct class imbalance;
# find better Model

import os
import re
import pandas as pd
import numpy as np
import seaborn as sns

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler

from sklearn.naive_bayes import MultinomialNB

### step 1: build corpus, save with labels


#### CREATING CORPUS

## get list of directories (= artists)

files = [f for f in os.listdir('.') if os.path.isdir(f) and not f.startswith('.')]

CORPUS = []
LABELS = []

# Build Corpus
def add_artist_to_corpus(artist):
    '''
    Adds oeuvre of artist to corpus; adds artist label in separate list
    '''
    for fn in os.listdir(f'{artist}/'):
        if '.txt' in fn:
            if 'all_songs.txt' not in fn:
                # print(fn)
                text = open(f'{artist}/' + fn).read()
                text = re.sub('\n', ' ', text)
                CORPUS.append(text)
                CORPUS.append('\n')
                label = artist + '\n'
                LABELS.append(label)

for artist in files:
    add_artist_to_corpus(artist)

#add_artist_to_corpus('RhiannonGiddens')

# save corpus for later; save labels for later.

with open('WomenInCountry.txt', 'w') as file:
    file.writelines(CORPUS)

with open('WomenInCountry_Labels.txt', 'w') as file:
    file.writelines(LABELS)

# quickly explore data

LABELS = open('WomenInCountry_Labels.txt', 'r').read().split('\n')
CORPUS = open('WomenInCountry.txt', 'r').read().split('\n')

LABELS = LABELS[: -1]
CORPUS = CORPUS[: -1]


def make_pie(X, y):
    df = pd.DataFrame(X, y)
    df = df.reset_index()
    counts = df['index'].value_counts()
    counts.plot(kind = 'pie')


make_pie(CORPUS, LABELS)

# find out: what is the most frequent word per artist?

cv = CountVectorizer(stop_words = "english")

cv.fit(CORPUS)

vec = cv.transform(CORPUS)

# What is each artist's most unique word?
df = pd.DataFrame(vec.todense(), columns=cv.get_feature_names(), index=LABELS)
df

tf = TfidfTransformer()

tf.fit(vec)

vec2 = tf.transform(vec)

# find the highest tfidf for each artist; give index of this; this is the "most unique word"

df2 = pd.DataFrame(vec2.todense(), columns=cv.get_feature_names(), index = LABELS)
unique_words = df2.groupby(df.index).idxmax(axis = 1)

top = unique_words.groupby(df.index).value_counts()
print(top)


### DEAL WITH CLASS IMBALANCE

# this is the status quo:

len(CORPUS)
make_pie(CORPUS, LABELS)


























# first, randomly undersample

# dict lets you decide how many samples to use for each artist
dict_rus = {
    'DollyParton' : 300
}

rus = RandomUnderSampler(sampling_strategy = dict_rus)

CORPUS_rus, LABELS_rus = rus.fit_resample(np.array(vec2.todense()), np.array(LABELS))

# investigate how these are balanced now

CORPUS_rus.shape, LABELS_rus.shape



make_pie(CORPUS_rus, LABELS_rus)


# next, randomly oversample

dict_ros = {
    'BrandiCarlile' : 220,
    'AlisonKrauss' : 220
}

ros = RandomOverSampler(sampling_strategy = dict_ros)

CORPUS_ros, LABELS_ros = ros.fit_resample(CORPUS_rus, LABELS_rus)

CORPUS_ros.shape, LABELS_ros.shape

make_pie(CORPUS_ros, LABELS_ros)



#
