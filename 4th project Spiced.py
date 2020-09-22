#!/usr/bin/env python
# coding: utf-8

# In[42]:


import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re


# In[20]:


response = requests.get('https://www.lyrics.com/lyric/36263069/Iron+Maiden/2+Minutes+to+Midnight') # got the song URL from lyrics.com


# In[21]:


response.status_code # check that the status is OK


# In[22]:


iron_maiden = response.text # getting the html website as a full text


# In[23]:


iron_maiden


# In[24]:


iron_maiden = BeautifulSoup(iron_maiden) # getting extracted the lyrics out of the full Html file with BeautifulSoup


# In[25]:


iron_maiden


# In[26]:


# lets look for the song lyrics within all the html text. I should look for the tags "pre" or "p" belonging to preformatted texts


# In[27]:


iron_maiden.find_all('pre')


# In[12]:


iron_maiden.find(class_='lyric-body') # another option to extract the lyrics from the chaotic html is to use "class=lyric-body"


# In[29]:


iron_maiden_2m = iron_maiden.find(class_='lyric-body').text # html converted into a text


# In[30]:


iron_maiden_2m


# In[201]:


type(iron_maiden_2m) # data type of the text as a STRING


# In[13]:


iron_maiden1 = iron_maiden.find(class_='lyric-body').text.split(',') # getting transformed the STRING into a LIST with the split function


# In[31]:


type(iron_maiden1) # data type of the text as a LIST


# ### Word prediction with distribution and sequence applied to a music company assessing lyrics of a band

# In[77]:


# there is a possible application of the generate_word_distribution and text_generation function in order to check the probability  
# of harsh language for parental advisory lyrics or "key words" that may incite ilegal activities.


# In[44]:


def generate_word_distribution(song): 
   
    text = iron_maiden1
    all_data = ' '.join([' '.join(re.findall('(?u)\\b\\w\\w+\\b',article.lower())) for article in text]).split()
    words = pd.DataFrame({'words':all_data})
    words['next_words'] = words['words'].shift(-1)
    word_distribution = words.groupby('words')['next_words'].value_counts(normalize=True)
    
    return word_distribution


# In[78]:


text = iron_maiden1 # this is the song to be assessed, that underwent before all the scraping and parsing processes


# In[79]:


type(text) # song must be a list in order to work with the words and function


# In[80]:


all_data = ' '.join([' '.join(re.findall('(?u)\\b\\w\\w+\\b',article.lower())) for article in text]).split() 
# words are split into a list


# In[38]:


type(all_data)


# In[210]:


all_data


# In[43]:


words = pd.DataFrame({'words':all_data}) # words list is converted into a dataframe


# In[81]:


words['next_words'] = words['words'].shift(-1) # column of "next words" is added to work with the distribution


# In[83]:


generate_word_distribution(iron_maiden1) # distribution of probabilities for the next words within each individual word within the lyrics


# In[50]:


distribution = generate_word_distribution(iron_maiden1)


# In[87]:


def text_generation(seed, length, distribution): # definition of the text generation function with the seed interpreted by the music company "X" as a "key word" 
       
    try:
        seed = seed.lower()
        for i in range(length):
             seed += ' ' + np.random.choice(distribution[seed.split()[-1]].index, p=distribution[seed.split()[-1]].values)
        return seed
    
    except:
        print('Oops! Try another seed')
        return None


# In[88]:


# it is assumed that the recording company has data stored showing that some "key-words" are followed by harsh language or
# messages inciting illegal activities such as violence, rape or drug consumption.


# In[264]:


text_generation('kill', 20, distribution) # we can test different words based on the distribution to check if harsh language is used on the lyrics 


# ### Vectorization with same application as above

# In[151]:


from sklearn.feature_extraction.text import CountVectorizer


# In[167]:


iron_maiden1


# In[171]:


iron_maiden1[7]


# In[168]:


len(iron_maiden1) 


# In[206]:


cv = CountVectorizer()


# In[207]:


cv.fit(iron_maiden1)


# In[214]:


vec_iron_maiden1 = cv.transform(iron_maiden1)


# In[221]:


vec_iron_maiden1


# In[222]:


df = pd.DataFrame(vec_iron_maiden1.todense(), columns=cv.get_feature_names())


# In[223]:


df # dataframe showing the repetion of the words


# In[261]:


df['war'].sum() # we can look for repetion of words that may be harsh or susceptible to promote ilegal activities


# In[256]:


df.loc[:, ['war']] # paragraphs were the word is located can be spotted an later examined to extract information on the context 
# for that word


# In[237]:


df.describe()

