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
npages="$(pdfinfo cv.pdf | grep Pages | awk '{print $2}')"

if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then
  # Force push the paper to GitHub orphaned branch
  cd $TRAVIS_BUILD_DIR
  git checkout --orphan "$TRAVIS_BRANCH-PR$TRAVIS_PULL_REQUEST"
  git -c user.name='travis' -c user.email='travis' commit -m "pull request build"
  git push -q -f https://$GITHUB_USER:$GITHUB_API_KEY@github.com/$TRAVIS_REPO_SLUG "$TRAVIS_BRANCH-PR$TRAVIS_PULL_REQUEST"
  curl -i -H "Authorization: token $GITHUB_API_KEY" \
    -H "Content-Type: application/json" \
    -X POST -d "{\"body\":\"https://github.com/$TRAVIS_REPO_SLUG/tree/$TRAVIS_BRANCH-PR$TRAVIS_PULL_REQUEST\"}" \
    https://api.github.com/repos/$TRAVIS_REPO_SLUG/issues/$TRAVIS_PULL_REQUEST/comments
fi


if [[ "$npages" -gt  "$ALLOWED_CV_PAGES" ]]; then
	echo "cv has more than $npages pages"
	exit 1
fi