#! usr/bin/env python
# coding: utf8

"""
    makeBalise transform extracted articles into  well formed xml file.
    It can also generate HTML file for article edition
    
    Packages:
        >>> sudo apt-get install python-html5lib
        >>> sudo apt-get install python-lxml
        >>> sudo apt-get install python-bs4
    
    Usage:
        >>> from MetaLex.dicXmilised import *
        >>> dicoHtml(save=True)
"""

# ----Internal Modules------------------------------------------------------

import MetaLex
from   composeArticle import *
from   dicXmlTool     import *

# ----External Modules------------------------------------------------------

import re, sys, codecs, os
from bs4    import BeautifulSoup
from random import sample
from shutil import copyfile
from lxml   import etree

# -----Exported Functions-----------------------------------------------------

__all__ = ['baliseXML', 'dicoHtml']

# -----Global Variables-----------------------------------------------------

components = {
                u'xml'  :   {
                              u'metadata'       : [u'projectname', u'author', u'date', u'comment', u'contributors'],
                              u'identification' : [u'article', u'entry', u'flexion', u'category', u'gender', u'rection', u'phonetic'], 
                              u'treatment'      : [u'definition', u'contextualisation', u'figured', u'contrary']
                            },
                u'tei'  :   {
                              u'metadata'       : [],
                              u'identification' : [], 
                              u'treatment'      : []
                            },
                u'lmf'  :   {
                              u'metadata'       : [],
                              u'identification' : [], 
                              u'treatment'      : []
                            },
                u'dtd'  :   [u'ELEMENT', u'ATTRIBUTE', u'PCDATA', u'CDATA', u'REQUIRED', u'IMPLIED'],
                u'xsd'  :   []
             }

articles   = []

# ----------------------------------------------------------

def dicoHtml(save=False) :
    """
      Build HTML editor file of the all articles 
      @return: file:MetaLexViewerEditor.html
    """
    MetaLex.dicPlugins
    
    instanceHtml = baliseHTML()
    filepath     = sys.path[-1]+u'/MetaLex-template.html'
    MetaLex.dicProject.createtemp()
    if MetaLex.dicProject.inDir('CopyMetaLexTemplate.html') :
        copyfile(filepath, 'CopyMetaLexTemplate.html')
        souphtl = instanceHtml.htmlInject('CopyMetaLexTemplate.html')
        if save : 
            with codecs.open('MetaLexViewerEditor.html', 'w') as htmlresult :
                htmlresult.write(souphtl)
            os.remove('CopyMetaLexTemplate.html')
            message = u"'MetaLexViewerEditor.html' has correctly been generated > Saved in dicTemp folder" 
            MetaLex.dicLog.manageLog.writelog(message)
    else :
        souphtl = instanceHtml.htmlInject('CopyMetaLexTemplate.html')
        if save : 
            with codecs.open('MetaLexViewerEditor.html', 'w') as htmlresult :
                htmlresult.write(souphtl)
            os.remove('CopyMetaLexTemplate.html')
            message = u"'MetaLexViewerEditor.html' has correctly been generated > Saved in dicTemp folder" 
            MetaLex.dicLog.manageLog.writelog(message)
    
      
 
class baliseHTML () :
    
    def __init__(self) :
        self.resultHtml = ''
        
    def htmlInject(self, template):
        """
          Create prettify HTML file all previous data generated 
          @return: str:html (prettify by BeautifulSoup)
        """
        instanceXml    = baliseXML()
        contentxml     = instanceXml.xmlised(typ=u'xml', save=False)
        MetaLex.dicProject.createtemp()
        soupXml        = BeautifulSoup(contentxml, "html5lib")
        projectconf    = MetaLex.dicProject.readConf()
        Hauthor, Hname, Hdate, Hcomment, Hcontrib = projectconf['Author'], projectconf['Projectname'], projectconf['Creationdate'], projectconf['Comment'], projectconf['Contributors']
        filetemplate   = codecs.open(template, 'r', 'utf-8')
        souphtml       = BeautifulSoup(filetemplate, "html5lib")
        content        = souphtml.find(u'div', attrs={'id': u'all-articles'}) 
        author         = content.find(u'h3', attrs={'id': u'author'})
        author.string  = 'main : '+Hauthor
        date           = content.find(u'h5', attrs={'id': u'date'})
        date.string    = Hdate
        descipt        = content.find(u'p', attrs={'id': u'description'})
        descipt.string = Hcomment
        contrib        = content.find(u'h4', attrs={'id': u'contributors'})
        contrib.string = 'contributors : '+Hcontrib
        project        = content.find(u'h4', attrs={'id': u'projetname'})
        project.string = Hname
        contentxml     = soupXml.find(u'mtl:content')
        articlesxml    = contentxml.findAll(u'entry')
        articleshtml   = souphtml.find(u'div', attrs={'id': u'mtl:articles'})
        for x in articlesxml : articleshtml.append(x)
        listlemme      = souphtml.find(u'ul', attrs={'id': u'list-articles'})
        for x in articlesxml :
            art     = x.get_text()
            idart   = x.get('id')
            lem     = ' '.join(re.split(ur'(\s)',art)[0:3]) 
            
            lemme   = BeautifulSoup(u'<li class="w3-hover-light-grey" ><span class="lemme" onclick="changeImage('+u"'"+idart+u"'"+u')">'+lem+u'</span><span class="fa fa-plus w3-closebtn" onclick="add('+u"'"+idart+u"'"+u')"/></li>', 'html5lib')
            listlemme.append(lemme.find(u'li'))
            
        filetemplate.close()
        self.resultHtml = souphtml.prettify("utf-8")
        return self.resultHtml
    
     

class baliseXML ():
    """
      Build XML file type (xml|tei|lmf) with global metadata of the project
      @param:   typ:str 
      @return:  obj:instance of baliseXML
    """
    
    def __init__(self, typ="xml") :
        self.typ = typ
        
    def buildStructure(self, data, Sfile=None, typ=u'dtd'):
        return False

    def xmlised(self, typ=u'xml', save=False) :
        """
          Create well formed (xml|tei|lmf) file with metadata and content xml 
          @return: metalexXml
        """
        metadata   = self.xmlMetadata()
        content    = self.xmlContent(forme=u'text')
        if typ == u'xml' :
            if save :
                name = u'MetaLex-'+MetaLex.projectName+u'.xml'
                metalexXml = self.balise(metadata+content, u'MetaLexProject', attr={'xmlns:mtl':'https://www.w3schools.com/MetaLex'})
                if MetaLex.dicProject.inDir(name) :
                    with codecs.open(name, 'w', 'utf-8') as fle :
                        fle.write(metalexXml)
                    message = u"'"+name+u"'  is created and contain all dictionary articles formated in xml standard format > Saved in dicTemp folder"
                    MetaLex.dicLog.manageLog.writelog(message)
                else:
                    message = u"'"+name+u"'  is created and contain all dictionary articles formated in xml standard format > Saved in dicTemp folder"
                    print message
                    #MetaLex.dicLog.manageLog.writelog(message)
                return metalexXml
            else :
                metalexXml = self.balise(metadata+content, u'MetaLexProject', attr={'xmlns:mtl':'https://www.w3schools.com/MetaLex'})
                return metalexXml
            

    def xmlMetadata(self, typ=u'xml'):
        """
          Create xml metadata file with configuration of the project 
          @return:  str:metadata
        """
        MetaLex.dicProject.createtemp()
        if typ == u'xml' :
            projectconf = MetaLex.dicProject.readConf()
            author      = self.balise(projectconf['Author'], u'mtl:author')
            name        = self.balise(projectconf['Projectname'], u'mtl:projectname')
            date        = self.balise(projectconf['Creationdate'], u'mtl:date')
            comment     = self.balise(projectconf['Comment'], u'mtl:comment')
            contribtab  = projectconf['Contributors'].split(u',') if projectconf['Contributors'].find(u',') else projectconf['Contributors']
            contrib = ''
            if len(contribtab) > 1 :
                for data in contribtab :
                    contrib += self.balise(data, u'mtl:pers') 
            else :
                contrib = self.balise(''.join(contribtab), u'mtl:pers') 
            contrib  = self.balise(contrib, u'mtl:contributors')
            cont     = name+author+date+comment+contrib
            metadata = self.balise(cont, u'mtl:metadata') 
            return metadata
        if typ == u'lmf' :
            return False
            
            
    def xmlContent(self, forme, typ=u'xml'): 
        """
          Create xml content file (representing articles) with data articles extracting
          @return: str:contentXml
        """
        content     = u''
        contentXml  = u''
        if typ == u'xml' :
            if forme == u'pickle' : 
                data = getDataArticles(u'pickle')
                for dicart in data :
                    for art in dicart.keys() :
                        art = self.balise(dicart[art], u'entry', art=True)
                        content += art
                contentXml = self.balise(content, u'mtl:content')
                return contentXml
            if forme == u'text' : 
                data = getDataArticles(u'text')
                cod = structuredWithCodif(data, u'xml')
                co  = cod.codifiedArticles()
                print co
                for art in data.keys() :
                    art = self.balise(data[art], u'entry', art=True)
                    content += art
                contentXml = self.balise(content, u'mtl:content')
                return contentXml
        
        
        
    def balise(self, element, markup, attr=None, typ=u'xml', art=False):
        """
          Markup data with a specific format type (xml|tei|lmf)
          @return: str:balised element
        """
        if type :
            if markup in components[u'xml'][u'identification'] \
            or components[u'xml'][u'treatment'] :
                if art :
                    element = self.chevron(markup, attr, art=True)+element+self.chevron(markup, attr, False)
                    return element
                else:
                    element = self.chevron(markup, attr)+element+self.chevron(markup, attr, False)
                    return element
        elif typ == u'tei' :
            if markup in components[u'tei'][u'identification'] \
            or components[u'xml'][u'treatment'] :
                if art :
                    element = self.chevron(markup, attr, art=True)+element+self.chevron(markup, attr, False)
                    return element
                else:
                    element = self.chevron(markup, attr)+element+self.chevron(markup, attr, False)
                    return element
        elif typ == u'lmf' :
            if markup in components[u'lmf'][u'identification'] \
            or components[u'xml'][u'treatment'] :
                if art :
                    element = self.chevron(markup, attr, True)+element+self.chevron(markup, attr, False)
                    return element
                else:
                    element =self. chevron(markup, attr)+element+self.chevron(markup, attr, False)
                    return element
        else :
            if art :
                element = self.chevron(markup, attr, True)+element+self.chevron(markup, attr, False)
                return element
            else:
                element = self.chevron(markup, attr)+element+self.chevron(markup, attr, False)
                return element
    
    
    def chevron(self, el, attr, openchev=True, art=False):
        """
          Put tag around the data element
          @return: str:tagging element 
        """
        idart = generateID()
        if art and attr == None:
            if openchev     : return u"<"+el+u" id='"+idart+u"' class='data-entry'"+u">"
            if not openchev : return u"</"+el+u">"
        if art and attr != None :
            allattrib = ''
            for at in attr.keys() :
                allattrib += ' '+at+'="'+attr[at]+'"'
            if openchev     : return u"<"+el+u" id='"+idart+u"' class='data-entry'"+u' '+allattrib+u">"
            if not openchev : return u"</"+el+u">"
        elif art == False and attr != None :
            allattrib = ''
            for at in attr.keys() :
                allattrib += ' '+at+'="'+attr[at]+'"'
            if openchev     : return u"<"+el+u' '+allattrib+u">"
            if not openchev : return u"</"+el+u">"
        elif art == False and attr == None :
            if openchev     : return u"<"+el+u">"
            if not openchev : return u"</"+el+u">"
        
        
        