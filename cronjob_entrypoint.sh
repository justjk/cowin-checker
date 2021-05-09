#!/bin/bash

# set district ids of interest.
DISTRICT_IDS=307,301,303,304

#replace with relevant age
AGE=45


#needed for notifications to work
export XDG_RUNTIME_DIR=/run/user/$(id -u)

#uncomment below and set value. needed for telegram notifications to work
# export COWIN_CHECKER_TELEGRAM_CHANNEL_ID=<channel id>
# export COWIN_CHECKER_TELEGRAM_BOT_TOKEN=<bot token>

#replace with actual path of source code
cd ~/personal/cowinchecker

#replace with your `workon` home
export WORKON_HOME=~/.virtualenvs

#replace with path to virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh

#replace with name of your virtualenv
workon cowinchecker

bash cowinscraper.sh $DISTRICT_IDS $AGE