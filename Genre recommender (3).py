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

# In[142]:


def fill_genre(array, genre):
    if genre in array:
        return 1
    return 0


# In[145]:


genres = ['Film-Noir', 'Adventure', 'Children',
           'IMAX', 'Crime', 'Documentary', 'Fantasy', 'Musical', 'Romance',
           'Mystery', 'Thriller', 'Animation', 'Action', 'Comedy', 'War', 'Drama',
           'Western', 'Sci-Fi', 'Horror']


# In[146]:


for genre in genres: 
    df_movies[genre] = df_movies.genres.apply(fill_genre, genre)


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

