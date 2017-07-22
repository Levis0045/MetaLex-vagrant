# MetaLex Tool
MetaLex is general tool for metalexicography activities
For other version of this tool, see [claroline/Claroline](http://github.com/Levis0056/dic)

[![Build Status](https://travis-ci.org/claroline/Distribution.svg?branch=master)](mteprojet.fr/MetaLex)

# Requirements
MetaLex is developped in Python 2.7 environment, these packages are required :

```
    sudo apt-get install python-html5lib
    sudo apt-get install python-lxml
    sudo apt-get install python-bs4
    sudo apt-get install tesseract-ocr-all
    sudo apt-get install libtesseract-dev libleptonica-dev 
    sudo pip install Cython
    sudo CPPFLAGS=-I/usr/local/include pip install tesserocr
    pip install pillow

```

# Usage

- Do this if MetaLex folder is in the parent of the current folder
``` 
import sys 
sys.path.append('..')

```

- If MetaLex is in the same file, import MetaLex

`import MetaLex`

- Import these standard packages

```
import ImageFilter as f
import MetaLex as dico
import os, glob

``` 

- Generate real path of images dictionaries file. The input images must be scans of monolinguals dictionaries

```
imagelist = []
for imagefile in glob.glob('folder_of_Images/*.jpg') :
    name = os.getcwd()+'/'+imagefile
    imagelist.append(name)

```

- All steps below must follows as presented

```
project = dico.newProject('Title of the project')
project.setConfProject('author', 'Comment', 'Contributors')
images  = project.MetaLex.getImages(imagelist)
images.enhanceImages().filter(f.DETAIL)
images.imageToText(save=True, langIn='fra')
images.makeTextWell('file_Rule.dic')
images.dicoHtml(save=False)

```

