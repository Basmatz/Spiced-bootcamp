import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist
import pandas as pd
import tensorflow

(xtrain, ytrain), (xtest, ytest) = mnist.load_data()

ytrain = to_categorical(ytrain)
ytest = to_categorical(ytest)

xtrain = pd.DataFrame(xtrain.reshape(60000, 784))
xtest = pd.DataFrame(xtest.reshape(10000, 784))

m = Sequential([
    Dense(units = 784, activation = 'relu',  input_shape = (784,)),
    Dense(units = 512, activation = 'relu'),
    Dense(units = 512, activation = 'relu'),
    Dense(units = 512, activation = 'relu'),
    Dense(units = 10, activation = 'softmax')
])

# build the computation graph
m.compile(optimizer=tensorflow.keras.optimizers.RMSprop(),
          loss=tensorflow.keras.losses.categorical_crossentropy,
          metrics=['accuracy'])

# print all layers
print(m.summary())

from livelossplot.inputs.tf_keras import PlotLossesCallback

# train the model
h  = m.fit(xtrain, ytrain, epochs=50, batch_size=120
           ,validation_data=(xtest, ytest),
           callbacks=[PlotLossesCallback()],
           verbose=0
           )