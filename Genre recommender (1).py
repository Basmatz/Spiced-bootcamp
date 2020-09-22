#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df_movies = pd.read_csv('movies1.csv')


# ### Encoding 1 element

# In[ ]:


def fill_comedy(array):
    if 'Comedy' in array:
        return 1
    return 0


# In[29]:


df_movies['comedy'] = df_movies.genres.apply(fill_comedy)


# In[30]:


df_movies.head(10)


# ### Encoding all genres

# In[114]:


def fill_genre(array, genre):
    genre = 'Adventure' 
    if genre in array:
        return 1
    return 0


# In[117]:



    df_movies[genre] = df_movies.genres.apply(fill_genre, genre)


# In[76]:


df_movies.head(10)


# In[120]:


df_genres = df_movies['comedy'] + df_movies['Comedy'] + df_movies['movieId']


# In[121]:


df_genres

