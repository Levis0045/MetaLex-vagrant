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
from wx.lib import art

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
                if codif in t and i == u'cats'    : return u' <cte:cat>'+codif+u'</cte:cat> '
                if codif in t and i == u'genres'  : return u' <cte:genre>'+codif+u'</cte:genre> '
                if codif in t and i == u'marques' : return u' <cte:marque>'+codif+u'</cte:marque> '
                if codif in t and i == u'varLings': return u' <cte:vLings>'+codif+u'</cte:vLings> '
                if codif in t and i == u'nombres' : return u' <cte:nbre>'+codif+u'</cte:nbre> '
                if codif in t and i == u'rection' : return u' <cte:rection>'+codif+u'</cte:rection> '
                if codif in t and i == u'affixe'  : return u' <cte:affixe>'+codif+u'</cte:affixe> '
        
        elif typ == u'symb' and codif in v and k == typ  :
            for i, t in symbCodif.items() :
                if codif in t and i == u'numbers' : return u' <csy:nbre>'+codif+u'</cte:nbre> '
                if codif in t and i == u'alpha'   : return u' <cte:alpha>'+codif+u'</cte:alpha> '
                if codif in t and i == u'symbs'   : return u' <cte:syb>'+codif+u'</cte:syb> '
                
                
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
        elsearch = re.search(ur'<.+>(.+)</.+>', tag)
        elment   = elsearch.group(1)
        return elment
    
    
    def makeComponentsArt(self):
        dataCodified  = self.codifiedArticles()
        treatArticles = []
        for article in dataCodified.keys() :
            identification, traitement, artComponents = u'', u'', u''
            cat, genre, treat, ident = False, False, False, True
            data = dataCodified[article].strip()
            data1  = re.sub(ur'<entry>(?P<ent>.+)<cgr>,</cgr>(?P<flex>....?.?)<cte:cat>', u'<entry>\g<ent><cgr>,</cgr>\g<flex></entry><cte:cat>', data)
            data2  = re.sub(ur'^(?P<entry>.+)<cte:cat>', u'<entry>\g<entry></entry><cte:cat>', data1)
            data3  = re.sub(ur'<entry>(?P<entry>.+)<cgr>,</cgr>', u'<entry>\g<entry></entry><cgr>,</cgr>', data2)
            #entry2 = re.sub(ur'<cte:cat>n.</cte:cat> <cte:genre>(?P<gr>..)</cte:genre> <cgr>,</cgr>(?P<ent>.+)', u'</entry><cte:cat>n.</cte:cat> <cte:genre>\g<gr></cte:genre> <cgr>,</cgr>\g<ent>', entry)
            #entry3 = re.sub(ur'<entry>(?P<ent>.+)<cgr>,</cgr>(?P<flex>....?.?)<cte:cat>', u'<entry>\g<ent><cgr>,</cgr>\g<flex></entry><cte:cat>', entry2)
            #entry4 = re.sub(ur'<entry>(?P<ent>.+) <cte:cat><cgr>,</cgr>', u'<entry>\g<ent><cte:cat>', entry3)
            print data3+'\n'
                    
            print '\n'
            
            
        return treatArticles
                    
                    
    def formatArticles(self):
        componentsArt = self.makeComponentsArt()    
        for art in componentsArt :
            print None+'\n'
           
        """
        if len(art) >= 1 : 
            if  art.find(u'<cte:cat>') == -1 and treat == False and ident == True:
                identification += art+u' '
                print identification+'*******'
                pass
            elif art.find(u'<cte:genre>') != -1 and cat == True :
                identification += art+u' '
                cat = False
                pass
            elif art.find(u'<cte:cat>') != -1 and cat == False :
                identification += art+u' '
                cat = True
                pass
            elif  art.find(u'<cgr>,</cgr>') != -1 and cat == True :
                traitement += art+u' '
                treat, ident = True, False
                pass
            elif treat == True and ident == False : 
                traitement += art+u' '
                pass
            if  art.find(u'<cte:cat>') != -1 and treat == False and ident == True:
                identification += art+u' '
                print identification+'*******'
                pass
            #print identification+'*******'+traitement+'\n'
        
        if re.search(ur'<cte:cat>n\.</cte:cat>', data, flags=re.I) :
            identification = re.search(ur'(.+<cte:cat>n.</cte:cat>.+</cte:genre>).+', data, flags=re.I)
            traitement     = re.search(ur'.+<cte:cat>n.</cte:cat>.+</cte:genre>(.+)', data, flags=re.I)
            #if identification and traitement : print identification.group(1)+traitement.group(1)+'\n'
            if identification and traitement : 
                artComponents = u'<article><identification>'+identification.group(1)+u'</identification>'+u'<traitement>'+traitement.group(1)+u'</traitement></article>'
                treatArticles.append(artComponents)
        if re.search(ur'^.+\s<cte:cat>v\.</cte:cat>(.+</cte:rection>|.+</cgr>|.+</cte:vLings>).+', data, flags=re.I)  :
            identification = re.search(ur'(.+<cte:cat>v.</cte:cat>(.+</cte:rection>)?).+', data, flags=re.I)
            traitement     = re.search(ur'.+<cte:cat>v.</cte:cat>(.+)', data, flags=re.I)
            if identification and traitement : 
                artComponents = u'<article><identification>'+identification.group(1)+u'</identification>'+u'<traitement>'+traitement.group(1)+u'</traitement></article>'
                treatArticles.append(artComponents)
        if re.search(ur'^.+\s<cte:cat>adj\.</cte:cat>.+', data, flags=re.I)  :
            identification = re.search(ur'(.+<cte:cat>adj.</cte:cat>(.+</cte:rection>)?).+', data, flags=re.I)
            traitement     = re.search(ur'.+<cte:cat>adj.</cte:cat>(.+)', data, flags=re.I)
            if identification and traitement : 
                artComponents = u'<article><identification>'+identification.group(1)+u'</identification>'+u'<traitement>'+traitement.group(1)+u'</traitement></article>'
                treatArticles.append(artComponents)    
        if re.search(ur'^.+\s<cte:cat>adv\.</cte:cat>.+', data, flags=re.I)  :
            identification = re.search(ur'(.+<cte:cat>adv.</cte:cat>(.+</cte:rection>)?).+', data, flags=re.I)
            traitement     = re.search(ur'.+<cte:cat>adv.</cte:cat>(.+)', data, flags=re.I)
            if identification and traitement : 
                artComponents = u'<article><identification>'+identification.group(1)+u'</identification>'+u'<traitement>'+traitement.group(1)+u'</traitement></article>'
                treatArticles.append(artComponents)
        if re.search(ur'^.+\s<cte:cat>prép\.</cte:cat>.+', data, flags=re.I)  :
            identification = re.search(ur'(.+<cte:cat>prép.</cte:cat>(.+</cte:rection>)?).+', data, flags=re.I)
            traitement     = re.search(ur'.+<cte:cat>prép.</cte:cat>(.+)', data, flags=re.I)
            #if identification and traitement : print identification.group(1)+traitement.group(1)+'\n'
            if identification and traitement : 
                artComponents = u'<article><identification>'+identification.group(1)+u'</identification>'+u'<traitement>'+traitement.group(1)+u'</traitement></article>'
                treatArticles.append(artComponents)
        
         entry  = re.sub(ur'<identification>(?P<entry>.+)<cte:cat>', u'<identification><entry>\g<entry></entry><cte:cat>', art)
            entry2 = re.sub(ur'<cte:cat>n.</cte:cat> <cte:genre>(?P<gr>..)</cte:genre> <cgr>,</cgr>(?P<ent>.+)</entry>', u'</entry><cte:cat>n.</cte:cat> <cte:genre>\g<gr></cte:genre> <cgr>,</cgr>\g<ent>', entry)
            entry3 = re.sub(ur'<entry>(?P<ent>.+)<cgr>,</cgr>(?P<flex>....?.?)<cte:cat>', u'<entry>\g<ent><cgr>,</cgr>\g<flex></entry><cte:cat>', entry2)
            entry4 = re.sub(ur'<identification><entry>(?P<ent>.+) <cte:cat><cgr>,</cgr>', u'<identification><entry>\g<ent><cte:cat>', entry3)
            print entry4+'\n'
    
        
        u'loc', 
        u'Fig', u'tr', u'intr', u'interj', u'art', u'conj', u'pron',
        u'loc.conj', u'loc.adv', u'loc.adj', u'pron.relat', u'pronom',
        """           
