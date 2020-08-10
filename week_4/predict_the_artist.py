#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline


# In[62]:


url= 'https://www.lyrics.com/artist/Sting/5536'
request= requests.get(url)


# In[63]:


request.status_code


# In[64]:


with open('Sting.txt' , 'w') as file:
    file.write(request.text)


# In[65]:


Sting_url_links= []

pattern = "/lyric/\d+/Sting/[^\"]+"
text= request.text


# In[66]:


Sting_songs = re.findall(pattern, text)


# In[67]:


Sting_songs


# In[68]:


for i in range(len(Sting_songs)):
    Sting_url_links.append('http://www.lyrics.com' +Sting_songs[i])


# In[69]:


len(Sting_url_links)


# In[70]:


Sting_url_links


# In[74]:


url2='https://www.lyrics.com/artist/Queen/5205'
request2= requests.get(url2)


# In[75]:


request2.status_code


# In[77]:


with open('Queen.txt', 'w') as file:
    file.write(request2.text)


# In[78]:


Queen_url_links=[]

pattern2 = "/lyric/\d+/Queen/[^\"]+"
text2= request2.text


# In[79]:


Queen_songs = re.findall(pattern2, text2)


# In[80]:


for i in range(len(Queen_songs)):
    Queen_url_links.append('http://www.lyrics.com' +Queen_songs[i])


# In[81]:


len(Queen_url_links)


# In[82]:


Queen_url_links


# In[83]:


bands = ['Sting','Queen']
for i in range(len(bands)):
    os.makedirs(os.path.join('C:\\Users\\Kriszta\\Desktop\\GitHub-Spiced\\logistic-lemongrass-student-code\\week_4', bands[i]))


# In[87]:


for i in range(len(Sting_url_links)):

    Sting_url=Sting_url_links[i]
    Sting_request =requests.get(Sting_url)

    pattern= "\/lyric\/.+\/.+\/(.+)$"
    with open("Sting/Sting--" + re.findall(pattern, Sting_url_links[i]) [0] + '.txt' , 'w') as file:
        Sting_soup_lyrics = BeautifulSoup(Sting_request.text)
        Sting_lyrics = Sting_soup_lyrics.pre.get_text()
        file.writelines(Sting_lyrics)
file.close()


# In[93]:


for i in range(len(Queen_url_links)):

    Queen_url=Queen_url_links[i]
    Queen_request =requests.get(Queen_url)

    pattern= "\/lyric\/.+\/.+\/(.+)$"
    with open("Queen/Queen--" + re.findall(pattern, Queen_url_links[i]) [0] + '.txt' , 'w') as file:
        Queen_soup_lyrics = BeautifulSoup(Queen_request.text)
        Queen_lyrics = Queen_soup_lyrics.pre.get_text()
        file.writelines(Queen_lyrics)
file.close()


# In[104]:


Sting_corpus= list()
for i in range(len(Sting_url_links)):
    with open("Sting/Sting--" + re.findall(pattern, Sting_url_links[i]) [0] + '.txt' , 'r') as file:
        doc= file.read()
        doc.lower()
        doc.split()
        file.close
        Sting_corpus.append(doc)


# In[106]:


Sting_label = ['Sting'] * len(Sting_corpus)
len(Sting_label)


# In[113]:


Sting_df= pd.DataFrame(list(zip(Sting_label,Sting_corpus )) , columns = ['bands', 'lyrics'])
Sting_df


# In[114]:


Queen_corpus= list()
for i in range(len(Queen_url_links)):
    with open("Queen/Queen--" + re.findall(pattern, Queen_url_links[i]) [0] + '.txt' , 'r') as file:
        doc= file.read()
        doc.lower()
        doc.split()
        file.close
        Queen_corpus.append(doc)


# In[115]:


Queen_label = ['Queen'] * len(Queen_corpus)
len(Queen_label)


# In[116]:


Queen_df= pd.DataFrame(list(zip(Queen_label,Queen_corpus )) , columns = ['bands', 'lyrics'])
Queen_df


# In[118]:


df = Sting_df.append(Queen_df, ignore_index=True)
df


# In[154]:


df = df.drop_duplicates( subset = 'lyrics')


# In[155]:


df


# In[204]:


df.groupby('bands').size()


# In[205]:


artist_1= 'Sting'
artist_2= 'Queen'


# In[206]:


labels = [artist_1]*313 + [artist_2]*275


# In[207]:


type(labels)


# In[208]:


len(labels)


# In[209]:


text_corpus = df['lyrics'].tolist()


# In[210]:


type(text_corpus)


# In[211]:


len(text_corpus)


# In[212]:


def train_model(text, labels):
    """
    Trains a scikit-learn classification model on text.

    Parameters
    ----------
    text : list
    labels : list

    Returns
    -------
    model : Trained scikit-learn model.

    """
    cv = CountVectorizer(stop_words='english')
    #here: balance the transformed numerical data
    tf = TfidfTransformer()
    nb = MultinomialNB(alpha = 1)
    model = make_pipeline(cv, tf, nb)
    model.fit(text, labels)

    return model


# In[213]:


def predict(model, new_text):
    """
    Takes the pre-trained model pipeline and predicts new artist based on unseen text.

    Parameters
    ----------
    model : Trained scikit-learn model pipeline.
    new_text : str

    Returns
    ---------
    prediction : str

    """
    new_text = [new_text]
    prediction = model.predict(new_text)
    probabilities = model.predict_proba(new_text)

    return prediction[0], probabilities


# In[ ]:
if __name__ == '__main__':

    model = train_model(text_corpus, labels)
    user_input = input('Please enter some text')

    predict(model, 'user_input')
    print('Here is your prediction')
    print('prediction')
