#! usr/bin/env python
# coding: utf8

"""
    Implémentation des outils de correction orthographique.
 
    Usage:
    >>> from DICOparser.wordsCorrection import *
    >>> correctWord(word)
"""

# ----Internal Modules------------------------------------------------------

import MetaLex

# ----External Modules------------------------------------------------------

import re, sys, collections
from collections import Counter

# -----Exported Functions-----------------------------------------------------

__all__ = ['correctWord', 'wordReplace', 'caractReplace']

# -----Global Variables-----------------------------------------------------



# --------------------------------------------------------------------

def correctWord (word):
    correct = wordCorrection()
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
            wordtab = word.split(u"’")
            deb, wordc = wordtab[0], wordtab[1]
            goodword = correct.correction(wordc)
            wordg = deb+u'’'+goodword[1:]
            return wordg
        elif word[0] in [u":"] :
            wordtab = word.split(u":")
            deb, wordc = wordtab[0], wordtab[1]
            goodword = correct.correction(wordc)
            wordg = deb+u'’'+goodword[1:]
            return wordg
        else :
            goodword = correct.correction(word)
            return goodword
    else :
        return word


class wordCorrection :
    def __init__(self):
        MetaLex.dicPlugins
        filepath = sys.path[-1]+'/METALEX_words-corpus.txt'
        self.corpusData = open(filepath).read()
        self.WORDS = {}
        self.start()
        self.lettersFr = u"abcdefghijklmnopqrstuvwxyzéèêîiïàùûâ'"

    def start(self):
        self.WORDS = self.train(self.words(self.corpusData))
        
    def words(self, text): 
        return re.findall(r'(\s+)', text.lower())
    
    def train(self, features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    def edits1(self, word):
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in self.lettersFr if b]
        inserts    = [a + c + b     for a, b in splits for c in self.lettersFr]
        return set(deletes + transposes + replaces + inserts)
    
    def known_edits2(self, word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.WORDS)
    
    def known(self, words): return set(w for w in words if w in self.WORDS)
    
    def correction(self, word):
        candidates = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word) or [word]
        return max(candidates, key=self.WORDS.get)
    
    
def wordReplace(word, data, test=False):
    equiv_words = data
    if test :
        if equiv_words.has_key(word) :
            return True
        else :
            return False
    elif word in equiv_words.keys() :
        return equiv_words[word]
        
    
    
def caractReplace(word, data, test=False):
    equiv_caract = data
    equiv_keys = equiv_caract.keys()
    if test :
        for k in equiv_keys:
            #print word + ' ' + k
            if word.find(k):
                return True
            else :
                return False
    else :
        for k in equiv_keys :
            #print equiv_caract.keys()
            if word.find(k):
                return re.sub(k, equiv_caract[k], word)
            
    
    
    
    

"""
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
