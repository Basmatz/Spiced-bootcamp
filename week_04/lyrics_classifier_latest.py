#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 15:09:44 2020

@author: stazhe
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 12:40:02 2020

@author: stazhe
"""
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
only_a_tags = SoupStrainer("a")

import requests
from transliterate import translit, detect_language
import re
import os
import fnmatch

import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity


from spacy.lang.ru import Russian
from spacy_russian_tokenizer import RussianTokenizer, MERGE_PATTERNS


def transliterate_list(items):
    """Transliterates the latin inputs in a list to russian, returns list of russian. 
    
    Params: items: a list of strings each either latin or russian cyrillic, cannot be mixed
    
    Returns: same list but the english inputs have been transliterated
    """
    newitems = []
    for item in items:
       if detect_language(item) == "ru":
           newitems.append(item)
       else:
           ru_item = translit(item, 'ru')
           newitems.append(ru_item)
    return newitems
        

def make_artists():
    """
    Makes a list of strings as input by the user and transliterates them to 
    russian if input in latin alphabet

    Returns
    -------
    artists : list of inputs in russian 

    """
    artists = []
    while True:
        text_input = input ("Please enter an artist to search for, type 'end' to finish:\n\n")
        if text_input == "end":
            break
        else: artists.append(text_input)
    return transliterate_list(artists)


def scrape_artists():
    """
    Scrapes all artists on rockk.ru and returns a dictionary of names and links for the artists

    Returns
    -------
   dictionary with artist names as keys and urls as values

    """
    url = "http://rockk.ru/"
    url_soup = BeautifulSoup(requests.get(url).content, 'lxml')
    all_links = url_soup.find_all(class_="side")
    
    artist_catalogue = {}
    
    for link in all_links:
    
        artist_name = link.contents[0]
        artist_url = "http://www.rockk.ru/"+link.get('href')
    
        artist_catalogue[artist_name] = artist_url
    return(artist_catalogue)

def search_results(input_list, input_dict):
    """
    Returns dctionary of search results from index dictionary

    Parameters
    ----------
    input_list : list of strings to search for
        
    input_dict : dictionary to search through
        

    Returns
    -------
    output_dict : dictionary of matching key-value pairs 
    (keys are the list items that match keys in the input dictionary )

    """
    output_dict = {}
    for item in input_list:
        item_result = next((value for dict_key, value in input_dict.items() if dict_key.lower() == item.lower()), None)
        output_dict[item]=item_result
    return output_dict

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





    
artists_input = make_artists()

artist_catalogue = scrape_artists()

search_results_artists = search_results(artists_input, artist_catalogue)

for artist in search_results_artists:
    url = search_results_artists[artist]
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
                
    
