#!/bin/bash -x
# update the site from UPDATE_BRANCH. Adds a new commit to LIVE_BRANCH after every new commit on UPDATE_BRANCH.
# set a cron job to run on LIVE_BRANCH
set -e


#! /bin/bash 
set -e

wget https://github.com/jgm/pandoc/releases/download/2.7.2/pandoc-2.7.2-1-amd64.deb
sudo dpkg -i pandoc-2.7.2-1-amd64.deb
rm pandoc-2.7.2-1-amd64.deb
pip3 install pypandoc pyyaml requests ads
python3 generator/update.py

if git status --porcelain | grep latex/ | grep -v "*.pdf"; then 
  # do latex stuff
  cd latex
  ../latexdockercmd.sh xelatex -interaction nonstopmode cv-shauncread.tex
  cd ..
fi



