#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 17:21:43 2020

@author: stazhe
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 11:42:58 2020

@author: stazhe
"""


import requests
import re

def find_charset(req):
    """
    Finds the encoding in the meta settings of a requested webpage and sets the encoding of it to it
    """
    charset = re.findall("<meta.+charset=(.+)(?='\s\/>)", req.text)
    req.encoding = charset[0]
    
    return req

def make_textfile(name):
    '''Makes a UTF-8 encoded text file with the same name from a request object'''
    with open(str(name)+'.txt', 'w', encoding="UTF8") as file:
        file.write(name.text)

def check_cyrillic (textfile):
    """
    Checks if a given file (extension .txt) contains a cyrillic vowel
    """
    with open(textfile, 'r') as file:
     
        contents =file.read()
        assert any(x in contents for x in ['а','е','ё','и','о','у'])
        return contents
    
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

def make_text_files (urls):
    for url in urls:
        request = requests.get(url)
   #    print(album.status_code) <-- optional check for errors in request
    
        find_charset(request)
        make_textfile(urls[url])
    



url = 'http://www.rockk.ru/viewpage.php?page_id=67'

kino =requests.get(url)

# set the encoding to the correct one and save the webpage as a text file.
find_charset(kino)   

make_textfile(kino)   


# Check that the characters have been rendered correctly:
contents = check_cyrillic('kino.txt')

album_pattern = "(album\.php\?cat_id=\d*)"
song_pattern = "(text\.php\?readmore=\d*)"


 


#Find the album URLs:
album_urls = find_urls(contents, album_pattern)

#Make text files of each album page:
make_text_files(album_urls)

