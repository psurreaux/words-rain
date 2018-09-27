#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2,cookielib
import sys, unicodedata
from bs4 import BeautifulSoup
import pymongo as Pymongo
from pymongo import MongoClient

#header
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

database_user = "database_user"
database_pass = "database_pass"

#local configs
client = MongoClient('localhost', 27017)
db = client['data-base']

#extern configs
'''connection = MongoClient("ds888888.mlab.com", 00000)
db = connection["data-base"]
db.authenticate(database_user, database_pass)'''


randomWord = "https://www.palabrasaleatorias.com/palavras-aleatorias.php?fs=10&fs2=0&Submit=Nova+palavra"

def getWords(url,header):
    response = urllib2.Request(url, headers=header)
    the_page = urllib2.urlopen(response)
    page = the_page.read()
    
    #parsing
    soup = BeautifulSoup(page, 'html.parser')
    table_div = soup.find('table')
    table = table_div.find_all('div')


    words = []
    for div in table:
        word = div.text.strip()#strip() is used to remove starting and trailing
        word = word.encode('utf8')
        word = unicodedata.normalize('NFKD', word.decode('utf8')).encode('ASCII', 'ignore')
        auxWord = word.split(' ')
        if(len(auxWord) == 1):
            words.append(word)
    
    return words

def anagraming(word):
    global hdr
    url = ("https://www.wordplays.com/pt/anagram-solver/{}".encode('utf8').format(word)) 
    response = urllib2.Request(url, headers=hdr)
    the_page = urllib2.urlopen(response)
    page = the_page.read()


    soup = BeautifulSoup(page, 'html.parser')

    # Take out the <div> of name and get its value
    table_div = soup.find('div',attrs={'id':'wordwrap'}).find_all('div',attrs={'class':'word'})

    anagrams = []
    for div in table_div:
        word = div.text.strip()#strip() is used to remove starting and trailing
        word = word.encode('utf8')
        word = unicodedata.normalize('NFKD', word.decode('utf8')).encode('ASCII', 'ignore')
        auxWord = word.split(' ')
        if(len(auxWord) == 1):
            anagrams.append(word)
    return anagrams





words = getWords(randomWord,hdr)
content = {}

for item in words:
    anagramas = anagraming(item)
    content[item] = anagramas

for x in content.keys():
    if(len(x) > 4):
        
        dic = {'name':x.capitalize(),'anagrams':content[x]}
        try:
            db.words.insert(dic)
        except Pymongo.errors.DuplicateKeyError:
            continue
    else:
        print("{} nao atende aos requisitos : tam > 4 ".encode('utf8').format(x))
print content.keys()
