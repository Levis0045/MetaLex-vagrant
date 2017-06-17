#! usr/bin/env python
# coding: utf8

"""
    Implémentation de détection de composants  des articles.
 
    
    Usage:
    >>> from MetaLex.dicOcrText import *
    >>> composeArticle()
"""

# ----Internal Modules------------------------------------------------------

import MetaLex

# ----External Modules------------------------------------------------------

import re, sys, codecs
from bs4 import BeautifulSoup

# -----Exported Functions-----------------------------------------------------

__all__ = ['findArticles', 'extractArticles']

# -----Global Variables-----------------------------------------------------

forms    = [u'.', u',', u'n.', u'adj.', u'v.', u'prép.', u'adv.', u'Adv.', u'loc.', u'm.', u'f.', u'Fig.', u'tr.', u'intr.']


# ----------------------------------------------------------


def findArticles(textart, enhance=False) :

    cats    = [u'n.', u'adj.', u'v.', u'prép.', u'adv.', u'Adv.', u'loc.']
    genres  = [u'm.', u'f.', u'Fig.', u'tr.', u'intr.']
    flexs   = [u'tr.', u'intr.']
    deb, fin, cat, flex, wcpt  = False, False, False, False, False
    
    article     = u''
    allArticles = []
    wordlists   = re.split(r'(\s+)', textart)
    
    for i, word in enumerate(wordlists) :
        word = word.strip()
        if len(word) >= 1 :
            #print word
            if word not in cats and word not in genres \
            and word not in flexs and word[-1] != u'.' \
            and fin == False :
                print word
                deb, fin, cat  = True, False, False
                article += word+u' '
            elif word in genres or word in flexs :
                cat, flex, deb = True, True, False
                article += word+u' '
                #print article+'\n'
            elif word[-1] == u'.' and not next(i, wordlists) :
                #print word
                fin, cat, flex, = True, True, True
                article += word+u' '
                
            elif word[-1] == u'.' and next(i, wordlists) :
                #print word
                fin, cat, flex,  = True, True, True
                article += word+u' '
                #print article+'\n'
                article = u''
            
            else : 
                pass
    
    
def next(i, tab):
    search   = tab[i:i+4]
    for el in forms :
        if el in search :
            return True
    
def before(i, tab):
    if i >= 2 :
        search  = tab[i-3:i]
        for el in forms :
            if el in search :
                return True


def extractArticles ():
    return False


