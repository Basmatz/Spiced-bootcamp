#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re


# In[2]:


pip install requests


# In[3]:


# Choose the URL to request it from.
url = 'https://www.lyrics.com/artist/Bruno-Mars/1107691'


# In[4]:


request = requests.get(url)


# In[5]:


request.status_code


# In[6]:


# It is a requests type
type(request)


# In[7]:


# requests.text will return the html file of the website as a string
print(request.text)


# In[8]:


pattern = '/lyric/\d+/Bruno\+Mars/[^/"]+'


# In[9]:


linklist1 = re.findall(pattern,request.text)


# In[10]:


print(linklist1)


# In[11]:


type(request.text)


# In[12]:


for index in range (len(linklist1)):
                    linklist1[index]= 'https://www.lyrics.com/'+ linklist1[index]


# In[13]:


for l in linklist1:
    print(l)


# In[14]:


for link in linklist1[:10]:
    url= link
    request = requests.get(url)
    print(request)
    print(request.text)
    


# In[15]:


for link in linklist1[:10]:
    url= link 
    request = requests.get(url)
    print(request)
    soup = BeautifulSoup(request.text)
    lyrics= soup.find(attrs={"id":"lyric-body-text"}).text
    print(lyrics)


# In[16]:


for link in linklist1[:10]:
    url= link 
    request = requests.get(url)
    print(request)
    soup = BeautifulSoup(request.text)
    lyrics= soup.find(attrs={"id":"lyric-body-text"}).text
    print(lyrics) 
    with open(f'/Users/dennyiva/desktop/Bruno_files/{link}', 'w') as file:
        file.write(lyrics)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


#Choosing the url for artist #2
url = 'https://www.lyrics.com/artist/Ray-Charles/3876'


# In[ ]:


request = requests.get(url)


# In[ ]:


request.status_code


# In[ ]:


type(request)


# In[ ]:


print(request.text)


# In[ ]:


pattern = '/lyric/\d+/Ray\+Charles/[^/"]+'


# In[ ]:


linklist = re.findall(pattern,request.text)


# In[ ]:


print(linklist)


# In[ ]:


type(request.text)


# In[ ]:


# make a loop with stringlist and for each of the elements do 3 things:


# In[ ]:


for l in linklist:
    print(l)


# In[ ]:


with open('RayCharles.txt', 'w') as file:
    file.write(request.text)


# In[ ]:


for index in range (len(linklist)):
                    linklist[index]= 'https://www.lyrics.com/'+ linklist[index]


# In[ ]:


for l in linklist:
    print(l)


# In[ ]:


for link in linklist[:10]:
    url= link
    request = requests.get(url)
    print(request)
    print(request.text)


# In[ ]:


for link in linklist[:10]:
    url= link 
    request = requests.get(url)
    print(request)
    soup = BeautifulSoup(request.text)
    lyrics= soup.find(attrs={"id":"lyric-body-text"}).text
    print(lyrics) 
    with open(f'/Users/dennyiva/desktop/Ray_files/{link}', 'w') as file:
        file.write(lyrics)
    


# In[ ]:


ls


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# STEP 2: response = request.get(full_url)
    
    # STep 3: response.text
    
    #Step 4: Grab the lyrics from the text (eg. regex, bs4)
    
    # Step 5: Once you grab the text, save the text to a file


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




