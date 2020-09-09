# launch this from within the deep_learning_w8 Python environment.

from tensorflow.keras import Sequential # tensorflow terminology for feed-forward network
from tensorflow.keras.layers import Dense # fully-connected layers (normal layer of neurons)
from tensorflow.keras.layers import Activation
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import backend as K
from tensorflow.keras.callbacks import EarlyStopping

import matplotlib.pyplot as plt

from contextlib import redirect_stdout

(xtrain, ytrain), (xtest, ytest) = mnist.load_data()

# reshape the x data
xtrain.shape
xtest.shape

def reshape_for_nn(data):
    data = data.reshape(data.shape[0], data.shape[1]*data.shape[2])
    return data

xtrain2 = reshape_for_nn(xtrain)
xtest2 = reshape_for_nn(xtest)

xtrain2.shape
xtest2.shape

# one-hot encode the y data

ytrain2 = to_categorical(ytrain, num_classes=10)
ytest2 = to_categorical(ytest, num_classes=10)

ytrain2.shape
ytest2.shape

# plotting function

def plot_performance(history):
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.legend(loc='upper left')


# writing notes to lab book doc
file = '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_9/experiment_log.txt'

def write_notes(model, batch_size, epochs, history, score, acc):
    with open(file, 'a') as f:
        with redirect_stdout(f):
            model.summary()
        f.write(f'Compilation parameters: batch size is {batch_size}, no. epochs is {epochs}\n\n')
        f.write(f"Final accuracy: {history.history['accuracy']} \n\n")
        f.write(f'Test score: {score} \n')
        f.write(f'Test accuracy: {acc} \n')
        f.write(f'--------------------------------------- \n\n\n')

# function for running model
def run_model(model):
    callback = EarlyStopping(monitor='val_loss', patience=3)
    K.clear_session()
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics='accuracy')
    epochs = 200
    batch_size = 500
    history = model.fit(xtrain2, ytrain2, epochs=epochs, batch_size=batch_size, verbose=1, callbacks=[callback], validation_split=0.2)
    score, acc = model.evaluate(xtest2, ytest2, batch_size=batch_size)
    plot_performance(history)
    write_notes(model, batch_size, epochs, history, score, acc)
    print(f'Test score is: {score}\n Test accuracy is: {acc}')


# model 1
model1 = Sequential([
    Dense(2, input_shape=(784,)),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])

run_model(model1)


# model 2
model2 = Sequential([
    Dense(300, input_shape=(784,)),
    Activation('relu'),
    Dense(100),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])

run_model(model2)


# model 3... let's be a little more modest

model3 = Sequential([
    Dense(100, input_shape=(784,)),
    Activation('relu'),
    Dense(30),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])

run_model(model3)


# model 4: extra hidden layer

model4 = Sequential([
    Dense(300, input_shape=(784,)),
    Activation('relu'),
    Dense(100),
    Activation('relu'),
    Dense(30),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])

run_model(model4)


# model 5

model5 = Sequential([
    Dense(200, input_shape=(784,)),
    Activation('relu'),
    Dense(100),
    Activation('relu'),
    Dense(50),
    Activation('relu'),
    Dense(30),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])

run_model(model5)


# model 6
model6 = Sequential([
    Dense(20, input_shape=(784,)),
    Activation('relu'),
    Dense(10),
    Activation('relu'),
    Dense(10),
    Activation('relu'),
    Dense(10),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])

run_model(model6)


# model 7
model7 = Sequential([
    Dense(20, input_shape=(784,)),
    Activation('relu'),
    Dense(10),
    Activation('relu'),
    Dense(10),
    Activation('relu'),
    Dense(10),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])

run_model(model7)



# model 8
model8 = Sequential([
    Dense(200, input_shape=(784,)),
    Activation('relu'),
    Dense(100),
    Activation('relu'),
    Dense(50),
    Activation('relu'),
    Dense(25),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])

run_model(model8)


# model 8
model9 = Sequential([
    Dense(800, input_shape=(784,)),
    Activation('relu'),
    Dense(200),
    Activation('relu'),
    Dense(100),
    Activation('relu'),
    Dense(50),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])

run_model(model9)
