#!/usr/bin/env python
# coding: utf-8

# ####
# Build a text classification model to predict the artist from a piece of text.
# 
# -Download HTML pages
# -Get a list of song urls
# -Extract lyrics from song urls
# -Convert text to numbers by applying the Bag Of Words method
# -Build and train a Naive Bayes classifier
# -Balance out your dataset
# -Write a command-line interface
# -Give a 5-minute lightning talk by the end of the week

# In[1]:


import requests
import re
from bs4 import BeautifulSoup


# #Download HTML pages

# In[2]:


# Choose the URL to request it from.
url = 'https://www.lyrics.com/artist/Bruno-Mars/1107691'


# In[3]:


request = requests.get(url)


# In[4]:


request.status_code


# In[5]:


# It is a requests type
type(request)


# In[6]:


# requests.text will return the html file of the website as a string
type(request.text)


# In[7]:


# Save the html in a txt file and search in an editor
with open('Bruno_files.txt', 'w') as file:
    file.write(request.text)
    
    
    
    


# ####Find and save all links for lyrics

# In[8]:


# with regular expressions:


# In[9]:


text = request.text


# In[10]:


pattern = "/lyric/\d+/Bruno-Mars/[A-Za-z+%\d+]+"


# In[11]:


re.findall(pattern, text, re.IGNORECASE)


# ####with beautifulSoup

# In[12]:


Bruno_soup = BeautifulSoup(text, 'html.parser')


# In[13]:


Bruno_soup.body.find_all(class_='tal qx')


# In[14]:


Bruno_soup.find(class_='tal qx').find('a')['href']


# In[15]:


links = []

for td in Bruno_soup.find_all('td'):
    if "tal" in td.get('class',[]):
          links.append('https://www.lyrics.com' + td.find('a')['href'])


# In[16]:


len(links)


# In[17]:


links[4:10]


# In[25]:


#Loop for all lyric files

for i in range(len(links)):
    temp_url = links[i]
    title = temp_url.split('/')[-1]
    print(i)
    
    temp_req = requests.get(temp_url)

    with open("/Users/dennyiva/desktop/spicedacademy/Bruno_lyrics/" + title + '.txt',  'w') as file:
        file.write(temp_req.text)


# In[27]:


# test on one song:

with open("/Users/dennyiva/desktop/spicedacademy/Bruno_lyrics/Billionaire.txt") as reader:
        songfile = reader.read()
        reader.close()


# In[28]:


type


# In[29]:


song_soup = BeautifulSoup(songfile, 'html.parser')


# In[30]:


lyrics = song_soup.pre.get_text()


# In[31]:


lyrics


# In[33]:


corpus = []


# In[ ]:





# In[ ]:




