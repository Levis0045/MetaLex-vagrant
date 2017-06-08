#!/usr/bin/python
# coding: utf8 

import sys, os
pytesserocr = os.path.dirname(os.path.abspath(__file__))+'/pytesseocr'
resources = pytesserocr = os.path.dirname(os.path.abspath(__file__))+'/resources'

sys.path.append(pytesserocr)
sys.path.append(resources)
