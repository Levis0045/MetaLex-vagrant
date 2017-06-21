#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
"""
    Ce package implémente tous les plugins de MetaLex
    
"""
 
__version__ = "0.0.1"

# ----Internal Modules------------------------------------------------------

from .dicOcrText  import *
from .dicXmlised  import *
from .dicLog      import *
from .dicPlugins  import *
from dicProject   import *

# -----Global Variables-----------------------------------------------------

projectName = ''
allProjectNames = [] 
fileImages = []
treatImages = []
resultOcrFiles = []
resultOcrData = {}

# ----------------------------------------------------------

version = "MetaLex package is in a version : %s " %__version__

    