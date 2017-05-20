#!/usr/bin/python
# coding: utf8


"""
    manageLog enrégistre toutes les opérations déclenchées tout au long du processus
    de traitement métalexicographique
     
"""

import MetaLex

# ----------------------------------------------------------

import codecs, os

# ----------------------------------------------------------

__all__ = ['writelog', 'logname', 'folderlog']

# ----------------------------------------------------------

def logname():
    strdate = ''
    datefile = os.popen('date').read()
    datetab = datefile.split(',')[0].split(' ')
    for date in datetab[1:] :
        strdate += date + '-'
        
    projectName = MetaLex.projectName
    return projectName+'_'+strdate.strip('-')+'.dicLog'
    
    
def folderlog():
    name = logname()
    position = os.getcwd()
    os.chdir('..')
    parentdir =  os.listdir('.')
    if 'dicLogs' not in parentdir :
        os.chdir(position)
        currentdir = os.listdir('.')
        if 'dicLogs' not in currentdir :
            os.mkdir('dicLogs')
            os.chdir('dicLogs/')
        else:
            os.chdir('dicLogs/') 
    else:
        os.chdir('dicLogs/') 
    
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
            header = '\n***** MetaLex : '+hour+' ********************************************** \n\n'
            message = '--> '+content+'\n'
            file.write(header)
            file.write(message) 
    else:
        pass
    
    os.chdir('..')
    print 'Log Writing is finish !!\n'
    
