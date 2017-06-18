#!/usr/bin/python
# coding: utf8



"""
    manageLog enrégistre toutes les opérations déclenchées tout au long du processus
    de traitement métalexicographique
     
"""

# ----Internal Modules------------------------------------------------------

import MetaLex

# ----External Modules------------------------------------------------------

import os

# -----Exported Functions-----------------------------------------------------

__all__ = ['createtemp', 'newProject', 'treat_image_append', 'get_part_file', 'inDir']

# -----Global Variables-----------------------------------------------------


# ----------------------------------------------------------


def get_part_file(namefile):
    """Extract file image name and file image extension"""
    
    (imageroot, ext) = os.path.splitext(os.path.basename(namefile))
    return (imageroot, ext)


def treat_image_append(namefile) :
    """Append image result files to the global variable at the scope"""
    
    tempnameLocation =  os.getcwd()+'/'+namefile
    MetaLex.treatImages.append(tempnameLocation)


def treat_ocr_append(namefile) :
    """Append ocr result files to the global variable"""
    
    tempnameLocation =  os.getcwd()+'/'+namefile
    MetaLex.resultOcrFiles.append(tempnameLocation)
     
def inDir(file):
    """Verify id a file is in a 'dicTemp' folder """
    
    name = 'dicTemp'
    currentdir = os.listdir('.')
    if file in currentdir :
        return False
    else :
        return True

    
def createtemp():
    """Create a 'dicTemp' folder is it doesn't exist at the parent folder at the scope"""
    
    name = 'dicTemp'
    currentdir = os.listdir('.')
    if name not in currentdir :
        if 'dicLogs' in currentdir :
            try:
                os.mkdir('dicTemp')
            except os.error :
                pass
            message = 'dicTemp folder' + '  > is created' 
            MetaLex.dicLog.manageLog.writelog(message)
            os.chdir('dicTemp/')
            message = 'Change current directory to  > dicTemp folder'  
            MetaLex.dicLog.manageLog.writelog(message) 
            os.chdir('dicTemp/')
    else:
        os.chdir('dicTemp/') 


def dicFile(file):
    """Take the current current script path and join it to file path"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, file)
       
        
class newProject :
    """
        
    """
    
    import MetaLex
    
    def __init__ (self, projectname):
        self.name = projectname
        MetaLex.allProjectNames.append(self.name)
        MetaLex.projectName = self.name
        self.fileImages = []
        self.resultOcr = ""
        self.resultText = ""
        self.resultXmlised = ""
        self.resultLog = ""
        self.lang = ""
        self.dicoType = ""
    
    def getProjectName(self):
        return self.name

    def getFileImages (self):
        if (len(MetaLex.fileImages)>= 1) :
            self.fileImages = MetaLex.fileImages
            return self.fileImages
    
    def getTreatImages (self):
        if (len(MetaLex.dicOcrText.fileImages)>= 1) :
            self.treatImageFile  = MetaLex.dicOcrText.treatImageFile 
            return self.treatImageFile 
    
    def getTextOcr (self):
        if (MetaLex.dicOcrText.textOcr) :
            self.resultOcr += MetaLex.dicOcrText.textOcr
            return self.resultOcr
        
    def getOcrText (self):
        return MetaLex.dicOcrText.makeOcr

       
        
   
