#!/bin/bash

BASEDIR="$(dirname ${BASH_SOURCE})"
if [ ! ${BASEDIR:0:1} == / ]; then
  BASEDIR="$(pwd)/$BASEDIR"
fi

INFLUX_BACKUP_FILE="$BASEDIR/../influx-backup.tar.gz"
INFLUX_BACKUP_NAME="upc-influx-backup.tar.gz"

/usr/bin/python3 "$BASEDIR/../onedrive-upload/upload_data.py" -s "$INFLUX_BACKUP_FILE" -d "$INFLUX_BACKUP_NAME"
