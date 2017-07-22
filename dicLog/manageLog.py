#!/usr/bin/python
# coding: utf8


"""
    
    ManageLog registers all operations triggered throughout the process
    Of metalexicographic processing
    
    Usage:
        >>> from MetaLex import manageLog
        >>> manageLog.writelog()
     
"""

# ----Internal Modules------------------------------------------------------

import MetaLex

# ----External Modules------------------------------------------------------

import codecs, os

# -----Exported Functions-----------------------------------------------------

__all__ = ['writelog', 'logname', 'folderlog', 'getDate']

# -----Global Variables-----------------------------------------------------


# --------------------------------------------------------------------------

def getDate():
    strdate = ''
    datefile = os.popen('date').read()
    datetab = datefile.split(',')[0].split(' ')
    for date in datetab[1:] :
        strdate += date + '-'
    return strdate.strip(u'-')


def logname():
    strdate = getDate()
    projectName = MetaLex.projectName
    return projectName+u'_'+strdate+u'.dicLog'
    
    
def folderlog():
    name       = logname()
    parentdir  = os.listdir('..')
    currentdir = os.listdir('.')

    if u'dicLogs' in currentdir :
        os.chdir(u'dicLogs')        
    elif u'dicLogs' not in currentdir and u'dicTemp' in currentdir :
        try :
            os.mkdir(u'dicLogs')
        except os.error :
            print 'Error :  We can cannot create dicLogs folder in this directory ! It s right exception ?'
            pass
        os.chdir(u'dicLogs/')
    elif u'dicLogs' not in currentdir and u'dicLogs' in parentdir :
        os.chdir(u'..')
        os.chdir(u'dicLogs/')
    else :
        try :
            os.mkdir(u'dicLogs')
        except os.error :
            print 'Error :  We can cannot create dicLogs folder in this directory ! It s right exception ?'
            pass
        os.chdir(u'dicLogs/')
       
    currentdirlog = os.listdir(u'.')
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
    
    print u'Log Writing is finish : "'+content+u'"\n'
    
