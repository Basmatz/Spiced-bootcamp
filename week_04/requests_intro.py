#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 11:02:23 2020

@author: stazhe
"""


import requests
import re




url = "https://www.lyrics.com/artist/Depeche-Mode/4071"
#url = 'http://www.rockk.ru/viewpage.php?page_id=67'
request =requests.get(url)
#rеquest.encoding = 'utf-8'

#check status code in order to assess whetherrequest was successful
print(request.status_code)

print(type(request))
help(request)

print(request.text)

#type(request.text)


with open('Depeche Mode.txt', 'w') as file:
    file.write(request.text)
    
