#!/usr/bin/env bash

sudo apt-get update

# install jpeg/png/zlib libs
sudo apt-get -y install zlib1g-dev libpng-dev libjpeg-dev

sudo apt-get -y install build-essential libssl-dev libffi-dev

# install python dev libs
sudo apt-get -y install python-dev python-pip python-setuptools
sudo pip install --upgrade pip

sudo apt-get -y install libtesseract-dev libleptonica-dev
sudo apt-get -y  install tesseract-ocr-all
sudo apt-get -y  install python-html5lib python-lxml python-bs4

# install
sudo apt-get -y install cython
sudo pip install Cython

sudo pip install pillow
sudo pip install termcolor

sudo CPPFLAGS=-I/usr/local/include pip install tesserocr

#install
sudo apt-get install git
touch ~/.bash_profile

cat <<EOT >> ~/.bash_profile
parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
export PS1="\u@\h \[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] $ "
EOT

cat <<EOT >> ~/.bashrc
# to have git branch in bash prompt
. ~/.bash_profile
EOT

git config --global user.email "you@example.com"
git config --global user.name "Your Name"
