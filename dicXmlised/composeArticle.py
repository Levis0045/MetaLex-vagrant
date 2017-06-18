#! usr/bin/env python
# coding: utf8

"""
    Implémentation de détection de composants  des articles.
 
    
    Usage:
    >>> from MetaLex.dicOcrText import *
    >>> findArticles()
"""

# ----Internal Modules------------------------------------------------------

import MetaLex

# ----External Modules------------------------------------------------------

import re, sys, codecs
from bs4 import BeautifulSoup

# -----Exported Functions-----------------------------------------------------

__all__ = ['findArticles', 'extractArticles']

# -----Global Variables-----------------------------------------------------

allforms    = {
               'forms'  : [u'.', u',', u'n.', u'adj.', u'v.', u'prép.', u'adv.', u'Adv.', u'loc.', u'm.', u'f.', u'Fig.', u'tr.', u'intr.'],
               'cats'   : [u'n.', u'adj.', u'v.', u'prép.', u'adv.', u'Adv.', u'loc.'],
               'genres' : [u'm.', u'f.', u'Fig.', u'tr.', u'intr.'],
               'flexs'  : [u'tr.', u'intr.']
               
            }


# ----------------------------------------------------------


def findArticles(textart, enhance=False) :

    deb, fin, cat, flex, wcpt  = False, False, False, False, False
    article     = u''
    allArticles = []
    wordlists   = re.split(r'(\s+)', textart)
    
    for i, word in enumerate(wordlists) :
        word = word.strip()
        if len(word) >= 1 :
            #print word
            if  word[-1] != u'.' and fin == False \
            and next(i, wordlists, 'entry')  and before(i, wordlists, 'entry'):
            #entry
                #print word
                deb, fin, cat, lex  = True, False, False, False
                article += word+u' '
            elif before(i, wordlists, 'var') and next(i, wordlists, 'var') and word[-1] != u'.' \
            and fin == False :
            #word flexion
                #print i, word
                fin, cat, flex, = True, False, False
                article += word+u' '
                #print article+'\n'
                article = u''
            elif word in allforms['cats']  :
            #category
                cat, flex, deb = True, True, False
                article += word+u' '
                #print article+'\n'
                #print word
            elif word in allforms['genres']  :
            #genre
                cat, flex, deb = True, True, False
                article += word+u' '
                #print article+'\n'
                #print word
            elif word in allforms['flexs'] :
            #flexion
                cat, flex, deb = True, True, False
                article += word+u' '
                #print article+'\n'
                #print word
            elif word[0] == u'[' :
            #phonetic
                cat, flex, deb = True, True, False
                article += word+u' '
                #print article+'\n'
                #print word
            elif before(i, wordlists, 'wordint') and word not in allforms['forms'] \
            and next(i, wordlists, 'wordint') :
            #word int
                deb, fin, cat, flex  = False, False, False, True
                article += word+u' '
                #print word
            elif next(i, wordlists, 'wordend')  and before(i, wordlists, 'wordend') \
            and word[-1] == u'.' :
            #mot de fin
                #print word
                fin, cat, flex, = True, False, False
                article += word+u' '
                #print article+'\n'
                article = u''
            else : 
                pass

apres = ''
avant = ''
def next(i, tab, typ) :
    word       = tab[i]
    nextpart   = tab[i+1:i+4]
    #print part
    if typ == 'entry' :
        for el in allforms['forms'] :
            if el in nextpart : return True
    if typ == 'wordint' :
        for el in nextpart :
            if re.search(r'(\S+)+', el, re.I) : return True
    if typ == 'wordend' :
        for el in allforms['forms'] :
            if el in nextpart : return True
    if typ == 'var' :
        if word[-1] == u',' :
            for el in allforms['cats'] :
                if el in nextpart : 
                    apres = el
                    print avant, word, apres
                    return True
        else : return False
    
def before(i, tab, typ) :
    word  = tab[i]
    if i >= 2 :
        previouspart  = tab[i-4:i-1]
        #print part
        if typ == 'entry' :
            for el in allforms['forms'] :
                if el in previouspart : return True
            for el in previouspart :
                if re.search(r'([a-zéèçêùàï.,]+)', el, re.I) : return True
        if typ == 'wordint' :
            for el in allforms['forms'] :
                if el in previouspart : return True
            for el in previouspart :
                if re.search(r'(\S+)', el, re.I) : return True
        if typ == 'wordend' :
            for el in allforms['forms'] :
                if el in previouspart : return True
            for el in previouspart :
                if re.search(r'(\S+)', el, re.I) : return True
        if typ == 'var' :
            if len(previouspart) >= 1 :
                if previouspart[0][-1] == u',' :
                    avant =  previouspart[0]
                    #print previouspart[0], word, apres
                    return True
                    
                
                
def extractArticles ():
    return False


