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

import re, sys, codecs, os
from bs4    import BeautifulSoup
from random import sample

# -----Exported Functions-----------------------------------------------------

__all__ = ['xmlised', 'dicoHtml']

# -----Global Variables-----------------------------------------------------


components = {
                u'xml'  :   {
                              u'metadata'       : [u'projectname', u'author', u'date', u'comment', u'contributors'],
                              u'identification' : [u'article', u'entry', u'flexion', u'category', u'gender', u'rection', u'phonetic'], 
                              u'treatment'      : [u'definition', u'contextualisation', u'figured', u'contrary']
                            },
                u'tei'  :   {
                              u'metadata'       : [],
                              u'identification' : [], 
                              u'treatment'      : []
                            },
                u'lmf'  :   {
                              u'metadata'       : [],
                              u'identification' : [], 
                              u'treatment'      : []
                            },
                u'dtd'  :   [u'ELEMENT', u'ATTRIBUTE', u'PCDATA', u'CDATA', u'REQUIRED', u'IMPLIED'],
                u'xsd'  :   [],
                u'forms':   {
                             u'allfs'  : [u'.', u',', u'n.', u'adj.', u'v.', u'prép.', u'adv.', u'Adv.', u'loc.', u'm.', u'f.', u'Fig.', u'tr.', u'intr.', u'interj.', u'art.'],
                             u'cats'   : [u'n.', u'adj.', u'v.', u'prép.', u'adv.', u'Adv.', u'loc.', u'interj.', u'art.'],
                             u'genres' : [u'm.', u'f.', u'Fig.', u'tr.', u'intr.'],
                             u'flexs'  : [u'tr.', u'intr.']
                            },
                u'codif':   {
                             u'text'   : [u'n.', u'adj.', u'v.', u'prép.', u'adv.', u'Adv.', u'loc.', u'm.', u'f.', u'Fig.', u'tr.', u'intr.', u'interj.', u'art.'],
                             u'graph'  : [u'.', u',', u':', u'-', u';'],
                             u'symb'   : [u'||', u'&#9830;', u'-', u'1.',u'2.',u'3.',u'4.',u'5.',u'6.',u'7.',u'8.',u'9.',u'a)',u'b)',u'c)',u'd)',u'e)',u'f)',u'g)',u'a.'],
                             u'typo'   : [u'I', u'G', u'B', u'P', u'']
                            }
             }

article = []
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



def xmlised(typ=u'xml', edit=True) :
    soup = BeautifulSoup(xmlMetadata(), "lxml")
    data = dataArticles()
    for dicart in data :
        for art in dicart.keys() :
            for cat in components[u'forms'][u'allfs']: 
                if dicart[art].find(cat) :
                    print balise(dicart[art], 'article'), ' \n'
    print soup.prettify()
        #findArticles(art, enhance=True)
    

def xmlMetadata(typ=u'xml'):
    MetaLex.dicProject.createtemp()
    if typ == u'xml' :
        projectconf = MetaLex.dicProject.readConf()
        author      = balise(projectconf['Author'], 'mtl:author', typ=u'')
        name        = balise(projectconf['Projectname'], 'mtl:projectname', typ=u'')
        date        = balise(projectconf['Creationdate'], 'mtl:date', typ=u'')
        comment     = balise(projectconf['Comment'], 'mtl:comment', typ=u'')
        contribtab  = projectconf['Contributors'].split(u',') if projectconf['Contributors'].find(',') else projectconf['Contributors']
        contrib = ''
        if len(contribtab) > 1 :
            for data in contribtab :
                contrib += balise(data, 'mtl:pers', typ=u'') 
        else :
            contrib = balise(''.join(contribtab), 'mtl:pers ', typ=u'') 
        contrib = balise(contrib, 'mtl:contributors', typ=u'')
        cont    = name+author+date+comment+contrib
        content = balise(cont, 'mtl:metadata', typ=u'') 
        return content
        
        
def xmlContent(): 
    
    
    
    
      
def buildStructure(data, typ=u'dtd'):
    return False



def dicoHtml(data) :
    
    return False
    
    
def balise(element, markup, typ=u'xml'):
    if type :
        if markup in components[u'xml'][u'identification'] \
        or components[u'xml'][u'treatment'] :
            element = chevron(markup)+element+chevron(markup, False)
            return element
    elif typ == u'tei' :
        if markup in components[u'tei'][u'identification'] \
        or components[u'xml'][u'treatment'] :
            element = chevron(markup)+element+chevron(markup, False)
            return element
    elif typ == u'lmf' :
        if markup in components[u'lmf'][u'identification'] \
        or components[u'xml'][u'treatment'] :
            element = chevron(markup)+element+chevron(markup, False)
            return element
    else :
        element = chevron(markup)+element+chevron(markup, False)
        return element
    

    
def generateMetadata():
    return False


    
def chevron(el, open=True, art=False):
    id = generateID()
    if art :
        if open : return u"<"+el+u" id='"+id+u"'"+u">"
        if not open : return u"</"+el+u">"
    else :
        if open : return u"<"+el+u">"
        if not open : return u"</"+el+u">"
    
    
def generateID():
    id = sample([u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9',u'0',u'a',u'b',u'c',u'd',u'e',u'f',u'g',u'h',u'i',u'j',u'k',u'l',u'm',u'n',u'o',u'p',u'q',u'r',u's',u't',u'v',u'w',u'y',u'z'], k=5)
    return u''.join(id)
    
    
    
    