from sqlalchemy import create_engine
from sklearn.decomposition import NMF
import pickle
from fuzzywuzzy import process
import pandas as pd
import numpy as np
import random

conn_string = 'postgres://postgres:postgres@localhost/movies100k'
db = create_engine(conn_string)

movies = pd.read_sql('select * from movies', db)
ratings = pd.read_sql('select * from ratings', db)

with open("films_serialized.txt", "rb") as fp:   # Unpickling
    choices = pickle.load(fp)

def NMF_recommender(user_ratings):

    joinedDF = pd.merge(movies,ratings, left_on = 'movieid' ,right_on ='movieid')

    df = joinedDF[['userid','title', 'rating']]


    df[df[['userid', 'title']].duplicated(keep = False)].sort_values(by = 'userid')
    df[['userid', 'title']].drop_duplicates()

    new_df = df.drop_duplicates(['userid', 'title'])

    R_true = new_df.pivot(index = 'userid', columns = 'title', values = 'rating')
    R_true.fillna(2.5, inplace = True)

    m = NMF(n_components=18, init='random', random_state=10)   # <-- the other dimension of P and Q; how many "genres"
    m.fit(R_true)

    P = m.components_
    Q = m.transform(R_true)

    user = pd.DataFrame(np.zeros(R_true.shape[1]))
    user = user.T

    user.columns = R_true.columns


    for film, rating in user_ratings.items():
        user[film] = rating

    user = np.array(user)
    profile = m.transform(user.reshape(1,-1))
    movies_for_user = np.dot(P.T,profile.T)
    recommendation = pd.DataFrame(movies_for_user)

    indices = recommendation.sort_values(by = 0, ascending = False).iloc[:5].index

    top_movies = R_true.columns[indices]

    return top_movies


def fuzzy_select(user_input_films):

   films = []

   for film in user_input_films:
       if film == '':
            continue
       films.append(process.extract(film, choices, limit=1)[0][0])

   return films
