#! usr/bin/env python
# coding: utf8

"""
    MetaLex-vagrant test : tool for metalexicographers
    
"""


#-----If MetaLex is in the same file, import MetaLex------------------------

import MetaLex as dico

# ----External Modules------------------------------------------------------

from PIL import ImageFilter as f
import os, glob

# ----Generate real path of images------------------------------------------

imagelist = []
for imagefile in glob.glob('imagesInputFiles/*.jpg') :
    name = os.getcwd()+'/'+imagefile
    imagelist.append(name)


#-----All steps below must follows as presented---------------------------

project = dico.newProject('Title of the project')
project.setConfProject('author', 'Comment', 'Contributors')
images  = project.MetaLex.getImages(imagelist)
images.enhanceImages().filter(f.DETAIL)
images.imageToText(save=True, langIn='fra')
images.makeTextWell('file_Rule.dic')
images.dicoHtml(save=True)

