# to do:
# create corpus for each artist
# define model for each artist
# create system that creates prediction for input text

import os
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from imblearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB

#### CREATING CORPORA

## get list of directories (= artists)

files = [f for f in os.listdir('.') if os.path.isdir(f) and not f.startswith('.')]


CORPUS = open('WomenInCountry.txt', 'r').read().split('\n')
LABELS = open('WomenInCountry_Labels.txt', 'r').read().split('\n')

CORPUS = CORPUS[:-1]
LABELS = LABELS[:-1]

dict_rus = {
    'DollyParton' : 300
}

dict_ros = {
    'BrandiCarlile' : 250,
    'AlisonKrauss' : 250
}

# Build Model

def language_model(corpus, labels):
    '''
    Trains a Naive Bayes model on the corpus.

    Input: corpus -- text containing all song lyrics by all artists under consideration.
    '''

    cv = CountVectorizer(stop_words = "english")
    clean_corpus = cv.fit_transform(corpus)
    tf = TfidfTransformer()
    vec2 = tf.fit_transform(clean_corpus)
    rus = RandomUnderSampler(sampling_strategy = dict_rus)
    ros = RandomOverSampler(sampling_strategy = dict_ros)
    bayes = MultinomialNB(alpha = 1)
    model = make_pipeline(cv, tf, rus, ros, bayes)

    model.fit(corpus, labels)

    return model

# Make a prediction

def predict(model, new_text):
    """
    Makes a new prediction based on the trained model and some new text input from the user.
    """
    new_text = [new_text]

    prediction = model.predict(new_text)

    return prediction[0]


# Run

if __name__ == '__main__':

    model = language_model(CORPUS, LABELS)
    user_input = input('What lyric do you want to predict an artist for? ')
    prediction = predict(model, user_input)
    print('Here is your prediction!')
    print(prediction)
