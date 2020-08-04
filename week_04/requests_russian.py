#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 11:42:58 2020

@author: stazhe
"""


import requests
import re




url = 'http://www.rockk.ru/viewpage.php?page_id=67'
kino =requests.get(url)

#check status code in order to assess whether request was successful
#print(kino.status_code)

#print(type(kino))
#help(kino)

#print(kino.text)

# Because the program deals with a page in cyrillic, we have to check the encoding 
# to make sure that the characters are read correctly. This is done by searching 
# for all instances of "charset" in the meta lines and isolating the name of the 
# encoding:



def find_charset(req):
    """
    Finds the encoding in the meta settings of a requested webpage and sets the encoding of it to it
    """
    charset = re.findall("<meta.+charset=(.+)(?='\s\/>)", req.text)
    req.encoding = charset[0]
    
    return req

find_charset(kino)   
#charset = re.findall("<meta.+charset=(.+)(?='\s\/>)", kino.text)
#print(charset)

# set the encoding to the correct one and save the webpage as a text file.
#kino.encoding = charset[0]


def make_textfile(name, filename):
    '''Makes a UTF-8 encoded text file with the same name from a request object'''
    with open(filename+'.txt', 'w', encoding="UTF8") as file:
        file.write(name.text)

make_textfile(kino, 'kino')    

# with open('kino.txt', 'w', encoding="UTF8") as file:
#     file.write(kino.text)
    
# Check that the characters have been rendered correctly:


def check_cyrillic (textfile):
    """
    Checks if a given file (extension .txt) contains a cyrillic vowel
    """
    with open(textfile, 'r') as file:
     
        contents =file.read()
        assert any(x in contents for x in ['а','е','ё','и','о','у'])
        return contents

contents = check_cyrillic('kino.txt')

# with open('kino.txt', 'r') as file:
 
#     contents =file.read()
#     assert 'д' in contents
#     # checks for a cyrillic character

#print(album_links)

def find_urls (contents, pattern):
    """
    Makes a dictionary of relevant links for a given page saved in a currently open text file
    
    Params:
    -------
    contents: the variable name of the file currently opened as file.read()
    pattern: the regular expression for the needed url 
    """
    links=re.findall(pattern, contents)
    urls = {pattern.split('=')[1]: 'http://www.rockk.ru/'+link for link in links}
    return urls

album_pattern = "(album\.php\?cat_id=\d*)"

album_urls = find_urls(contents, album_pattern)



# Next search for links to albums in the text:
#album_links=re.findall("(album\.php\?cat_id=\d\d\d)", contents)
#returns a list of album links.
#print(album_links)
#Next we make a dictionary of links for the songs on each album:
#album_urls = {str(link)[-3:]: 'http://www.rockk.ru/'+link for link in album_links}
#print(album_urls)

# For each url we make a new request:

def make_text_files (urls):
    for url in urls:
        request = requests.get(url)
   #    print(album.status_code) <-- optional check for errors in request
    
        find_charset(request)
        make_textfile(urls[url], str(urls[url]))
    
    
# for album_url in album_urls.values():
#     album = requests.get(album_url)
# #    print(album.status_code) <-- optional check for errors in request
    
#     find_charset(album)
    
#     with open(str(album_url)[-3:]+'.txt', 'w', encoding="UTF8") as file:
#         file.write(album.text)
    
# def find_song_urls(contents):
#     """
#     Finds the song URLs for an open album file currently opened
    
#     Params:
#     -------
#     contents is the variable name of the file currently opened as file.read()
    
#     """
#     song_links=re.findall("(text\.php\?readmore=\d*)", contents)
#     song_urls = {"song_"+str(link)[-4:]: 'http://www.rockk.ru/'+link for link in song_links}
#     return song_urls


song_pattern = "(text\.php\?readmore=\d*)"
print(album_urls)

# Make text files for all songs in an album:    
for album_key in album_urls:
    contents = check_cyrillic(str(album_key)+'.txt')
    song_urls = find_urls(contents, song_pattern)
    
    
    #contents = check_cyrillic(album_urls[album_key])
    #album_songs=find_song_urls(contents)
    print(album_urls[album_key])

