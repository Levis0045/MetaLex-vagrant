#! usr/bin/env python
# coding: utf8


"""
    Implémentation des outils d'ocrisation de l'image.
 
    Usage:
 
    >>> import MetaLex as dico
    >>> import ImageFilter as     
    >>> project = dico.newProject(project_name)
    >>> images = project.MetaLex.getImages(imagelist)
    >>> images.enhanceImages().filter(f.DETAIL)
    >>> images.imageToText(show=True, langIn='fra')
    
"""

# ----Internal Modules------------------------------------------------------

import MetaLex
from MetaLex import dicProject

# ----External Modules------------------------------------------------------

from tesserocr import PyTessBaseAPI
import codecs

# -----Exported Functions-----------------------------------------------------

__all__ = ['imageToText']

# -----Global Variables-----------------------------------------------------


# ----------------------------------------------------------

    
def imageToText(show=False, save=False, langIn='fra'):
    """
        Take image files, ocrised and save them to 'dicTemp' folder
    """
    
    allimages = []
    if len(MetaLex.fileImages) >= 1 and not len(MetaLex.treatImages) >= 1 :
        print "\n Vous avez aucun(s) fichier(s) image traité(s), veuillez les traiter avant la lecture optique \n"
    
    elif not len(MetaLex.fileImages) >= 1 :
        print " \n Vous n'avez aucun(s) fichier(s) image à traiter"
    
    else:
        allimages = MetaLex.treatImages
         
    num = 1
    for img in allimages :
        with PyTessBaseAPI() as api:
            api.Init(lang=langIn)
            api.SetImageFile(img)
            
            image, ext = dicProject.get_part_file(img)
            imagepart = image.split('_')[:3]
            imagefile = image+ext
            
            imageconcat = ''
            for i in imagepart :
                imageconcat +='_'+i 
            imageconcat = imageconcat.split('.')[0]
            tempname = 'text_ocr'+imageconcat+'_'+str(num)+'.html'
            
            print "\n--> Début de la lecture optique de '"+imagefile+"'\n"
            textocr = api.GetHOCRText(0)
            print "\n--> Fin de la lecture optique de '"+imagefile+"'\n"
            
            if save:
                dicProject.createtemp()
                with codecs.open(tempname, 'w', "utf-8") as wr :
                    wr.write(textocr)
                message = "'"+ imagefile +"' is Ocrised to > '"+tempname+"' > Saved in dicTemp folder" 
                print "--> "+message+"\n"
                MetaLex.dicLog.manageLog.writelog(message) 
            elif show :
                print "\n\n*********************************************************\n\n"
                print textocr
                print "\n\n*********************************************************\n\n"
            else :
                message = " Warning : imageToText(show=False, save=False) >> precise the action 'show=False or save=False'"
                MetaLex.dicLog.manageLog.writelog(message) 
                
            dicProject.treat_ocr_append(tempname)  
            MetaLex.resultOcrData[img] = [textocr]
            
        num += 1
                
    return MetaLex.resultOcrData
                
                
                
                
