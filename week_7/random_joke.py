#!/usr/bin/env python
# coding: utf-8

# In[1]:


import slack
import pyjokes


# In[7]:


oauth_token='xoxb-1227345553298-1330257325860-jGwb5bwonFww8KDhhSV8l1oT'

client = slack.WebClient(token=oauth_token)
joke = pyjokes.get_joke()

response = client.chat_postMessage(channel='#random', text=f"Here is a Python joke: {joke}")


# In[ ]:




