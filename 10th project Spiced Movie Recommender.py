#!/usr/bin/env python
# coding: utf-8

# In[27]:


import pandas as pd
import numpy as np
import tqdm
import seaborn as sns
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_distances, euclidean_distances
from sklearn.metrics import jaccard_score
from sklearn.metrics.pairwise import cosine_similarity


# In[28]:


df_movies = pd.read_csv('movies1.csv')


# In[29]:


df_movies


# In[30]:


df_ratings = pd.read_csv('ratings.csv')


# ### Cosine similarity for the first 2 movies

# In[31]:


df = df_ratings.loc[(df_ratings['movieId'] < 3)]


# In[33]:


df_r = df.pivot_table(values='rating', index='movieId', columns='userId')


# In[34]:


df_r


# In[35]:


df_r.fillna(3.75,inplace=True)


# In[36]:


df_r


# In[37]:


x = df_r.iloc[0] # movie Toy Story


# In[41]:


y = df_r.iloc[1] # movie Jumanji


# In[39]:


def cosim(vec1, vec2):
    num = np.dot(vec1, vec2)
    denom = np.sqrt(np.dot(vec1,vec1) * np.dot(vec2,vec2))
    return num / denom


# In[40]:


cosim(x, y) # cosine similarity between Toy Story and Jumanji


# ### Recommendation for 1 specific movie based on RATINGS

# In[25]:


# I choose 'Action' as genre to pick a movie
df_action = df_movies.loc[df_movies['genres'] == 'Action']


# In[26]:


df_action


# In[27]:


df_ratings


# In[28]:


# I merge the 'ratings' dataframe with the 'movies' dataframe 
df_ac = df_ratings.merge(df_action,on='movieId', how='left')


# In[29]:


df_ac = df_ac[df_ac['genres'] == 'Action']


# In[30]:


df_ac


# In[31]:


# MovieId set as rows, UserId as columns and I get all ratings by users for every action movie
df_ac = df_ac.pivot_table(values='rating', index='movieId', columns='userId')


# In[32]:


df_ac.fillna(3.75,inplace=True) # Every missing rating is filled with the value 3.75


# In[33]:


df_ac


# In[34]:


df_action[df_action['title'] == 'Double Impact (1991)'] # I get the movieId of a given movie


# In[35]:


df_ac.index.get_loc(4200) # i get the iloc position of the movie


# In[36]:


cosim = pd.DataFrame(cosine_similarity(df_ac))# I get the cosines of every action movie


# In[37]:


sns.heatmap(cosim) 


# In[124]:


double_impact_recommendations = cosim.iloc[15]


# In[125]:


double_impact_recommendations # I get the cosines of all movies with the movie I picked as a reference


# In[40]:


# I get the list ordered by cosine similarity with the movie we like
double_impact_recommendations_ordered = double_impact_recommendations.sort_values(ascending=False) 


# In[41]:


double_impact_recommendations_ordered


# In[42]:


# I get the first five movies with similar ratings
double_impact_recommendations_ordered_5 = double_impact_recommendations_ordered.iloc[0:6]


# In[43]:


double_impact_recommendations_ordered_5


# In[44]:


# I get the names of the recommended movies 
df_action.iloc[[33, 48, 37, 19, 47]]


# ### Recommendation for 1 specific movie based on GENRE

# ### Encoding 1 column for a given genre 

# In[45]:


# function to encode the movies where the genre 'Comedy' appears
def fill_comedy(array):
    if 'Comedy' in array:
        return 1
    else : 
        return 0


# In[121]:


df_movies['comedy'] = df_movies.genres.apply(fill_comedy)


# In[122]:


df_movies.head(10) # dataframe with a column giving information about movies including 'comedy' as genre


# ### Encoding columns with all genres

# In[4]:


# function to try to encode all genres
def fill_genre(array, genre):
    if genre in array:
        return 1
    return 0


# In[5]:


# list with all different genres
genres = ['Film-Noir', 'Adventure', 'Children',
           'IMAX', 'Crime', 'Documentary', 'Fantasy', 'Musical', 'Romance',
           'Mystery', 'Thriller', 'Animation', 'Action', 'Comedy', 'War', 'Drama',
           'Western', 'Sci-Fi', 'Horror']


# In[6]:


# column builder for all different genres and their relations as binary numbers with the movie selection
for genre in genres: 
    df_movies[genre] = df_movies.genres.apply(fill_genre, genre=genre)


# In[7]:


df_movies.head(10)


# In[8]:


# I drop the columns I dont need to build the cosine dataframe
df_genres = df_movies.drop(['title' , 'genres'] , axis='columns')


# In[9]:


df_genres.set_index('movieId', inplace=True)


# In[10]:


df_genres.head(10)


# In[11]:


cosim_genres = pd.DataFrame(cosine_similarity(df_genres))


# In[12]:


cosim_genres.head(10) # I get the dataframe with all cosine similarities related to movieId and genre


# In[16]:


df_movies.iloc[1000] # I pick 1 random movie, in this case Field of Dreams


# In[17]:


field_of_dreams_recommendations = cosim_genres.iloc[1000]


# In[18]:


field_of_dreams_recommendations # I get the list with the different cosine similarities with our movie


# In[19]:


field_of_dreams_recommendations_ordered = field_of_dreams_recommendations.sort_values(ascending=False) 


# In[20]:


# Cosine similarities get ordered to get the most similar movies by genre
field_of_dreams_recommendations_ordered


# In[21]:


# I get the first five movies with the most similar genre
field_of_dreams_ordered_5 = field_of_dreams_recommendations_ordered.iloc[0:6]


# In[25]:


# I get the names of the recommended movies all of them with the combination of "Children|Drama|Fantasy"
df_movies.iloc[[837, 1244, 671, 1800, 1000]]


# ### Label encoding for grouped genres

# In[41]:


df_movies['genres'] = df_movies['genres'].astype('category')


# In[43]:


df_movies['genres_code'] = df_movies['genres'].cat.codes


# In[47]:


df_movies[df_movies['title'] == 'No Game No Life: Zero (2017)']


# In[52]:


df_movies[df_movies['genres_code'] == 554].head(5)


# ### Cosine similaraties by movie genre combiantion

# In[50]:


df_genres = df_movies.pivot_table(values='genres_code', index='movieId', columns='genres')


# In[51]:


df_genres


# In[54]:


df_genres.fillna(1,inplace=True)


# In[55]:


cosim_genres = pd.DataFrame(cosine_similarity(df_genres))


# In[60]:


cosim_genres


# In[72]:


df_movies[df_movies['title'] == 'No Game No Life: Zero (2017)']


# In[74]:


df_genres.index.get_loc(193583) 


# In[76]:


No_game_recommendation = cosim_genres.iloc[9738]


# In[77]:


No_game_recommendation


# In[79]:


No_game_recommendation_ordered = No_game_recommendation.sort_values(ascending=False) 


# In[80]:


No_game_recommendation_ordered


# In[81]:


df_genres.iloc[[8999, 7368, 7199, 4558,]]


# In[82]:


df_movies.loc[df_movies['movieId'] == 139855]

