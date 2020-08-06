#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 19:49:37 2020

@author: stazhe
"""


import requests
import re
from bs4 import BeautifulSoup
from bs4 import SoupStrainer#Import os module
import os
import fnmatch

only_a_tags = SoupStrainer("a")


def find_links(url, keyword):
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
    list_of_links=[]
    req=requests.get(url)
    req_soup_a = BeautifulSoup(req.content, "lxml", parse_only=only_a_tags)
    relevant_items = req_soup_a.find_all("a", href=lambda href: href and keyword in href)
    for item in relevant_items:
         if keyword in item.get('href'):
               list_of_links.append("http://www.rockk.ru/"+item.get('href'))
    return list_of_links           
    
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
       
def get_song_lyrics(url):
    """
    Finds song lyrics from a given url. Takes the first instance in case multiple lyrics are present.
    

    Parameters
    ----------
    url : url of lyrics page of the required song
    """
    song = requests.get(url)
    song_soup = BeautifulSoup(song.content, 'lxml').find(class_='main-body')
    lyrics = song_soup.text
    return lyrics

def get_song_title(url, artistname):
    """
    Returns song title for URL of song
    """
    song = requests.get(url)
    song_soup = BeautifulSoup(song.content, 'lxml').find('td', {'class' :'news-capmain'}).find('strong')
    title = artistname + ": " + song_soup.text
    return title

def remove_chords(lyrics):
    """Removes chord progression lines from lyrics block by searching for lines containing A-H and removing them"""
    lines = lyrics.split("\n")
    for line in lines:
        if re.search("[A-H]", line):
            lines.remove(line)
    new_lyrics="\n".join(lines)
    return new_lyrics

def write_lyrics_to_text(title, lyrics):
    """
    Makes a text file of given lyrics with a given title
    """
    with open(title+'.txt', 'w', encoding="UTF8") as file:
            file.write(lyrics)
            
def find_links_text(text, keyword):
    """
    Makes a list of links containing a relevant keyword in a given piece of text

    Parameters
    ----------
    text
        
    keyword : string
        keyword common to the needed links

    listname: name of list for links to be appended to
    
    Returns
    -------
    List of URLs of the requested links

    """
    list_of_links=[]
    text_soup_a = BeautifulSoup(text, "lxml", parse_only=only_a_tags)
    relevant_items = text_soup_a.find_all("a", href=lambda href: href and keyword in href)
    for item in relevant_items:
         if keyword in item.get('href'):
               list_of_links.append("http://www.rockk.ru/"+item.get('href'))
    return list_of_links           

# First for one artist:

url = 'http://www.rockk.ru/viewpage.php?page_id=67'
artistname = BeautifulSoup(requests.get(url).content, 'lxml').title.string.split(" - ")[0]

# Make text files of links to songs:

albumslist = find_links(url, "album.php")

make_text_files(albumslist, 'readmore')

      
# Cycle through list of albums and for each one extract the URLs and make text files of the lyrics they link to            

for album in albumslist:     
    album_num = album.split('=')[1]
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, str(album_num)+("*")):
            with open(file, 'r') as textfile:
                contents =textfile.read()                
    song_urls = find_links_text(contents, 'readmore')
    
    for song in song_urls:
        title = get_song_title(song, artistname)
        lyrics = get_song_lyrics(song)
        lyrics = remove_chords(lyrics)
        write_lyrics_to_text(title, lyrics)       
            