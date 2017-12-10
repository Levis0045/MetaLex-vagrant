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


sudo apt-get update

# install jpeg/png/zlib libs
sudo apt-get -y install zlib1g-dev libpng-dev libjpeg-dev

sudo apt-get -y install build-essential libssl-dev libffi-dev

# install python dev libs
sudo apt-get -y install python-dev python-pip python-setuptools
sudo pip install --upgrade pip

sudo apt-get -y install libtesseract-dev libleptonica-dev
sudo apt-get -y install tesseract-ocr-all
sudo apt-get -y install python-html5lib python-lxml python-bs4

# install
sudo apt-get -y install cython
sudo pip install Cython

sudo pip install pillow
pip install http://effbot.org/downloads/Imaging-1.1.7.tar.gz
sudo pip install termcolor

sudo CPPFLAGS=-I/usr/local/include pip install tesserocr

#install
sudo apt-get install git
touch ~/.bash_profile

# install web file manager with docker
sudo apt-get -y install docker.io
sudo systemctl start docker
sudo usermod -aG docker ubuntu
sudo docker run -d -t --net=host --rm -v ~:/root -v /:/mnt/fs coderaiser/cloudcmd

cat <<EOF >> ~/.bash_profile
parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
export PS1="\u@\h \[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] $ "
EOF

cat <<EOF >> ~/.bashrc
# to have git branch in bash prompt
. ~/.bash_profile
EOF

git config --global user.email "you@example.com"
git config --global user.name "Your Name"
