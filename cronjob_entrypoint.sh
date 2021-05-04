#!/bin/bash

# set district ids of interest.
DISTRICT_IDS=146,147

#replace with relevant age
AGE=33


#needed for notifications to work
export XDG_RUNTIME_DIR=/run/user/$(id -u)

#replace with actual path of source code
cd ~/personal/cowinchecker

#replace with your `workon` home
export WORKON_HOME=~/.virtualenvs

#replace with path to virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh

#replace with name of your virtualenv
workon cowinchecker

bash cowinscraper.sh $DISTRICT_IDS $AGE