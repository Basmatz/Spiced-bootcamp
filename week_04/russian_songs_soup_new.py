#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 19:49:37 2020

@author: stazhe
"""


import requests
import re
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

only_a_tags = SoupStrainer("a")


def find_links(url, keyword, listname):
    """
    Makes a list of links containing a relevant keyword in a given URL

    Parameters
    ----------
    url : a URL that can be passed to requests
        
    keyword : string
        keyword common to the needed links

    listname: name of list for links to be appended to
    
    Returns
    -------
    List of URLs of the requested links

    """
    req=requests.get(url)
    req_soup_a = BeautifulSoup(req.content, "lxml", parse_only=only_a_tags)
    relevant_items = req_soup_a.find_all("a", href=lambda href: href and keyword in href)
    for item in relevant_items:
         if keyword in item.get('href'):
               listname.append("http://www.rockk.ru/"+item.get('href'))


def make_text_files(list_of_links, keyword):
    """Makes a text file from every link in a list
    Parameters:
    -----------
    list_of_links : a list containing links ending in = followed by an ID
    keyword : a key filtering all the relevant links, str
    """
    for link in list_of_links:
        
        #Request the webpage
        req=requests.get(link)
        
        #Name is the unique digit ID plus album name/song name
        name = str(link).split("=")[1]
        name+=BeautifulSoup(req.content, 'lxml').title.string.split('-')[-1].replace(" ", "_")
      
        #Parse the links in it with bs4
        req_soup_a = BeautifulSoup(req.content, 'lxml', parse_only=only_a_tags)
        #Filters the links on the page by ones containing the keyword
        relevant_items = req_soup_a.find_all("a", href=lambda href: href and keyword in href)
        
        with open(name+'.txt', 'w', encoding="UTF8") as file:
            file.write(str(relevant_items))
       

# First for one artist:

url = 'http://www.rockk.ru/viewpage.php?page_id=67'


# Pipeline to make text files of links to songs:
albumslist=[]

find_links(url, "album.php", albumslist)

make_text_files(albumslist, 'readmore')

print(albumslist)
#This results in a text file for each album containing the links to the songs






