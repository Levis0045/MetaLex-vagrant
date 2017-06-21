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
from   composeArticle import *

# ----External Modules------------------------------------------------------

import re, sys, codecs
from   bs4 import BeautifulSoup
import os

# -----Exported Functions-----------------------------------------------------

__all__ = ['xmlised', 'dicoHtml']

# -----Global Variables-----------------------------------------------------


components = {
                u'xml' : {
                          u'metadata'       : [u'namespace', u'projectname', u'author', u'date', u'comment', u'contributors'],
                          u'identification' : [u'entry', u'flexion', u'category', u'gender', u'rection', u'phonetic'], 
                          u'treatment'      : [u'definition', u'contextualisation', u'figured', u'contrary']
                        },
                u'tei' : {
                          u'metadata'       : [],
                          u'identification' : [], 
                          u'treatment'      : []
                        },
                u'lmf' : {
                          u'metadata'       : [],
                          u'identification' : [], 
                          u'treatment'      : []
                        },
                u'dtd' : [u'ELEMENT', u'ATTRIBUTE', u'PCDATA', u'CDATA', u'REQUIRED', u'IMPLIED'],
                u'xsd' : []
             }

# ----------------------------------------------------------


def dataArticles(typ=u'pickle'):
    MetaLex.dicProject.createtemp()
    contentdir = os.listdir('.')
    filepickle = u''
    filetext   = u''
    for fil in contentdir :
        if fil.split('.')[1]   == u'pickle' :
            filepickle = fil 
        elif fil.split('.')[1] == u'art'    :
            filetext = fil
    if typ :
        datapickle = MetaLex.dicProject.fileUnpickle(filepickle)
        return datapickle
    if typ == u'text' :
        datatext = MetaLex.dicProject.fileGettext(filetext)
        return datatext



def xmlised(typ=u'xml') :
    data = dataArticles()
    print data
    
    
    
      
def buildStructure(data, typ=u'dtd'):
    return False




def dicoHtml(data) :
    
    return False
    
    
    
    