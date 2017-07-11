#!/usr/bin/python
# coding: utf8



"""
    ManageLog registers all operations triggered throughout the process
    Of metalexicographic processing


    Usage:
        >>> import MetaLex as dico
        >>> projet = dico.newProject('LarousseMemoire')
     
"""

# ----Internal Modules------------------------------------------------------

import MetaLex

# ----External Modules------------------------------------------------------

import os, codecs
import pickle

# -----Exported Functions-----------------------------------------------------

__all__ = ['createtemp', 'newProject', 'treat_image_append', 'get_part_file', 'inDir']

# -----Global Variables-----------------------------------------------------


# ----------------------------------------------------------

        
def get_part_file(namefile):
    """
      Extract file image name and file image extension
      @keyword namefile:str
      @return: list (imageroot, ext)
    """
    (imageroot, ext) = os.path.splitext(os.path.basename(namefile))
    return (imageroot, ext)


def treat_image_append(namefile) :
    """
      Append image result files to the global variable at the scope
      @keyword namefile:str
      @return: ...
    """
    tempnameLocation =  os.getcwd()+u'/'+namefile
    MetaLex.treatImages.append(tempnameLocation)


def treat_ocr_append(namefile) :
    """
      Append ocr result files to the global variable
      @keyword namefile:str
      @return: ...
    """
    tempnameLocation =  os.getcwd()+u'/dicTemp/'+namefile
    MetaLex.resultOcrFiles.append(tempnameLocation)
     
     
def inDir(fil):
    """
      Verify if an input file is in a 'dicTemp' folder 
      @return: boolean
    """
    currentdir = os.listdir('.')
    if fil in currentdir :
        return False
    else :
        return True


def nameFile(tab, ext):
    """
      Generate name file to saved result of articles extraction  
      @keyword tab:array
      @keyword ext:str
      @return: namepickle 
    """
    name  = str(tab[0]).split(u'/')[-1].split(u',')[0].split(u'_')[:-1]
    if ext == u'.art' :
        nametxt    = u'articles_'+u'_'.join(name)+u'.art'
        return nametxt
    elif ext == u'.pickle' :
        namepickle = u'articles_'+u'_'.join(name)+u'.pickle'
        return namepickle
        

def filePickle(data, name):
    """
      Create pickle file of the articles data
      @keyword data:dictionary
      @keyword name:str
      @return: True 
    """
    with codecs.open(name, 'wb') as f :
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        return True
    
    
def fileUnpickle(fil):
    """
      Unpack pickle file of articles data
      @keyword fil:str
      @return: data articles object
    """
    with codecs.open(fil, 'rb') as f :
        data = pickle.load(f)
        return data 


def fileGettext(fil):
    """
      Extract articles data into file text
      @return: data articles text
    """
    datatext = {}
    with codecs.open(fil, 'r', 'utf-8') as f :
        for line in f :
            partline = line.split(u':')
            datatext[partline[0].strip()] = partline[1].strip()
    return datatext


def readConf():
    """
      Extract data configuration of the project
      @return: data configuration text
    """
    confData = {}
    with codecs.open(u'MetaLex.cnf', 'r', 'utf-8') as conf :
        for line in conf :
            if line[0] == u'\\' : 
                part  = line.strip().split(u':')
                title = part[0][1:].replace(u' ', u'')
                val   = part[1]
                confData[title] = val
    return confData
        
        
def createtemp():
    """
      Create a 'dicTemp' folder if it doesn't exist at the parent folder at the scope
      @return: place in dicTemp folder
    """
    
    name = u'dicTemp'
    currentdir = os.listdir('.')
    if u'testDicoParser' in currentdir :
        os.chdir(u'testDicoParser/')
        currentdir = os.listdir('.')
        if name not in currentdir and u'dicLogs' in currentdir :
            try:
                os.mkdir(u'dicTemp')
            except os.error :
                pass
            message = u'dicTemp folder' + u'  > is created' 
            MetaLex.dicLog.manageLog.writelog(message)
            os.chdir(u'dicTemp/')
            message = u'Change current directory to  > dicTemp folder'  
            MetaLex.dicLog.manageLog.writelog(message) 
            os.chdir(u'dicTemp/')
        else:
            os.chdir(u'dicTemp/') 
    elif u'dicLogs' in currentdir and u'dicTemp' in currentdir :
        os.chdir(u'dicTemp/') 


def dicFile(fil):
    """
      Take the current script path and join it to file path
      @keyword fil:str
      @return: normalize file path
    """
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, fil)
       
        
class newProject :
    """
       Create new environment project and its configuration
       @keyword projectname: str
       @return: new environment project
    """
    
    import MetaLex
    
    def __init__ (self, projectname):
        self.name = projectname
        MetaLex.allProjectNames.append(self.name)
        MetaLex.projectName = self.name
        self.fileImages     = []
        self.resultOcr      = u""
        self.resultText     = u""
        self.resultXmlised  = u""
        self.resultLog      = u""
        self.lang           = u""
        self.dicoType       = u""
    
    def setConfproject (self, author, comment, contrib):
        """
          Set parameters of new environment project
          @keyword author:str
          @keyword comment:str
          @keyword contrib:str
          @return: normalize file path
        """
        project  = MetaLex.projectName
        MetaLex.projectAuthor = author
        dateInit = MetaLex.manageLog.getDate()
        Intro    = u'***************** MetaLex project configuration *****************'
        end      = u'*****************************************************************'
        content  = Intro+'\n\n'+'\Project name  : '+project+'\n'+'\Creation date : '+dateInit+'\n'+'\Author        : '+author+'\n'+'\Contributors  : '+contrib\
        +'\n'+'\Comment       : '+comment+'\n\n'+end
        MetaLex.dicProject.createtemp()
        if MetaLex.dicProject.inDir('MetaLex.cnf') :
            with codecs.open('MetaLex.cnf', 'w', 'utf-8') as conf :
                conf.write(content)
        
        
    def getProjectName(self):
        return MetaLex.projectName 

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

       
        
   
