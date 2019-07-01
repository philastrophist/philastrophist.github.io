---
title: "AAS Job Hunter"
excerpt: "Keep track of the jobs available on AAS job register"
github: philastrophist/AAS-job-hunter
collection: projects
---
# AAS Job Hunter

Organise jobs in astronomy from the [AAS website](https://jobregister.aas.org) with the help of Google Sheets.

### Features:

* See when your deadlines are approaching ![plot](../../images/job-hunter-graph.PNG)
* Keep track of discarded or complete applications ![plot](../../images/job-hunter-completed.PNG)
* Integrate with [travis-ci](http://travis-ci.com) to automatically keep your database up to date
* No pesky to-do lists or heavy websites to host

## Installation
1. Fork this repository
1. Make a copy of the spreadsheet [here](https://docs.google.com/spreadsheets/d/1XX8PU3nuFPVLojfWhbhnhc3yuM3pmfNK6qiN1wheQQI/edit?usp=sharing)
(not updated)
1. Save the `SPREADSHEET_ID` as an environment variable
1. Save the required `MAILGUN` environment variables for notifications (or modify that bit)
1. run `python sheets.py` to get authorised with google (it will tell you what to do)
1. run `python run.py` to update the google sheet!

#### Travis integration
1. Set all environment variables you used above as secret keys in travis settings
1. run `gem install travis`
1. run `travis encrypt-file token.pickle [--pro]`
1. Update the .travis.yml file like it tells you. Something like `openssl aes-256-cbc -K $encrypted_040c7bfba308_key -iv $encrypted_040c2s1d3a42s_iv -in token.pickle.enc -out token.pickle -d`
1. Set cron job in travis settings to run every day!

Done! 