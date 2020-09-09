# launch this from within the deep_learning_w8 Python environment.

from tensorflow.keras import Sequential # tensorflow terminology for feed-forward network
from tensorflow.keras.layers import Dense # fully-connected layers (normal layer of neurons)
from tensorflow.keras.layers import Activation
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import backend as K
from tensorflow.keras.callbacks import EarlyStopping

import matplotlib.pyplot as plt
import pandas as pd

import logging
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

# set up empty lists for collecting model Performance
name_list = []
val_acc_list = []
train_acc_list = []
test_acc_list = []
overfit_by = []

# define batch size and epochs

epochs = 200
batch_size = 500

# function for appending info

def append_info(model_name, val_acc, train_acc, test_acc, fit_diff):
    name_list.append(model_name)
    val_acc_list.append(val_acc)
    train_acc_list.append(train_acc)
    test_acc_list.append(test_acc)
    overfit_by.append(fit_diff)


# plotting function

fig, axs = plt.subplots(2)
fig.suptitle('Vertically stacked subplots')
axs[0].plot(x, y)
axs[1].plot(x, -y)

def plot_performance(history, model_name, test_acc, no_epochs):
    fig, axs = plt.subplots(2, figsize=(12,8))
    fig.suptitle(f'Training Performance: {str(model_name)}')
    axs[0].plot(history.history['loss'], label='training loss')
    axs[0].plot(history.history['val_loss'], label='validation loss')
    axs[0].legend(loc='upper right')
    axs[1].set_ylim([0, 1])
    axs[1].plot(history.history['accuracy'], label='training accuracy', linestyle='dashed')
    axs[1].plot(history.history['val_accuracy'], label='validation accuracy', linestyle='dashed')
    axs[1].scatter(no_epochs, test_acc, label='test accuracy')
    axs[1].legend(loc='upper left')
    plt.savefig(f'/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_9/MNIST_NN_Plots/{model_name}.png')


# writing notes to lab book doc
filepath = '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_9/Experiment_Logs/'

def write_notes(filepath, model_name, model, batch_size, epochs, history, train_acc, test_acc, fit_diff):
    file = str(filepath) + 'log_' + str(model_name) + '.txt'
    with open(file, 'w') as f:
        f.write(f'----- MODEL: {model_name} -----\n')
        with redirect_stdout(f):
            model.summary()
        f.write(f'Compilation parameters: batch size is {batch_size}, no. epochs is {epochs}\n\n')
        f.write(f"Final accuracy: {train_acc} \n\n")
        # f.write(f'Test score: {score} \n')
        f.write(f'Test accuracy: {test_acc} \n')
        f.write(f'Difference in training and test accuracy: {round(fit_diff*100, 1)}%\n')
        f.write(f'--------------------------------------- \n\n\n')

# check on overfitting

def overfitting(train_acc, test_acc):
    fit_diff = train_acc - test_acc
    if fit_diff > .02:
        logging.critical(f'---- WARNING: Model appears to be overfitting by {round(fit_diff*100, 1)}% ----')
    else:
        logging.critical(f'Model does not seem to be overfitting \n Test-train accuracy difference is {round(fit_diff*100, 1)}%')
    return fit_diff

# function for running model
def run_model(model, model_name, filepath):
    callback = EarlyStopping(monitor='val_loss', patience=3)
    K.clear_session()
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics='accuracy')
    history = model.fit(xtrain2, ytrain2, verbose=0, epochs=epochs, batch_size=batch_size, callbacks=[callback], validation_split=0.2)
    score, test_acc = model.evaluate(xtest2, ytest2, batch_size=batch_size)
    train_acc = history.history['accuracy'][-1]
    val_acc = history.history['val_accuracy'][-1]
    fit_diff = overfitting(train_acc, test_acc)
    no_epochs = callback.stopped_epoch
    print(f'Last validation accuracy was: {val_acc}\nTraining accuracy is: {train_acc}\nTest accuracy is: {test_acc}')
    return history, test_acc, train_acc, val_acc, score, fit_diff, no_epochs


# function for all steps together:

def run_everything(model, model_name, filepath, batch_size, epochs):
    history, test_acc, train_acc, val_acc, score, fit_diff, no_epochs = run_model(model, model_name, filepath)
    plot_performance(history, model_name, test_acc, no_epochs)
    write_notes(filepath, model_name, model, batch_size, epochs, history, train_acc, test_acc, fit_diff)
    append_info(model_name, val_acc, train_acc, test_acc, fit_diff)


# model 1
model1 = Sequential([
    Dense(2, input_shape=(784,)),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])


run_everything(model1, 'model1', filepath, batch_size, epochs)



# model 2
model2 = Sequential([
    Dense(300, input_shape=(784,)),
    Activation('relu'),
    Dense(100),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])

run_everything(model2, 'model2', filepath, batch_size, epochs)


# model 3... let's be a little more modest

model3 = Sequential([
    Dense(100, input_shape=(784,)),
    Activation('relu'),
    Dense(30),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])

run_everything(model3, 'model3', filepath, batch_size, epochs)


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

run_everything(model4, 'model4', filepath, batch_size, epochs)


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

run_everything(model5, 'model5', filepath, batch_size, epochs)


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

run_everything(model6, 'model6', filepath, batch_size, epochs)


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

run_everything(model7, 'model7', filepath, batch_size, epochs)



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

run_everything(model8, 'model8', filepath, batch_size, epochs)


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

run_everything(model9, 'model9', filepath, batch_size, epochs)


### investigate metrics so far.
performance_data = {'model_name': name_list, 'validation_acc': val_acc_list, 'train_acc' : train_acc_list, 'test_acc': test_acc_list, 'overfitting': overfit_by}

performance = pd.DataFrame(performance_data)


performance











#
