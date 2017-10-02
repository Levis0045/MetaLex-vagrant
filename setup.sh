#!/usr/bin/env bash

#    MetaLex is general tool for lexicographic and metalexicographic activities
#    Copyright (C) 2017  by Elvis MBONING

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
#    Contact : levismboning@yahoo.fr
    
#    --------------------------------------------------------------------------



#Install mains packages
sudo apt-get install vagrant
sudo apt-get install virtualbox

#Get MetaLex-vagrant from the official repository
git clone git@github.com:Levis0045/MetaLex-vagrant.git
cd MetaLex-vagrant

#Get MetaLex from the official repository
git clone git@github.com:Levis0045/MetaLex.git

#Install MetaLex's dependencies
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
sudo pip install Cython
sudo apt-get install libtesseract-dev libleptonica-dev libjpeg-dev zlib1g-dev libpng-dev
sudo apt-get install tesseract-ocr-all
sudo apt-get install python-html5lib
sudo apt-get install python-lxml
sudo apt-get install python-bs4
sudo pip install pillow
sudo pip install termcolor
sudo CPPFLAGS=-I/usr/local/include pip install tesserocr
    
#Build vagrant machine with all dependencies
vagrant up   

#Update the vagrant box
vagrant box update 

#Connect to ubuntu xenia development
vagrant ssh  

cd /vagrant
cd Metalex-vagrant