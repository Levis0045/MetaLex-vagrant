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

__all__ = ['findArticles', 'formatArticles']

# -----Global Variables-----------------------------------------------------

allforms = {
               'forms'  : [u'.', u',', u'n.', u'adj.', u'v.', u'prép.', u'adv.', u'Adv.', u'loc.', u'm.', u'f.', u'Fig.', u'tr.', u'intr.', u'interj.', u'art.', u'Firm.'],
               'cats'   : [u'n.', u'adj.', u'v.', u'prép.', u'adv.', u'Adv.', u'loc.', u'interj.', u'art.'],
               'genres' : [u'm.', u'f.', u'Fig.', u'tr.', u'intr.'],
               'flexs'  : [u'tr.', u'intr.']
           }


# ----------------------------------------------------------

def findArticles(textart, enhance=False) :
    deb, fin, cat, flex, wcpt  = False, False, False, False, False
    article     = u''
    allArticles = []
    wordlists   = re.split(ur'(\s+)', textart.strip())
    
    for i, word in enumerate(wordlists) :
        word = word.strip()
        if len(word) >= 1 :
            if word[-1] != u'.' :
                article += word+' '
            elif word[-1] == u'.' and next(i, wordlists, u'wordend'):
                #print word+'*****'
                print article
                article = u''
            else : 
                article += word+' '
                
            
    
    

def findArticlesa(textart, enhance=False) :

    deb, fin, cat, flex, wcpt  = False, False, False, False, False
    article     = u''
    allArticles = []
    wordlists   = re.split(ur'(\s+)', textart.strip())
    
    for i, word in enumerate(wordlists) :
        word = word.strip()
        if len(word) >= 1 :
            #print word
            if  word[-1] != u'.' and fin == False \
            and next(i, wordlists, u'entry')  and before(i, wordlists, 'entry'):
            #entry
                #print word
                deb, fin, cat, lex  = True, False, False, False
                article += word+u' '
            elif before(i, wordlists, u'var') and next(i, wordlists, 'var') and word[-1] != u'.' \
            and fin == False :
            #word flexion
                #print i, word
                fin, cat, flex, = True, False, False
                article += word+u' '
                #print article+'\n'
                article = u''
            elif word in allforms[u'cats']  :
            #category
                cat, flex, deb = True, True, False
                article += word+u' '
                #print article+'\n'
                #print word
            elif word in allforms[u'genres']  :
            #genre
                cat, flex, deb = True, True, False
                article += word+u' '
                #print article+'\n'
                #print word
            elif word in allforms[u'flexs'] :
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
            elif before(i, wordlists, u'wordint') and word not in allforms['forms'] \
            and next(i, wordlists, u'wordint') :
            #word int
                deb, fin, cat, flex  = False, False, False, True
                article += word+u' '
                #print word
            elif next(i, wordlists, u'wordend')  and before(i, wordlists, 'wordend') \
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
    nextpart   = tab[i-1:i+5]
    #print '***',nextpart
    if typ == u'entry' :
        for el in allforms[u'forms'] :
            if el in nextpart : return True
    if typ == u'wordint' :
        for el in nextpart :
            if re.search(ur'(\S+)+', el, re.I) : return True
    if typ == u'wordend' :
        for el in allforms[u'cats'] :
            if el in nextpart : return True
    if typ == u'var' :
        if word[-1] == u',' :
            for el in allforms[u'cats'] :
                if el in nextpart : 
                    apres = el
                    #print avant, word, apres
                    return True
        else : return False
    
    
def before(i, tab, typ) :
    word  = tab[i]
    if i >= 2 :
        previouspart  = tab[i-5:i-1]
        print previouspart
        if typ == u'entry' :
            for el in allforms[u'forms'] :
                if el not in previouspart : return True
            for el in previouspart :
                if re.search(r'([a-zéèçêùàï.,]+)', el, re.I) : return True
        if typ == u'wordint' :
            for el in allforms[u'forms'] :
                if el in previouspart : return True
            for el in previouspart :
                if re.search(r'(\S+)', el, re.I) : return True
        if typ == u'wordend' :
            for el in allforms[u'forms'] :
                if el in previouspart : return True
            for el in previouspart :
                if re.search(r'(\S+)', el, re.I) : return True
        if typ == u'var' :
            if len(previouspart) >= 1 :
                if previouspart[0][-1] == u',' :
                    avant =  previouspart[0]
                    #print previouspart[0], word, apres
                    return True
                    
                
                
def formatArticles ():
    return False


