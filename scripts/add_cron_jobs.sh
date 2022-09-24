#!/bin/bash

BASEDIR="$(dirname ${BASH_SOURCE})"
if [ ! ${BASEDIR:0:1} == / ]; then
  BASEDIR="$(pwd)/$BASEDIR"
fi

crontab -l | { cat; echo "# add morning jobs"; } | crontab -
crontab -l | { cat; echo "50 7 * * * /usr/bin/python3 \"$BASEDIR/../onedrive-upload/refresh_token.py\""; } | crontab -
crontab -l | { cat; echo "0 8 * * * sh \"$BASEDIR/create_influx_backup.sh\""; } | crontab -
crontab -l | { cat; echo "10 8 * * * sh \"$BASEDIR/upload.sh\""; } | crontab -
crontab -l | { cat; echo "# add evening jobs"; } | crontab -
crontab -l | { cat; echo "50 19 * * * /usr/bin/python3 \"$BASEDIR/../onedrive-upload/refresh_token.py\""; } | crontab -
crontab -l | { cat; echo "0 20 * * * sh \"$BASEDIR/create_influx_backup.sh\""; } | crontab -
crontab -l | { cat; echo "10 20 * * * sh \"$BASEDIR/upload.sh\""; } | crontab -
