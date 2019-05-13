#!/bin/bash -x
set -e

wget https://github.com/jgm/pandoc/releases/download/2.7.2/pandoc-2.7.2-1-amd64.deb
sudo dpkg -i pandoc-2.7.2-1-amd64.deb
rm pandoc-2.7.2-1-amd64.deb
pip3 install pypandoc pyyaml requests ads
python3 _generator/update.py

if git status --porcelain | grep latex/ | grep -v "*.pdf"; then 
  # do latex stuff
  cd _latex
  ../latexdockercmd.sh xelatex -interaction nonstopmode cv-shauncread.tex
  cp cv-shauncread.pdf ../cv.pdf
  cd ..
fi



