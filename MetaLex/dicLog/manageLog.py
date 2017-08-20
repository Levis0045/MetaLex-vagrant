#!/usr/bin/env python
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

import codecs, os, re
import unicodedata
from string import maketrans

# -----Exported Functions-----------------------------------------------------

__all__ = ['writelog', 'logname', 'folderlog', 'getDate']

# -----Global Variables-------------------------------------------------------


# ----------------------------------------------------------------------------

def getDate():
    strdate  = ''
    datefile = os.popen('date').read()

    try :
        datetab  = datefile.split(',')[0].split(' ')
        for date in datetab[1:] :
            strdate += date+'-'
        date = unicode(strdate.strip('-').translate(maketrans('û', 'u ')))
        date = unicodedata.normalize('NFKD', date).encode('ascii','ignore')
        return date
    except :
        datetab  = datefile.split(' ')
        for date in datetab :
            strdate += date+'-'
        date = unicode(strdate.strip('-'))
        return date

def logname():
    strdate = getDate()
    projectName = MetaLex.projectName
    logName = projectName+'_'+strdate+'.dicLog'
    return logName


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
            print 'Error :  We can cannot create dicLogs folder in this directory ! It is right exception ?'
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
    try :
        datetab = datefile.split(',')[1].split(' ')
        hour = datetab[1]
    except :
        datetab = datefile.split(' ')[3]
        hour = datetab

    folderlog()
    currentdirlog = os.listdir('.')
    if name in currentdirlog :
        with codecs.open(name, 'a', 'utf-8') as log :
            header = u'\n***** MetaLex : '+hour+u' ********************************************** \n\n'
            message = u'--> '+content+u'\n'
            log.write(header)
            log.write(message)
    else:
        pass
    #os.chdir('..')
    print u'Log writing is finish : "'+content+u'"\n'
