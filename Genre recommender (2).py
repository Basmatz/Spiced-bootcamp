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

# In[130]:


def fill_genre(array, genre):
    # i tried to include something defining genre like genre = [list with all genres] but it does not work
    # i tried different combination of 'genre' but nothing works
    if genre in array:
        return 1
    return 0


# In[126]:


for genre in df_movies.genres: 
    df_movies[genre] = df_movies.genres.apply(fill_genre, genre)
# it seems genre has to be defined or identified but I am not sure how to do it


# In[127]:


df_movies.head(10) 
# this dataframe comes from calculating the fill_genre funcion only with array (fill_genre(array))
# I could use this dataframe but I must delete all columns with more than 1 element (all columns as lists) but I dont know
# how to implement that


# In[129]:


df_genres = df_movies['comedy'] + df_movies['Comedy'] + df_movies['movieId']
# here I tried to add just the columns with 1 genre to create a dataframe with the desired columns, didnt have time to finish it


# In[121]:


df_genres

