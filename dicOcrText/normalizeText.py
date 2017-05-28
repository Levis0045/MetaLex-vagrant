#! usr/bin/env python
# coding: utf8

"""
    Implémentation des outils de normalization de l'image.
 
    Usage:
 
    >>> from DICOparser.dicImage import *
    >>> dicoNormalize()
"""

import MetaLex

# ----------------------------------------------------------

from string import rstrip
import re, sys
from collections import Counter

# ----------------------------------------------------------

__all__ = ['makeTextWell', 'readFile', 'correction']

# ----------------------------------------------------------


dicArticles = []
AllWords = []


def fileRuleUnpack(file):
    return false
    
    
    
def makeTextWell(filerule):
    
    with open(file, 'r') as f :
        #tabCategorie = ["adj. ", "n. ", "n. m. ", "n. f. ", "adv.", "prép.", "v.", "n."]
        article = ""
        #regextext = re.compile(r"(adj.|n.|m.|n.|f.|adv.|prép.|v.|n.)", re.M)
        for ligne in f :
            ligne = str(rstrip(ligne))
            if re.match(r"\w+", ligne):
                #print ligne[-1]
                if not(re.match(r"^[A-Z]", ligne)) : 
                    if ligne[-1] != "." :
                        article += ligne
                        #print "%s " %ligne        
                    if ligne[-1] == "." :
                        article +=" "+ligne+" "
                        article = re.sub(r"(-|—|— |- )",r"", article, re.M)
                        dicArticles.append(article)
                        #print "%s\n" %article
                        article = ""
    
    for art in dicArticles :
        print art, '\n'
        words = art.split()
        AllWords.append(words)
        
    #return dicArticles

    """
    try: 
        if words[1][-1] == '.' :
            #print words[1]
    except :
        print "*****c'est erreur, pas de panique********"
        
    print "\n\n" 
    """
                           
def readFile ():
   
    with open(file, 'r') as f :
        for ligne in f :
            ligne = str(rstrip(ligne))
            if re.match(r"\w+", ligne):
                print ligne                       


# functions for Word spelling proposed in http://norvig.com/spell-correct.html
  
def words(text): 
    w = text.lower().split()
    return w

WORDS = Counter(words(open('ressourcesTextuelles/dela-fr.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])
    print  (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    #print set(w for w in words if w in WORDS)
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = "abcdefghijklmnopqrstuvwxyzéèêîiïàùûâ'"
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    #print inserts
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))  






"""
class wordCorrection :
    def __init__(self):
        self.WORDS = Counter(words(open('big.txt').read()))
        
    def words(self, text): return re.findall(r'\w+', text.lower())
    
    
    def P(self, word, N=sum(WORDS.values())): 
        "Probability of `word`."
        return self.WORDS[word] / N
    
    def correction(self, word): 
        "Most probable spelling correction for word."
        return max(self.candidates(word), key=self.P)
    
    def candidates(self, word): DICOparser
        "Generate possible spelling corrections for word."
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])
    
    def known(self, words): 
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.WORDS)
    
    def edits1(self, word):
        "All edits that are one edit away from `word`."
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)
    
    def edits2(self, word): 
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))  

"""
                     