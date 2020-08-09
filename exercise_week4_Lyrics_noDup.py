# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 10:32:46 2020

@author: Besitzer
"""
#find dupliacte song titles on lyrics.com

#
import os
import requests
import re
from bs4 import BeautifulSoup
#
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


#folder in to store data in home directory 
folder='lyrics'

def writeLyrics2File(dic,artist,songTitle,lyrics):
    '''
    writes text to file named songTitle
    '''
    print(artist) 
    if not os.path.exists(dic+'/'+artist): os.mkdir(dic+'/'+artist)   
    file = open(dic+'/'+artist+'/'+songTitle, 'w',encoding='utf-8')
    file.write(lyrics)
    file.close()
#
#
def getArtist(url):    
    pos1 = url.find('/',url.find('artist'))
    pos2 = url.find('/',pos1+1)    
    artist = url[pos1+1:pos2]    
    #substitute chars not in line 
    # with file naming convention (BUT NOT "-" by "_"     
    return (re.sub(r'\[a-zA-Z0-9_-]+','_', artist))



def cosineSim(lisSong):    
    tfcv = TfidfVectorizer()
    lyricVec = tfcv.fit_transform(lisSong)
    #
    for ls in lisSong:
        ls=re.sub(r'\W+','_', ls)
    return cosine_similarity(lyricVec)

def duplicateSongIndex(mat,tol=.7):
    index=[]
    k=1
    for j in range(mat.shape[1]):       
        for i in range(k,mat.shape[0]):  
            if mat[i,j]>tol:
                index.append(i)                
        k+=1    
    indexNoDup = [] 
    #get rid of duplicate index numbers
    [indexNoDup.append(x) for x in index if x not in indexNoDup]  
    return(indexNoDup)




if __name__=="__main__":   

    domain= 'http://www.lyrics.com'
    url = []
    #url.append('https://www.lyrics.com/artist/Wu-Tang-Clan/143661')
    #url.append ('https://www.lyrics.com/artist/Dilated-Peoples/393048')
    #url.append ('https://www.lyrics.com/artist/A-Tribe-Called-Quest/50081')
    #url.append('https://www.lyrics.com/artist/The-Pharcyde/21811')
    url.append ('https://www.lyrics.com/artist/KRS-One/92135')
    #url.append('https://www.lyrics.com/artist/Gang-Starr/41')
    #url.append('https://www.lyrics.com/artist/The-Roots/168531')   
    
    
    for u in url:
        res = requests.get(u)
        #print(res.status_code)        
        soup= BeautifulSoup(res.text,'lxml')
        artist = soup.find_all('h1')[0].text
        print(artist)   
        pattern ='\/lyric\/\d+\/'+artist.replace(' ','\+')+'\/[A-Za-z\+]+'
        songTitleLinks= []
        songTitle=[]
        for link in soup.find_all('a', href=True):
            if re.match(pattern, link['href']):
                songTitleLinks.append(link['href'])
                songTitle.append(link.contents[0])
               
        songMat = cosineSim(songTitle)
        dupIndex = duplicateSongIndex(songMat)
        print('Found %i duplicate song(s) for %s'%(len(dupIndex),artist))
        #        
        #delete duplicates from song title link list
        songTitleLinksNew=[]
        
        for i,stl in  enumerate(songTitleLinks):
            if not i in dupIndex:
                songTitleLinksNew.append(stl)
   
        #Test
        #print('cosine:' + str(round(songMat[340,2],2))+'  singTitles: ' +songTitle[340]+'  '+songTitle[2])
       
        

