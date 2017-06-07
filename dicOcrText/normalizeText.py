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
from array import array

# -----Exported Functions-----------------------------------------------------

__all__ = ['makeTextWell', 'fileRule']

# -----Global Variables-----------------------------------------------------

dicArticles = []
AllWords = []

# ----------------------------------------------------------

    
def makeTextWell(file_rules, okCorrect=False):
    filerule = fileRule(file_rules)
    data_rules = filerule.fileRuleUnpack()
    html_files = MetaLex.resultOcrFiles
    for html in html_files :
        with open(html, 'r') as h :
            extractArticle(h, data_rules, okCorrect)
            
        
def extractArticle(html_file, data, okCorrect):
    soup = BeautifulSoup(html_file, "html5lib")
    div = soup.find('div', attrs={'class': u'ocr_page'}) 
    art = 1
    
    for div in div.findAll('div', attrs={'class': u'ocr_carea'}) :
        for para in div.findAll('p', attrs={'class': u'ocr_par'}) :
            contentOrigin = u''
            contentCorrection = u''
            for span in para.stripped_strings:
                if span[-1] == u'—' or span[-1] == u'-':
                    span = span[:-1]
                    AllWords.append(span)
                    if okCorrect :
                        spanCorrect = correctWord(span)
                        contentCorrection += spanCorrect
                    else :
                        contentOrigin += span+u' '
                    #print '*****  '+span + ' : ' + spanCorrect
                elif wordReplace(span, data[1], test=True) :
                    span = wordReplace(span, data[1])
                    if okCorrect :
                        spanCorrect = correctWord(span)
                        contentCorrection += spanCorrect+u' '
                    else :
                        contentOrigin += span+u' '
                    #print '*****  '+span + ' : ' + spanCorrect
                elif caractReplace(span, data[2], test=True):
                    span = caractReplace(span, data[2])
                    AllWords.append(span)
                    if okCorrect :
                        spanCorrect = correctWord(span)
                        contentCorrection += spanCorrect+u' '
                    else:
                        contentOrigin += span+u' '
                    #print '*****  '+span + ' : ' + spanCorrect
                else:
                    if okCorrect :
                        AllWords.append(span)
                        spanCorrect = correctWord(span)
                        contentCorrection += spanCorrect+u' '
                    else :
                        AllWords.append(span)
                        contentOrigin += span+u' '
                    #print '*****  '+span + ' : ' + spanCorrect
            artnum = 'art'+str(art)
            crtnum = 'correct'+str(art)
            if len(contentOrigin) >= 5 :
                article = {artnum:contentOrigin, crtnum:contentCorrection}
                dicArticles.append(article)
                art += 1

    for article in dicArticles :
        for art in article.items()[0]:
            print art+'\n'


def correctWord (word):
    correct = MetaLex.wordCorrection()
    if len(word) > 1 :
        word = word.strip()
        if word[-1] in [u'.', u',']:
            fin = word[-1]
            if word[0].isupper() :
                deb = word[0]
                wordc = word[:-1]
                goodword = correct.correction(wordc.lower())
                wordg = deb+goodword[1:]+fin
                return wordg
            else : 
                wordc = word[:-1]
                goodword = correct.correction(wordc)
                wordg = goodword+fin
                return wordg
        elif word[-1] in [u')']:
            return word
        elif word[1] in [u"'", u"’"] :
            deb = word[:2]
            wordc = word[2:]
            goodword = correct.correction(wordc)
            wordg = deb+goodword[1:]
            return wordg
        elif word[0] in [u":"] :
            deb = word[0]
            wordc = word[1:]
            goodword = correct.correction(wordc)
            wordg = deb+goodword[1:]
            return wordg
        else :
            goodword = correct.correction(word)
            return goodword
    else :
        return word
        
        
def wordReplace(word, data, test=False):
    equiv_words = data
    if test :
        if equiv_words.has_key(word) :
            return True
    else :
        if  word in equiv_words.keys() :
            return equiv_words[word]
    
    
def caractReplace(word, data, test=False):
    equiv_caract = data
    if test :
        for k in equiv_caract.items()[0]:
            if word.find(k):
                return True
            else :
                return False
    else:
        for ke in equiv_caract.keys() :
            if word.find(ke):
                return word.replace(ke, equiv_caract[ke])
            break
        
        
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
    
    