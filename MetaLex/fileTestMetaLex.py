#! usr/bin/env python
# coding: utf8

"""
    MetaLex test : tool for metalexicographers
    
    Packages:
        >>> sudo apt-get install build-essential libssl-dev libffi-dev python-dev
        >>> sudo apt-get install libtesseract-dev libleptonica-dev 
        >>> sudo apt-get install python-html5lib
        >>> sudo apt-get install python-lxml
        >>> sudo apt-get install python-bs4
        >>> sudo apt-get install tesseract-ocr-all
        >>> sudo pip install pillow
        >>> sudo pip install Cython
        >>> sudo CPPFLAGS=-I/usr/local/include pip install tesserocr
"""


"""
# Do this if MetaLex folder is in the parent of the current folder
# import sys
# sys.path.append('..')
"""

#-----If MetaLex is in the same file, import MetaLex------------------------
import MetaLex as dico


# ----External Modules------------------------------------------------------

import ImageFilter as f
import os, glob

# ----Generate real path of images------------------------------------------

imagelist = []
for imagefile in glob.glob('folder_of_Images/*.jpg') :
    name = os.getcwd()+'/'+imagefile
    imagelist.append(name)


#-----All steps below must follows as presented---------------------------

project = dico.newProject('Title of the project')
project.setConfProject('author', 'Comment', 'Contributors')
images  = project.MetaLex.getImages(imagelist)
images.enhanceImages().filter(f.DETAIL)
images.imageToText(save=True, langIn='fra')
images.makeTextWell('file_Rule.dic')
images.dicoHtml(save=False)

