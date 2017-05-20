#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
"""
    Implémentation des outils de normalization de l'image.
 
    Usage:
 
    >>> import MetaLex as dico
    >>> import ImageFilter as f
    >>> project = dico.newProject(project_name)
    >>> images = project.MetaLex.getImages(imagelist)
    >>> images.enhanceImages().filter(f.DETAIL)
    >>> images.enhanceImages().bright(1, save=True)
    
    filters :
    
    'BLUR', 'BuiltinFilter', 'CONTOUR', 'DETAIL', 'EDGE_ENHANCE', 
    'EDGE_ENHANCE_MORE', 'EMBOSS', 'FIND_EDGES', 'Filter', 
    'GaussianBlur', 'Kernel', 'MaxFilter', 'MedianFilter', 
    'MinFilter', 'ModeFilter', 'RankFilter', 
    'SHARPEN', 'SMOOTH', 'SMOOTH_MORE', 'UnsharpMask'
          
"""
 
import MetaLex
from MetaLex import dicProject

# ----------------------------------------------------------

import Image, os
import ImageEnhance
from shutil import copyfile
import warnings

# ----------------------------------------------------------

__all__ = ['getImages', 'enhanceImages']

# ----------------------------------------------------------


def getImages(images):
    """Take input image list and save it in the scope"""
    
    if len(images) >= 1 :
        num = 1
        for image in images : 
            exts = ('.png', '.jpg', '.JPG', '.jpeg', '.PNG', '.JPEG', '.tif', '.gif')
            imageroot, ext = dicProject.get_part_file(image)
            if os.path.isfile(image) and ext in exts:
                imagedir = os.path.dirname(image)
                
                imagedirNew = ""
                for tep in imagedir.split('/')[:-1] :
                    imagedirNew += tep +"/"
                imagedirNew = imagedirNew+"dicImages/"
                
                if not os.path.exists(imagedirNew) :
                    os.mkdir(imagedirNew)
                    
                imagefileNew = "dic_image_"+str(num)+ext
                imageLocationNew =  imagedirNew+'/'+imagefileNew
                copyfile(image, imageLocationNew)
                MetaLex.fileImages.append(imageLocationNew)
                num += 1
            else :
                print " Error : getImages(images) >> The input image '"+imageroot+ext+"' is not a file image"
                
        imagestr = str(images)
        message = imagestr + ' > are append for the current treatment' 
        MetaLex.dicLog.manageLog.writelog(message)
    else: 
        message = ' Error : getImages(images) >> They are not images for the current treatment : input images !!' 
        print message+"\n"
        MetaLex.dicLog.manageLog.writelog(message)
        
    return MetaLex
    
        
   
class enhanceImages ():
    """
    This Class enhance image file and save them to 'dicTemp'
    """
    
    def __init__(self):
        self.images = MetaLex.fileImages
        
    def contrast(self, value, show=False, save=False):
        """Enhance image file with the contrast value"""
        
        if self.images >= 1 :
            num = 1
            for image in  self.images :
                img = Image.open(image)
                imagename, ext = dicProject.get_part_file(image)
                tempname = 'img_contrast_'+str(num)+'.'+ext
                enh = ImageEnhance.Contrast(img)
                
                if show :
                    enh.enhance(value).show()
                elif save :
                    dicProject.createtemp()
                    enh.enhance(value).save(tempname)
                    dicProject.treat_image_append(tempname)
                    message = imagename + 'is modified with contrast (' +str(value)+ ') > '+tempname+' > Saved in dictemp folder'  
                    MetaLex.dicLog.manageLog.writelog(message) 
                    num += 1 
                else :
                    print ' Warning : contrast(value, show=False, save=False) --> You must define one action for the current treatment : show=true or save=true '
                    
        else:
            message = ' Error : getImages(images) >> They are not images for the current treatement : please input images !! ' 
            print message+"\n"
            MetaLex.dicLog.manageLog.writelog(message)
            
            
    def sharp(self, value, show=False, save=False):
        """Enhance image file with the sharp value"""
        
        if len(self.images) >= 1 :
            num = 1
            for image in  self.images :
                img = Image.open(image)
                imagename, ext = dicProject.get_part_file(image)
                tempname = 'img_sharp_'+str(num)+'.'+ext
                enh = ImageEnhance.Sharpness(img)

                if show :
                    enh.enhance(value).show()
                elif save :
                    dicProject.createtemp()
                    enh.enhance(value).save(tempname)
                    dicProject.treat_image_append(tempname)
                    message = imagename + 'is modified with sharp (' +str(value)+ ') > '+tempname+' > Saved in dictemp folder'  
                    MetaLex.dicLog.manageLog.writelog(message) 
                    num += 1 
                else :
                    print 'Warning : sharp(value, show=False, save=False) --> You must define one action for the current treatment : show=true or save=true '
        
        else:
            message = ' Error : getImages(images) >> They are not images for the current treatement : please input images !! ' 
            print message+"\n"
            MetaLex.dicLog.manageLog.writelog(message)
            
            
    def bright(self, value, show=False, save=False):
        """Enhance image file with the bright value"""
        
        if len(self.images) >= 1 :
            num = 1
            for image in  self.images :
                img = Image.open(image)
                imagename, ext = dicProject.get_part_file(image)
                tempname = 'img_bright_'+str(num)+'.'+ext
                enh = ImageEnhance.Brightness(img)

                if show :
                    enh.enhance(value).show()
                elif save :
                    dicProject.createtemp()
                    enh.enhance(value).save(tempname)
                    dicProject.treat_image_append(tempname)
                    message = imagename + 'is modified with bright (' +str(value)+ ') > '+tempname+' > Saved in dictemp folder'  
                    MetaLex.dicLog.manageLog.writelog(message) 
                    num += 1 
                else :
                    print 'Warning : bright(value, show=False, save=False) --> You must define one action for the current treatment : show=true or save=true '
        else:
            message = ' Error : getImages(images) >> They are not images for the current treatement : input images!!' 
            print message+"\n"
            MetaLex.dicLog.manageLog.writelog(message)
            
            
    def contrastBright(self, contrast, bright, show=False, save=False):
        """Enhance image file with the contrastBright value"""
        
        if len(self.images) >= 1 :
            num = 1
            for image in  self.images :
                img = Image.open(image)
                imagename, ext = dicProject.get_part_file(image)
                tempname = 'img_bright_'+str(num)+'.'+ext
                enhbright = ImageEnhance.Brightness(img)
                dicProject.createtemp()
                enhbright.enhance(bright).save(tempname)
                img2 = Image.open(tempname)
                enhconst = ImageEnhance.Contrast(img2)
                tempname2 = 'img_contrast_bright_'+str(num)+'.png'
                dicProject.createtemp()
                enhconst.enhance(contrast).save(tempname2)
                os.remove(tempname)
                dicProject.treat_image_append(tempname2)
                message = imagename + ' is modified with  contrast (' +str(contrast)+ ') and  bright ('+str(bright)+') > '+tempname2+' > Saved in dictemp folder'  
                MetaLex.dicLog.manageLog.writelog(message) 
                img.close()
                num += 1
        else:
            message = '  > They are not images for the current treatement : input images!!' 
            print message+"\n"
            MetaLex.dicLog.manageLog.writelog(message)  
            
            
           
    def convert (self):
        """Convert image file to white/black image"""
        
        if len(self.images) >= 1 :
            num = 1
            for image in  self.images :
                img = Image.open(image)
                imagename, ext = dicProject.get_part_file(image)
                tempname = 'img_convert_'+str(num)+'.'+ext
                img.convert("L").show()
                num += 1
        else:
            message = '  > They are not images for the current treatement : input images!!' 
            print message+"\n"
            MetaLex.dicLog.manageLog.writelog(message)
            
                  
                
    def filter (self, imgfilter):
        """Filter image file with specific filter value"""
        
        if len(self.images) >= 1 :
            num = 1
            for image in  self.images :
                img = Image.open(image)
                imagename, ext = dicProject.get_part_file(image)
                tempname = 'img_filter_'+str(num)+'.'+ext
                dicProject.createtemp()
                img.filter(imgfilter).save(tempname)
                dicProject.treat_image_append(tempname)
                message = imagename + ' is modified with  filter (' +str(imgfilter)+ ')  > '+tempname+' > Saved in dictemp folder'  
                MetaLex.dicLog.manageLog.writelog(message)
                img.close()
                num += 1
        else:
            message = '  > They are not images for the current treatement : input images!!' 
            print message+"\n"
            MetaLex.dicLog.manageLog.writelog(message)
            
                    
                
    def removeColor (self):
        """Remove color in image file to enhance its quality"""
        
        if len(self.images) >= 1 :
            num = 1
            for image in  self.images :
                img = Image.open(image)
                imagename, ext = dicProject.get_part_file(image)
                tempname = 'img_color_remove_'+str(num)+'.'+ext
                
                replace_color = (255, 255, 255)
                find_color = (0, 0, 0)
                new_image_data = []
                for color in list(img.getdata()) :
                    #print color
                    if color == find_color or color == replace_color :
                        #print color
                        new_image_data += [color]
                    else:
                        #print color
                        pass
                        
                img.putdata(new_image_data)
                img.show()
                pass
        else:
            message = '  > They are not images for the current treatement : input images!!' 
            print message+"\n"
            MetaLex.dicLog.manageLog.writelog(message)
            
                    
