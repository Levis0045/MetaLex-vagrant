#! usr/bin/env python
# coding: utf8

"""
    Implémentation de détection de composants  des articles.
 
    Packages:
        >>> apt-get install python-html5lib
        >>> apt-get install python-lxml
        >>> apt-get install python-bs4
        
    Usage:
        >>> from MetaLex.dicOcrText import *
        >>> parseArticle()
        >>> structuredWithCodif()
        
"""

# ----Internal Modules------------------------------------------------------

from MetaLex    import codifications
from dicXmlTool import * 

# ----External Modules------------------------------------------------------

import re, sys, codecs
from bs4  import BeautifulSoup
from lxml import etree

# -----Exported Functions---------------------------------------------------

__all__ = ['parseArticle', 'structuredWithCodif']

# -----Global Variables-----------------------------------------------------

codi       = codifications.codificationsStore()
contentDic = codi.getAllCodifications()
textCodif  = codi.getCodifTextType()
symbCodif  = codi.getCodifSymbType()

# --------------------------------------------------------------------------

def parseArticle(textart) :
    codif=[u'text', u'symb', u'typo', u'graph']
    i, c = 0, 0
    p = parserCodification()
    resultext = p.procCodi(textart, i, c, codif, contentDic)
    return resultext


def buildReplaceCodif(codif, typ):
    for k, v in contentDic.items():
        if typ == u'text' and codif in v and k == typ :
            for i, t in textCodif.items() :
                if codif in t and i == u'cats' :
                    return u' <cte:cat>'+codif+u'</cte:cat> '
                if codif in t and i == u'genres' :
                    return u' <cte:genre>'+codif+u'</cte:genre> '
                if codif in t and i == u'marques' :
                    return u' <cte:marque>'+codif+u'</cte:marque> '
                if codif in t and i == u'varLings' :
                    return u' <cte:vLings>'+codif+u'</cte:vLings> '
                if codif in t and i == u'nombres' :
                    return u' <cte:nbre>'+codif+u'</cte:nbre> '
                if codif in t and i == u'rection' :
                    return u' <cte:rection>'+codif+u'</cte:rection> '
                if codif in t and i == u'affixe' :
                    return u' <cte:affixe>'+codif+u'</cte:affixe> '
        
        elif typ == u'symb' and codif in v and k == typ  :
            for i, t in symbCodif.items() :
                if codif in t and i == u'numbers' :
                    return u' <csy:nbre>'+codif+u'</cte:nbre> '
                if codif in t and i == u'alpha' :
                    return u' <cte:alpha>'+codif+u'</cte:alpha> '
                if codif in t and i == u'symbs' :
                    return u' <cte:syb>'+codif+u'</cte:syb> '
                
                
class parserCodification() :
    """
       
    """
    
    def __init__(self):
        self.result = u''
        self.codif = [u'text', u'symb', u'typo', u'graph']
          
    def procCodi(self, art, i, c, codif, codifs):
        num    = i
        codift = self.codif[c] 
        codi   = ' '+codifs[codift][num]+' '
        
        if  art.find(codi)  != -1 :
            #print '3'
            if codift == u'text' : replac = buildReplaceCodif(codifs[codift][num], u'text')
            if codift == u'graph': replac = u' <cgr>'+codifs[codift][num]+u'</cgr> '
            if codift == u'typo' : replac = u' <cty>'+codifs[codift][num]+u'</cty> '
            if codift == u'symb' : replac = buildReplaceCodif(codifs[codift][num], u'symb')
            artcodi = art.replace(codi, replac)
            self.result = artcodi
            num += 1
            if num < len(codifs[codift]) :
                #print '4', codifs[codift][num]
                self.procCodi(artcodi, num, c, self.codif, codifs)
            elif c < 3 :
                c = c + 1
                num = 0
                self.procCodi(artcodi, num, c, self.codif, codifs)
                #print artcodi, codif[c]
            if c == 3 and art == None :
                self.result = art
        else : 
            num += 1
            if num < len(codifs[codift]) :
                #print '6', codifs[codift][num]
                self.procCodi(art, num, c, self.codif, codifs)
            elif c < 3 :
                c = c + 1
                num = 0
                self.procCodi(art, num, c, self.codif, codifs)
            elif c == 3 and art == None :
                self.result =  art
        
        return self.result



class structuredWithCodif():
    """
       
    """
    
    def __init__(self, data, output):
        self.data         = data
        self.dataCodified = u''
        self.dataBalised  = u''
        self.output       = output
    
    
    def normalizeDataToCodif(self):
        contentall = {}
        for art in self.data.keys() :
            content = u''
            for word in re.split(ur' ', self.data[art]) :
                if word[-1] == u';' or word[-1] == u':' or word[-1] == u',':
                    word, caract = word[:-1], word[-1]
                    content += word+u' {0} '.format(caract)
                elif word[-1] == u'.' and word not in contentDic['text'] :
                    word, caract = word[:-1], word[-1]
                    content += word+u' {0} '.format(caract)
                elif word[0] == u'(' and word not in contentDic['symb'] :
                    print word, '----------------'
                    word, caract = word[:1], word[0]
                    content += word+u' {0} '.format(caract)
                elif word[-1] == u')' and word not in contentDic['symb'] :
                    print word, '----------------'
                    word, caract = word[:-1], word[-1]
                    content += word+u' {0} '.format(caract)
                else :
                    content += word +u' '
            contentall[art] = content
        return contentall
          
          
    def codifiedArticles(self):
        dataArticles = self.normalizeDataToCodif()
        datacodified = {}
        for art in dataArticles.keys() :
            artcodif = parseArticle(dataArticles[art])
            datacodified[art] = artcodif
        return datacodified
         
         
    def readTag(self, tag):
        elsearch = re.search(ur'<...>(.+)</...>', tag)
        elment   = elsearch.group(1)
        return elment
    
      
    def formatArticles(self):
        dataCodified  = self.codifiedArticles()
        treatArticles = {}
        for art in dataCodified.keys() :
            for partArt in dataCodified[art].split(' ') :
                
                
                
                return False
    
    
    

