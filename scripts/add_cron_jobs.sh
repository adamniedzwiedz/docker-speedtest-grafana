#!/bin/bash

BASEDIR="$(dirname ${BASH_SOURCE})"
if [ ! ${BASEDIR:0:1} == / ]; then
  BASEDIR="$(pwd)/$BASEDIR"
fi

TMP_CRON_FILE="$(mktemp)"
crontab -l > TMP_CRON_FILE

# add morning jobs
echo "50 7 * * * /usr/bin/python3 \"$BASEDIR/../onedrive-upload/refresh_token.py\"" >> TMP_CRON_FILE
echo "0 8 * * * sh \"$BASEDIR/create_influx_backup.sh\"" >> TMP_CRON_FILE
echo "10 8 * * * sh \"$BASEDIR/upload.sh\"" >> TMP_CRON_FILE
# add evening jobs
echo "50 19 * * * /usr/bin/python3 \"$BASEDIR/../onedrive-upload/refresh_token.py\"" >> TMP_CRON_FILE
echo "0 20 * * * sh \"$BASEDIR/create_influx_backup.sh\"" >> TMP_CRON_FILE
echo "10 20 * * * sh \"$BASEDIR/upload.sh\"" >> TMP_CRON_FILE

rm $TMP_CRON_FILE
