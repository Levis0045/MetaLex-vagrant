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
graphCodif = codi.getCodifGraphType()

# --------------------------------------------------------------------------

def parseArticle(textart) :
    """
      Generate results from Parser codifications types
      @param:  textart:str
      @return: dict:resultext
    """
    codif=[u'text', u'symb', u'typo', u'graph']
    i, c = 0, 0
    p = parserCodification()
    resultext = p.procCodi(textart, i, c, codif, contentDic)
    return resultext


def buildReplaceCodif(codif, typ):
    """
      Make balise to codifications types 
      @param  codif:str
      @param   type:str
      @return: str:balise codification type
    """
    for k, v in contentDic.items():
        if typ == u'text' and codif in v and k == typ :
            for i, t in textCodif.items() :
                if codif in t and i == u'cats'    : return u' <cte-cat>'+codif+u'</cte-cat> '
                if codif in t and i == u'genres'  : return u' <cte-genre>'+codif+u'</cte-genre> '
                if codif in t and i == u'marques' : return u' <cte-marque>'+codif+u'</cte-marque> '
                if codif in t and i == u'varLings': return u' <cte-vLings>'+codif+u'</cte-vLings> '
                if codif in t and i == u'nombres' : return u' <cte-chif>'+codif+u'</cte-chif> '
                if codif in t and i == u'rection' : return u' <cte-rection>'+codif+u'</cte-rection> '
                if codif in t and i == u'affixe'  : return u' <cte-affixe>'+codif+u'</cte-affixe> '
        
        elif typ == u'symb' and codif in v and k == typ  :
            for i, t in symbCodif.items() :
                if codif in t and i == u'numbers' : return u' <csy-chif>'+codif+u'</cte-chif> '
                if codif in t and i == u'alpha'   : return u' <cte-alpha>'+codif+u'</cte-alpha> '
                if codif in t and i == u'symbs'   : return u' <cte-syb>'+codif+u'</cte-syb> '
        
        elif typ == u'graph' and codif in v and k == typ  :
            for i, t in graphCodif.items() :
                if codif == t and i == u'point'    : return u' <cgr-pt>'+codif+u'</cgr-pt> '
                if codif == t and i == u'virgule'  : return u' <cgr-vrg>'+codif+u'</cgr-vrg> '
                if codif == t and i == u'pointv'   : return u' <cgr-ptvrg>'+codif+u'</cgr-ptvrg> '
                if codif == t and i == u'dpoint'   : return u' <cgr-dpt>'+codif+u'</cgr-dpt> '
                if codif == t and i == u'ocrochet' : return u' <cgr-ocrh>'+codif+u'</cgr-ocrh> '
                if codif == t and i == u'fcrochet' : return u' <cgr-fcrh>'+codif+u'</cgr-fcrh> '
                if codif == t and i == u'opara'    : return u' <cgr-opar>'+codif+u'</cgr-opar> '
                if codif == t and i == u'fpara'    : return u' <cgr-fpar>'+codif+u'</cgr-fpar> '
                
                
class parserCodification() :
    """
      Parse data article with all type of dictionaries codification
      @return: dict:resultext
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
            if codift == u'graph': replac = buildReplaceCodif(codifs[codift][num], u'graph')
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
      Extract all single article from date articles codified
      @return: dict:contentall
    """
    
    def __init__(self, data, output):
        self.data          = data
        self.dataCodified  = u''
        self.dataBalised   = u''
        self.output        = output
        self.treatArticles = []
    
    def normalizeDataToCodif(self):
        """
          Extract all single article from date articles codified
          @return: dict:contentall
        """
        contentall = {}
        for art in self.data.keys() :
            content = u''
            for word in re.split(ur' ', self.data[art]) :
                word = word.strip() 
                if word[-1] == u';' or word[-1] == u':' or word[-1] == u',':
                    word, caract = word[:-1], word[-1]
                    content += word+u' {0} '.format(caract)
                elif len(word)> 2 and word[-1] == u'.' and word[0] != u'(' and word[-2] != u')' and word not in contentDic['text'] :
                    word, caract = word[:-1], word[-1]
                    content += word+u' {0} '.format(caract)
                elif word[0]  == u'('  and word not in contentDic['symb'] :
                    #print word, '----------------'
                    word, caract = word[1:], word[0]
                    content += caract+u' {0} '.format(word)
                elif len(word)> 2 and word[-1] == u'.' and word[-2] == u')' and word not in contentDic['symb'] :
                    #print word, word[-2],'----------------'
                    word, caract, point = word[:-2], word[-2], word[-1]
                    content += word+u' {0} {1} '.format(caract, point)
                elif len(word)> 2 and word[0] == u'[' and word[-1] == u']' and word not in contentDic['symb'] :
                    #print word, word[-2],'----------------'
                    word, caract1, caract2 = word[1:-1], word[0], word[-1]
                    content += u' {0} {1} {2} '.format(caract1, word, caract2)
                else :
                    content += word +u' '
            contentall[art]  = content
        return contentall
          
          
    def codifiedArticles(self):
        dataArticles = self.normalizeDataToCodif()
        datacodified = {}
        for art in dataArticles.keys() :
            artcodif          = parseArticle(dataArticles[art])
            datacodified[art] = artcodif
        return datacodified
         
         
    def readTag(self, tag):
        elsearch = re.search(ur'<.+>(.+)</.+>', tag)
        elment   = elsearch.group(1)
        return elment
    
    
    def segmentArticles (self, article):
        if re.search(ur'.+\s<cgr-pt>\.</cgr-pt>\s.+\s<cte-cat>.+', article) : 
            arts = re.search(ur'(.+\s<cgr-pt>\.</cgr-pt>)(\s.+\s<cte-cat>.+)', article)
            art1, art2 = arts.group(1), arts.group(2)
            self.segmentArticles (art1)
            self.segmentArticles (art2)
        else :
            """
            print '3--------------------------------------'
            print article
            print '--------------------------------------\n\n'
            """
            self.treatArticles.append(article)
    
    
    def formatArticles(self):
        dataCodified  = self.codifiedArticles()
        for i, article in dataCodified.items() :
            if i == 'article1' : self.treatArticles.append('sep')
            if article.count('<cgr-pt>.</cgr-pt>') >= 2 :
                if re.search(ur'<cgr-pt>\.</cgr-pt>\s<cte-cat>', article) :
                    self.treatArticles.append(article)
                    """
                    print '1--------------------------------------'
                    print article
                    print '--------------------------------------\n\n'
                    """
                elif self.segmentArticles (article):
                    print True
            else :
                self.treatArticles.append(article)
                """
                print '2--------------------------------------'
                print article
                print '--------------------------------------\n\n'
                """
        return self.treatArticles
                    
                    