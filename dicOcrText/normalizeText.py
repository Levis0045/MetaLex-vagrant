#! usr/bin/env python
# coding: utf8

"""
    Implémentation des outils de normalization du texte des articles.
 
    apt-get install python-html5lib
    apt-get install python-lxml
    apt-get install python-bs4
    
    Usage:
    >>> from MetaLex.dicOcrText import *
    >>> makeTextWell()
    
"""

# ----Internal Modules------------------------------------------------------

import MetaLex

# ----External Modules------------------------------------------------------

import re, sys, codecs
from bs4 import BeautifulSoup
import warnings
#import ipdb

# -----Exported Functions-----------------------------------------------------

__all__ = ['makeTextWell', 'fileRule']

# -----Global Variables-----------------------------------------------------

dicArticles = []
AllWords = []

# ----------------------------------------------------------


def makeTextWell(html_f, file_rules, okCorrect=False):
    filerule = fileRule(file_rules)
    data_rules = filerule.fileRuleUnpack()
    #html_ocr_files = MetaLex.resultOcrFiles
    html_ocr_files = html_f
    for html in html_ocr_files :
        with open(html, 'r') as h :
            extractArticle(h, data_rules, okCorrect)
            
         
def findArticle(articles, enhance=False):
    for article in articles :
        #print article
        for art, artcorrect in article.items() :
            if enhance :
                content = artcorrect
                #print content
                #ipdb.set_trace() 
                text = u''
                if content.count(u' n.') > 1 or content.count(u' adj.') > 1 \
                or content.count(u' v.') > 1 or content.count(u' adv.') > 1 \
                or content.count(u' prép.') > 1 :
                    rt =  re.split(r'(\W+)', content)
                    for i, t in enumerate(rt) :
                        #print i, t
                        if t != u'. ': 
                            text += t+u''
                        if t == u'. ' :
                            if u'n' in rt[i:i+8] or u'adv' in rt[i:i+8] \
                            or u'v' in rt[i:i+8] or u'prép' in rt[i:i+8] \
                            or u'adj' in rt[i:i+8] or u'conj' in rt[i:i+8] :
                                print text+'.\n'
                                text = u''
                            else :
                                text += t
                        #print re.split('.', content.strip())
                    
            else : 
                print artcorrect, art

                     
def extractArticle(html_file, data, okCorrect):
    soup = BeautifulSoup(html_file, "html5lib")
    div = soup.find('div', attrs={'class': u'ocr_page'}) 
    art = 1
    
    for div in div.findAll('div', attrs={'class': u'ocr_carea'}) :
        for para in div.findAll('p', attrs={'class': u'ocr_par'}) :
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
                        contentOrigin += span+u''
                        
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
                elif span.count(u'n.') > 1 :
                    print span+'\n'
                else:
                    if okCorrect :
                        AllWords.append(span)
                        spanCorrect = MetaLex.correctWord(span)
                        contentCorrection += spanCorrect+u' '
                    else :
                        AllWords.append(span)
                        contentOrigin += span+u' '
                    #print '*****  '+span + ' : ' + spanCorrect
            print contentOrigin+'\n'
            artnum = 'article_'+str(art)
            crtnum = 'correction_'+str(art)
            if len(contentOrigin) >= 5 :
                article = {crtnum:contentCorrection, artnum:contentOrigin}
                dicArticles.append(article)
                art += 1

    #findArticle(dicArticles, enhance=True)
    
        
        
class fileRule():
    
    def __init__(self, file_rule):
        self.file = file_rule
        
        
    def fileRuleUnpack(self):
        word, caracter, regex = '\W', '\C', '\R'
        metadata, ruleWords, ruleCaracts, ruleRegex = {}, {}, {}, {}
        startw, startc, startr = False, False, False
        
        if self.verify() :
            with codecs.open(self.file, 'r', 'utf-8') as rule :
                for line in rule : 
                    line = line.strip()
                    if line.startswith('\MetaLex') : 
                        names = ('tool', 'project', 'theme', 'lang', 'admin', 'date')
                        for name, cnt in zip(names, line.split('\\')[1:]) :
                            metadata[name] = cnt
                    if line == word : startw, startc, startr = True, False, False
                    if line == caracter : startw, startc, startr = False, True, False
                    if line == regex : startw, startc, startr = False, False, True
                    if startw :
                        linepart = line.split('/')
                        if len(linepart) == 3 : ruleWords[linepart[1]] = linepart[2]
                    if startc :
                        linepart = line.split('/')
                        if len(linepart) == 3 : ruleCaracts[linepart[1]] = linepart[2]
                    if startr :
                        linepart = line.split('/')
                        if len(linepart) == 3 : ruleRegex[linepart[1]] = linepart[2]
        else :
            warnings.warn("Your file syntax is not correct. Please correct it as recommended")
                    
        return metadata, ruleWords, ruleCaracts, ruleRegex 
        
    
    def verify(self):
        module, synw, sync, synr, synrw, delimiter = (False for x in range(6))
        fileop = codecs.open(self.file, 'r', 'utf-8').readlines()
        if '\START' == fileop[0].strip() and '\END' == fileop[-1].strip() : delimiter = True
        if len(fileop[1].strip().split('\\')) == 7 :
            for el in fileop[1].strip().split('\\') :
                if el == 'MetaLex': module = True
        for lg in fileop:
            lg = lg.strip()
            if lg == '\W' : synw = True
            if lg == '\C' : sync = True
            if lg == '\R' : synr = True
            if lg[0] == '/' : 
                if len(lg.split('/')) == 3 : synrw = True
        if sync and synw and synr and module and delimiter and synrw :
            return True
        else :
            return False
    
    