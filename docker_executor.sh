#!/bin/bash

# set district ids of interest.
DISTRICT_IDS=265

#replace with relevant age
AGE=18

docker run \
    --env COWIN_CHECKER_TELEGRAM_CHANNEL_ID="<set telegram channel id>" \
    --env COWIN_CHECKER_TELEGRAM_BOT_TOKEN="<set telegram bot token>" \
    cowinchecker:latest $DISTRICT_IDS $AGE