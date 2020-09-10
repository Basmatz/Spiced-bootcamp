import re
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Flatten, LSTM, Embedding
from tensorflow.keras.preprocessing import sequence

from sklearn.model_selection import train_test_split



# import data
file = '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_9/DollyPartonCorpus.txt'
dolly_raw = open(file).read()


trial = '''Well the two new people that's moved to the middle of the block
And we're at the top of the town and don't you think we're not
Well we found love and happiness people envy us you see
'''


# clean data


def clean_text(data):
    '''
    Takes input data; splits it into lines (= sentences); splits these into indvidual words (lowercase); removes empty items & overly short lines; returns list of lists.
    '''
    new = data.split('\n')
    new = [re.findall('(?u)\\b\\w\\w+\\b', x) for x in new]
    new = [[x.lower() for x in line] for line in new]
    new = [x for x in new if len(x) > 3] # remove empty lists and any line shorter than 3 words
    return new

dolly_new = clean_text(dolly_raw)

# investigate lengths of each song lyric line

sorted([len(line) for i, line in enumerate(dolly_new)])[0] # shortest line
sorted([len(line) for i, line in enumerate(dolly_new)])[-1] # longest line

# for i, line in enumerate(dolly_new):
#     if len(line) < 5:
#         print(line)

# vectorise X data

vocab_list = []
for line in dolly_new:
    for word in line:
        vocab_list.append(word)

vocab_list = list(set(vocab_list)) # set() drops duplicates
vocab_size = len(vocab_list) + 1

word_to_num = {}

for i, word in enumerate(vocab_list):
    word_to_num[word] = i+1 #i+1 because we're reserving 0 for blank space

# create X and y data
# X data is all but the last word in each line
# y data is last word in line.

vec_y = [[word_to_num[word] for word in line[-1:]] for line in dolly_new] # from 2nd to last item
# however, vec_y currently has one dimension too many, so let's flatten it using list comprehension
vec_y_list = [list[0] for list in vec_y]
vec_X = [[word_to_num[word] for word in line[:-1]] for line in dolly_new] # from 1st to penultimates item

vec_y[0:3]
vec_y_list[0:3]
vec_X[0:3]


# checking: word "the" appears in 2nd and penultimate position; no. 733 does too.
# dolly_new[:1]
# vec_X[:1]

# add padding to ensure all lines are same length

# find out maximum length of dolly parton lines
lengths = [len(line) for i, line in enumerate(dolly_new)]
maxlen = max(lengths)
meanlen = sum(lengths)/len(lengths)

# pad X to uniform length
pad_vec_X = sequence.pad_sequences(vec_X, maxlen=maxlen, padding='pre')

pad_vec_X.shape


# train-test split!

Xtrain, Xtest, ytrain, ytest = train_test_split(pad_vec_X, np.array(vec_y_list))

Xtrain.shape
Xtest.shape
ytrain.shape
ytest.shape

## build model

model = Sequential()
model.add(Embedding(input_dim=vocab_size,
                    output_dim=32,
                    input_length=maxlen))
model.add(LSTM(units=256))
model.add(Dense(vocab_size, activation='softmax'))

model.summary()

## compile

model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

## train!

history = model.fit(Xtrain, ytrain, epochs=10, batch_size=120, validation_split=0.2)



plt.plot(history.history['acc'], label='accuracy')
plt.plot(history.history['val_acc'], label='val accuracy')
plt.legend()

plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.legend()

model.evaluate(Xtest, ytest)


#





#
