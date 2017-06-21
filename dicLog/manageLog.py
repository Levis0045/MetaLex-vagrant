#!/usr/bin/python
# coding: utf8


"""
    
    ManageLog registers all operations triggered throughout the process
    Of metalexicographic processing
    
    Usage:dryadedryadedryadedryadedryadedryadedryadedryadedryade
        >>> from MetaLex import manageLog
        >>> manageLog.writelog()
     
"""

# ----Internal Modules------------------------------------------------------

import MetaLex

# ----External Modules------------------------------------------------------

import codecs, os

# -----Exported Functions-----------------------------------------------------

__all__ = ['writelog', 'logname', 'folderlog']

# -----Global Variables-----------------------------------------------------


# --------------------------------------------------------------------------

def logname():
    strdate = ''
    datefile = os.popen('date').read()
    datetab = datefile.split(',')[0].split(' ')
    for date in datetab[1:] :
        strdate += date + '-'
        
    projectName = MetaLex.projectName
    return projectName+u'_'+strdate.strip(u'-')+u'.dicLog'
    
    
def folderlog():
    name = logname()
    position = os.getcwd()
    os.chdir('..')
    parentdir =  os.listdir('.')
    if u'dicLogs' not in parentdir :
        os.chdir(position)
        currentdir = os.listdir('.')
        if u'dicLogs' not in currentdir :
            os.mkdir(u'dicLogs')
            os.chdir(u'dicLogs/')
        else:
            os.chdir(u'dicLogs/') 
    else:
        os.chdir(u'dicLogs/') 
    
    currentdirlog = os.listdir('.')
    if name not in currentdirlog :
        logfile = codecs.open(name, 'a', 'utf-8')
        return logfile  
    else:
        pass


def writelog(content):
    name = logname()
    datefile = os.popen('date').read()
    datetab = datefile.split(',')[1].split(' ')
    hour = datetab[1]
    
    folderlog()      
    currentdirlog = os.listdir('.')
    if name in currentdirlog :
        with codecs.open(name, 'a', 'utf-8') as file :
            header = u'\n***** MetaLex : '+hour+u' ********************************************** \n\n'
            message = u'--> '+content+u'\n'
            file.write(header)
            file.write(message) 
    else:
        pass
    
    os.chdir('..')
    print u'Log Writing is finish : "'+content+u'"\n'
    
