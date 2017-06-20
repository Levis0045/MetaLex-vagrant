#! usr/bin/env python
# coding: utf8

"""
    Implémentation des outils de normalization du texte des articles.
    
    Packages:
        >>> apt-get install python-html5lib
        >>> apt-get install python-lxml
        >>> apt-get install python-bs4
    
    Usage:
        >>> from MetaLex.dicOcrText import *
        >>> makeTextWell('dico_rules_larousse.dic')
    
"""

# ----Internal Modules------------------------------------------------------

import MetaLex
from MetaLex import dicXmlised as Xml

# ----External Modules------------------------------------------------------

from bs4 import BeautifulSoup
import re, sys, codecs
import warnings
import pickle
#import ipdb

# -----Exported Functions-----------------------------------------------------

__all__ = ['makeTextWell', 'fileRule']

# -----Global Variables-----------------------------------------------------

dicArticles = []
AllWords    = []
namepickle  = ''
nametxt     = ''

# ----------------------------------------------------------


def makeTextWell(file_rules, okCorrect=False):
    filerule = fileRule(file_rules, typ=u'rule_wc')
    data_rules = filerule.fileRuleUnpack()
    html_ocr_files = MetaLex.resultOcrFiles
    #html_ocr_files = html_f
    for html in html_ocr_files :
        with open(html, 'r') as html_file :
            enhanceText(html_file, data_rules, okCorrect)
        
    name       = str(html_ocr_files[0]).split('/')[-1].split(',')[0].split('_')[:-1]
    namepickle = 'articles_'+'_'.join(name)+'.pickle'
    nametxt    = 'articles_'+'_'.join(name)+'.txt'
    
    saveNormalize(namepickle, 'pickle')
    saveNormalize(nametxt, 'text')     
         
                     
def enhanceText(html_file, data, okCorrect):
    soup = BeautifulSoup(html_file, "html5lib")
    div = soup.find(u'div', attrs={'class': u'ocr_page'}) 
    art = 1
        
    for div in div.findAll(u'div', attrs={'class': u'ocr_carea'}) :
        for para in div.findAll(u'p', attrs={'class': u'ocr_par'}) :
            contentOrigin = u''
            contentCorrection = u''
            
            for span in para.stripped_strings:
                if span[-1] == u'—' or span[-1] == u'-' or span[-1] == u'— ' or span[-1] == u'- ':
                    span = span[:-1]
                    AllWords.append(span)
                    if okCorrect :
                        spanCorrect = MetaLex.correctWord(span)
                        contentCorrection += spanCorrect
                    else :
                        contentOrigin += span
                        
                    #print '*****  '+span + ' : ' + spanCorrect
                elif MetaLex.wordReplace(span, data[1], test=True) :
                    span = MetaLex.wordReplace(span, data[1])
                    if okCorrect :
                        spanCorrect = MetaLex.correctWord(span)
                        contentCorrection += spanCorrect+u' '
                    else :
                        contentOrigin += span+u' '
                        
                    #print '*****  '+span + ' : ' + spanCorrect
                elif MetaLex.caractReplace(span, data[2], test=True):
                    span = MetaLex.caractReplace(span, data[2])
                    AllWords.append(span)
                    if okCorrect :
                        spanCorrect = MetaLex.correctWord(span)
                        contentCorrection += spanCorrect+u' '
                    else:
                        contentOrigin += span+u' '
                        
                    #print '*****  '+span + ' : ' + spanCorrect
                #elif span.count(u'n.') > 1 :
                    #print span+'\n'
                else:
                    if okCorrect :
                        AllWords.append(span)
                        spanCorrect = MetaLex.correctWord(span)
                        contentCorrection += spanCorrect+u' '
                    else :
                        AllWords.append(span)
                        contentOrigin += span+u' '
                    #print '*****  '+span + ' : ' + spanCorrect
            #Xml.findArticles(contentOrigin, enhance=True)
            #print contentOrigin+'\n'
            artnum = u'article_'+str(art)
            crtnum = u'correction_'+str(art)
            if len(contentOrigin) >= 5 and len(contentCorrection) == 0:
                article = {artnum:contentOrigin}
                dicArticles.append(article)
                art += 1
            elif len(contentOrigin) >= 5 and len(contentCorrection) >= 5 :
                article = {crtnum:contentCorrection, artnum:contentOrigin}
                dicArticles.append(article)
                art += 1
                
    
    
    
    
def saveNormalize(name, typ):
    MetaLex.dicProject.createtemp()
    if typ == 'text' :
        if MetaLex.dicProject.inDir(name) :
            with codecs.open(name, 'a', 'utf-8') as file :
                for art in dicArticles :
                    for k, v in art.items() :
                        file.write('%s : %s\n' %(k, v))
            message = '"'+name+'" is created and contain all text format data from html files > Saved in dicTemp folder'  
            MetaLex.dicLog.manageLog.writelog(message) 
            print message
        else :
            message = '"'+name+'" is created and contain all text format data from html files > Saved in dicTemp folder'  
            MetaLex.dicLog.manageLog.writelog(message) 
            print message
    
    if typ == 'pickle' :  
        if MetaLex.dicProject.inDir(name) :
            with open(name, 'wb') as file :
                pickle.dump(dicArticles, file, pickle.HIGHEST_PROTOCOL)
            message = name + ' is created and contain all text format data from html files > Saved in dicTemp folder'  
            MetaLex.dicLog.manageLog.writelog(message) 
            print message
        else :
            message = name + ' is created and contain pickle data object from html files > Saved in dicTemp folder'  
            MetaLex.dicLog.manageLog.writelog(message) 
            print message    
    
        
    #findArticle(dicArticles, enhance=True)
    
        
        
class fileRule():
    
    def __init__(self, file_rule, typ):
        self.file = file_rule
        self.typ = typ
        
        
    def fileRuleUnpack(self):
        word, caracter, regex = u'\W', u'\C', u'\R'
        metadata, ruleWords, ruleCaracts, ruleRegex = {}, {}, {}, {}
        startw, startc, startr = False, False, False
        
        if self.verify(self.typ) :
            if self.typ == u'rule_wc' :
                with codecs.open(self.file, 'r', 'utf-8') as rule :
                    for line in rule : 
                        line = line.strip()
                        if line.startswith(u'\MetaLex') : 
                            names = (u'tool', u'project', u'theme', u'lang', u'admin', u'date')
                            for name, cnt in zip(names, line.split(u'\\')[1:]) :
                                metadata[name] = cnt
                        if line == word : startw, startc, startr = True, False, False
                        if line == caracter : startw, startc, startr = False, True, False
                        if line == regex : startw, startc, startr = False, False, True
                        if startw :
                            linepart = line.split(u'/')
                            if len(linepart) == 3 : ruleWords[linepart[1]] = linepart[2]
                        if startc :
                            linepart = line.split(u'/')
                            if len(linepart) == 3 : ruleCaracts[linepart[1]] = linepart[2]
                        if startr :
                            linepart = line.split(u'/')
                            if len(linepart) == 3 : ruleRegex[linepart[1]] = linepart[2]
            if self.typ == u'rule_art' :
                return False
        else :
            warnings.warn(u"Your file syntax is not correct. Please correct it as recommended")
                    
        return metadata, ruleWords, ruleCaracts, ruleRegex 
        
    
    def verify(self, typ):
        module, synw, sync, synr, synrw, delimiter = (False for x in range(6))
        fileop = codecs.open(self.file, 'r', 'utf-8').readlines()
        if typ == u'rule_wc' :
            if u'\START' == fileop[0].strip() and u'\END' == fileop[-1].strip() : delimiter = True
            if len(fileop[1].strip().split(u'\\')) == 7 :
                for el in fileop[1].strip().split(u'\\') :
                    if el == u'MetaLex': module = True
            for lg in fileop:
                lg = lg.strip()
                if lg == u'\W' : synw = True
                if lg == u'\C' : sync = True
                if lg == u'\R' : synr = True
                if lg[0] == u'/' : 
                    if len(lg.split(u'/')) == 3 : synrw = True
            if sync and synw and synr and module and delimiter and synrw :
                return True
            else :
                return False
            
        if typ == u'rule_art' :
            return False



