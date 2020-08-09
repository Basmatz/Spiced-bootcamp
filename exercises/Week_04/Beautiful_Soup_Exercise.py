#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup


# #### Request the html document we are interested in and convert it to a string

# In[2]:


response = requests.get('https://www.spiced-academy.com/en/program/data-science')
response.status_code


# In[3]:


spiced_html = response.text
spiced_html


# In[4]:


type(spiced_html)


# #### Use this string to create a BeautifulSoup object

# In[13]:


spiced_soup = BeautifulSoup(spiced_html, 'html.parser')


# In[14]:


spiced_soup.body.find(class_='description').find(class_="mob-hidden").text


# In[15]:


spiced_soup.body.find(class_='description').h3.text


# In[16]:



spiced_soup.find_all(attrs={"class":"curriculum-mini-section"})[0]


# In[ ]:





# In[ ]:





# In[6]:


spiced_soup


# In[7]:


spiced_soup.body.find(class_='description').find(class_="mob-hidden").text


# In[8]:


spiced_soup.body.find(class_='description').h3


# In[9]:


spiced_soup.find_all(attrs={"class":"curriculum-mini-section"})


# #### Example of looking for Campuses on the Spiced website

# In[10]:


spiced_soup.find(class_="program-intro-panel text-container--simple").find('a')['href']


# In[11]:


#spiced_soup.find(attrs={"class":"program-intro-panel text-container--simple"})


# In[12]:


# Finding all the 'a' tags
for tag in spiced_soup.find_all('a'):
    print(tag.get_text())


# In[ ]:




