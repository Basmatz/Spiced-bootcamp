#!/usr/bin/env python
# coding: utf-8

# In[98]:


import tensorflow.keras


# In[101]:


from tensorflow.keras import Sequential # tf terminology for Feed-Forward Network
from tensorflow.keras.layers import Dense # Fully-connected layers (normal layer of neurons)
from tensorflow.keras.layers import Activation


# In[102]:


from tensorflow.keras import Sequential #tf terminology for Feed-Forward Network
from tensorflow.keras.layers import Dense #Fully-connected layers (normal layer of neurons)
from tensorflow.keras.layers import Activation


# In[7]:


import matplotlib.pyplot as plt


# In[103]:


from tensorflow.keras.datasets import mnist

(xtrain, ytrain), (xtest, ytest) = mnist.load_data()


# In[21]:


xtest.shape


# In[104]:


#getting the images flattened from a 28x28 2 dimension images into 784 items 1 dimension array creating a sequential layer stack
import pandas as pd

xtest_n = pd.DataFrame(xtest.reshape(10000, 784))


# In[29]:


xtest_n.shape


# In[30]:


ytest.shape


# In[105]:


# normalizing/standardizing the xtest data from pixels from 0 to 255 into pixels from 0 to 1, what is best for neuron weights
xtest1 = xtest_n / 255


# In[106]:


# I choose to work the model with 2 hidden layers and 1 output layer with 10 neurons
model = Sequential([
    Dense(300, input_shape=(784,)), 
    # choosing 300 neurons as a first hidden layer     
    Activation('relu'),
    # choosing activation function relu for our first hidden layer
    Dense(100),
    # 100 neurons for the second hidden layer
    Activation('relu'),
    # choosing activation function relu for our second hidden layer
    Dense(10),
    # 10 neurons output layer with probabilities for 10 classes (numbers 0 to 9), 
    # normalizes to probability distribution for each class
    # sums up to 1 for all classes
    Activation('softmax')
    # choosing activation function softmax for the output layer
])


# In[107]:


# categorical: for multi-class scenarios
# sparse: with 1 target class index (0..9), classes are exclusive
# cross entropy: probability difference between true and predicted classes
model.compile(optimizer='adam', loss= 'sparse_categorical_crossentropy', metrics=['accuracy'])


# In[108]:


history = model.fit(xtest1, ytest, epochs=50, batch_size= 500, verbose=1, validation_split=0.2)


# In[109]:


model.summary() # we have a total number of 266.610 parameters!
                # 235.500 parameters to train with 784 input data + 300 neurons + 1 bias for each node
                # 30100 for the second layer + bias
                # 1010 for the output layer + bias


# In[36]:


# evaluation of the model
score = model.evaluate(xtest1, ytest, batch_size=4)
print(score)


# In[50]:


plt.plot(history.history['loss'])
plt.plot(history.history['val_loss']) # model is overfitting


# In[38]:


plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy']) # accuracy of 100%, model is overfitting


# ### Batchnormalization

# In[68]:


from tensorflow.keras.layers import BatchNormalization


# In[69]:


# including the batch normalization 
model = Sequential([
    Dense(300, input_shape=(784,)),       
    Activation('relu'),
          BatchNormalization(),
    Dense(100),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])


# In[71]:


model.compile(optimizer='adam', loss= 'sparse_categorical_crossentropy', metrics=['accuracy'])


# In[72]:


# accuracy 100%
history_batch = model.fit(xtest1, ytest, epochs=50, batch_size= 500, verbose=1, validation_split=0.2)


# # 1 Dropout

# In[74]:


from tensorflow.keras.layers import Dropout


# In[77]:


model = Sequential([
    Dense(300, input_shape=(784,)), 
    Dropout(0.5),
    Activation('relu'),
    Dense(100),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])


# In[78]:


model.compile(optimizer='adam', loss= 'sparse_categorical_crossentropy', metrics=['accuracy'])


# In[79]:


history_dropout = model.fit(xtest1, ytest, epochs=50, batch_size= 500, verbose=1, validation_split=0.2)


# ### 1 Dropout and earlystopping

# In[83]:


from tensorflow.keras.callbacks import EarlyStopping


# In[87]:


model = Sequential([
    Dense(300, input_shape=(784,)), 
    Dropout(0.5),
    Activation('relu'),
    Dense(100),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])


# In[88]:


model.compile(optimizer='adam', loss= 'sparse_categorical_crossentropy', metrics=['accuracy'])


# In[89]:


callback = EarlyStopping(monitor='val_loss', patience=3)


# In[90]:


history = model.fit(xtest1, ytest, epochs=50, batch_size=500, verbose=1, callbacks=[callback], validation_split=0.2)


# In[91]:


plt.plot(history.history['loss'])
plt.plot(history.history['val_loss']) # model is overfitting


# # 2 dropouts and earlystopping

# In[111]:


model = Sequential([
    Dense(300, input_shape=(784,)), 
    Dropout(0.5),
    Activation('relu'),
    Dense(100),
    Dropout(0.5),
    Activation('relu'),
    Dense(10),
    Activation('softmax')
])


# In[112]:


model.compile(optimizer='adam', loss= 'sparse_categorical_crossentropy', metrics=['accuracy'])


# In[113]:


callback = EarlyStopping(monitor='val_loss', patience=3)


# In[114]:


history = model.fit(xtest1, ytest, epochs=50, batch_size=500, verbose=1, callbacks=[callback], validation_split=0.2)


# In[115]:


plt.plot(history.history['loss'])
plt.plot(history.history['val_loss']) # model is not overfitting!


# In[116]:


model.summary()


# In[ ]:




