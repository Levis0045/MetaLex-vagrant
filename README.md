# MetaLex-vagrant 
MetaLex is general tool for **lexicographics** and **metalexicographics** activities.
For current developpement version of this tool, see [MetaLex-vagrant/v0.2](https://github.com/Levis0045/MetaLex-vagrant/tree/v0.2)

[![Build Status](https://travis-ci.org/claroline/Distribution.svg?branch=master)](mteprojet.fr/MetaLex-vagrant)

# Requirements
MetaLex-vagrant is developped in **Python 2.7** and vagrant environment, these packages are required :


```sh
    sudo apt-get install vagrant
    sudo apt-get install virtualbox
    git clone git@github.com:Levis0045/MetaLex-vagrant.git
    cd MetaLex-vagrant
    vagrant up   #Build vagrant machine with all dependencies
    vagrant ssh  #Connect to ubuntu xenia development
    cd /vagrant
    cd Metalex-vagrant
```

# Usage


- Usage situation

```
    I am a metalexicographer or linguist and I have printed dictionaries. I wish to make a diachronic metalexicographics studies to
    the evolution of the formulations of the definitions of a collection of dictionaries available from period A to period B.
    
    Traditionally or at best, the contemporary metalexicographer(according to our point of view) would apply successively the following methodology:
    
    - Scanning of printed materials (Scan)
    - Optical reading of the supports (Ocrisation)
    - Manual Error Corrections
    - Marking of the articles obtained
    - Metalexographical analysis / decryption of articles
    
    
    This is an example of process used with MetaLex ! Some other more complex process can be done !

```


- Global usage commands line
  
```sh

    python MetaLex.py -h
    
```

```md

   MetaLex arguments :
   
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -p PROJECTNAME, --project PROJECTNAME
                        Defined MetaLex project name
  -c author comment contributors, --confproject author comment contributors
                        Defined MetaLex configuration for the current project
  -i [IMAGEFILE], --dicimage [IMAGEFILE]
                        Input one or multiple dictionary image(s) file(s) for
                        current MetaLex project
  -d IMAGESDIR, --imagedir IMAGESDIR
                        Input folder name of dictionary image files for
                        current MetaLex project
  --imgalg actiontype value
                        Set algorithm for enhancing dictionary image files for
                        current MetaLex project (actiontype must be : constrat
                        or bright or filter)
  -r FILERULE, --filerule FILERULE
                        Defined file rules that we use to enhance quality of
                        OCR result
  -l LANG, --lang LANG  Set language for optical characters recognition and
                        others MetaLex treatment
  -s, --save            Save output result of the current project in files
  -t, --terminal        Show result of the current treatment in the terminal

```


- Virtually, go to the  **Test** folder and build the file rule. 


MetaLex take **file_Rule.dic** file which using  specific structure to enhance output text of OCR data (from image's files dictionnaries). **\W** for word replacement, **\C** for caracter replacement and **\R**  for regular expression replacement. The space between headers served to describe remplacement.

```md

    \START
    \MetaLex\project_name\type_of_project\lang\author\date
    \W
    /t'/t
    /{/f.
    /E./f.
    \C
    /i'/i
    \R
    /a-z+/ij
    \END
    
```

- Run your project with the default parameters except dictionary images data and save results


```sh
    python MetaLex.py  -d 'imagesInputFiles' -s
```

- Run your project with your own set of parameters 


```sh
    python MetaLex.py -p 'projectname' -c 'author' 'comment' 'contributors' -d 'imagesInputFiles' -r 'file_Rule.dic' -l fra -s
```

# Contributors

Special thank to [Bill](https://github.com/billmetangmo) for this version


# Reference

Please don't forget to cite this work :

```latex

    @article{Mboning-Elvis,
        title  = {Quand le TAL s'empare de la métalexicographie : conception d'un outil pour le métalexicographe},
        author = {Mboning, Elvis},
        url    = {https://github.com/Levis0045/dic/},
        date   = {2017-06-20},
        shool  = {Université de Lille 3},
        year   = {2017},
        pages  = {12},
        keywords = {métalexicographie, TAL, fouille de données, extraction d'information, lecture optique, lexicographie, Xmlisation, DTD}
    }
    
```


