# MetaLex-vagrant 
MetaLex is general tool in AGPL Licence for `lexicographics` and `metalexicographics` activities.
For current developpement version of this tool, see [MetaLex/v1.0](https://github.com/Levis0045/MetaLex/tree/v1.0) 
or see [MetaLex-vagrant/v1.0](https://github.com/Levis0045/MetaLex-vagrant/tree/v1.0)


[![Build Status](https://travis-ci.org/claroline/Distribution.svg?branch=master)](mteprojet.fr/MetaLex-vagrant)


# Usage


- This is an example of process used with MetaLex 

```
    I am a metalexicographer or linguist and I have paper dictionaries. 
    I want to perform a diachronic study of the evolution of the wording of 
    definitions in a collection of dictionaries available from period A to period B.
```

- Traditionally or at best, the contemporary metalexicographer (according to our point of view)
  would apply the following methodology :
  
```
    1- Scanning of printed materials (Scan) and enhance its qualities
    2- Optical reading of the pictures (Ocrisation) = extract articles content 
    3- Manual Error Corrections  of text articles                   
    4- Marking of the articles with regular standard                 
    5- Metalexographical analysis / decryption of articles 
```

- metalex through its modules operates in the same way by successively executing 
  each of these tasks automatically.
  
```
    1 = MetaLex enhances the quality of dictionary images 
        **metalex.ocrtext.normalizeImage.EnhanceImages().filter(f.DETAIL)**
    2 = MetaLex extract from dictionary images all dictionary articles 
        **metalex.ocrtext.make_ocr.image_to_text()**
    3 = MetaLex corrects dictionary articles 
        **metalex.ocrtext.make_text_well()**
    4 = MetaLex marking dictionary articles depending of some standard 
        **metalex.xmlised.put_xml('tei') or MetaLex.xmlised.put_xml('lmf')**
    5 = MetaLex generates some metalexicographics analysis of part of content dictionary 
        **metalex.xmlised.handleStat()**
```

- Some other more complex processes can be done !


# Requirements

MetaLex-vagrant is developped in `Python 2.7` and vagrant environment, these packages are required :

- We can install all package dependencies manually

```sh
    sudo apt-get install vagrant
    sudo apt-get install virtualbox
    git clone git@github.com:Levis0045/MetaLex-vagrant.git
    cd MetaLex-vagrant
    git clone git@github.com:Levis0045/MetaLex.git
    vagrant box update    # Update the vagrant box
    vagrant up   # Build vagrant machine with all dependencies
    vagrant ssh  # Connect to ubuntu xenia development
    cd /vagrant

```

- Or we can use `setup.sh` to install all package dependencies : `Make sure to execute this file in the current system partition ext4 otherwise right permission will be raised in NTFS partition`
  
```sh
    sudo ./setup.sh
    sudo pip install --no-cache-dir -I pillow
```

# How to run MetaLex ?

- Virtually, go to the  `test/` folder. Re-install `pillow` to fix Image module functionalities and build documentation 
  
```sh
    
    python runMetalex.py -h

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
                        others MetaLex treatments
  -s, --save            Save output result of the current project in files
  -t, --terminal        Show result of the current treatment in the terminal

```


- Build the file rules of the project. 


MetaLex takes `file_Rule.dic` file which using  specific structure to enhance output text of OCR data (from dictionnary images files). `\W` for words replacement, `\C` for caracters replacement and `\R`  for regular expressions replacement. The spaces between headers served to describe remplacement.

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
    python runMetalex.py  -d 'imagesInput' -s   # We defined a folder containing dictionnary images for current treatment 
    python runMetalex.py  -i 'imagedic.png' -s  # Or you can also defined a single dictionnary image
```

- Run your project with your own set of parameters and save results


```sh
    python runMetalex.py -p 'projectname' -c 'author' 'comment' 'contributors' -d 'imagesInput' -r 'file_Rule.dic' -l 'fra' -s
```

# Contributors

Special thank to [Bill](https://github.com/billmetangmo) for this version


# Reference

Please don't forget to cite this work :

```latex

    @article{Mboning-Elvis,
        title  = {Quand le TAL s'empare de la métalexicographie : conception d'un outil pour le métalexicographe},
        author = {Mboning, Elvis},
        url    = {https://github.com/Levis0045/MetaLex-vagrant},
        date   = {2017-06-20},
        shool  = {Université de Lille 3},
        year   = {2017},
        pages  = {12},
        keywords = {métalexicographie, TAL, fouille de données, extraction d'information, lecture optique, lexicographie, Xmlisation, DTD}
    }
    
```


