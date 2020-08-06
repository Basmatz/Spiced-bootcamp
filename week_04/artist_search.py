#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 12:40:02 2020

@author: stazhe
"""
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
from transliterate import translit, detect_language
only_a_tags = SoupStrainer("a")

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


    
artists_input = make_artists()

artist_catalogue = scrape_artists()

search_results_artists = search_results(artists_input, artist_catalogue)


