#!/bin/bash

INFLUX_BACKUP_FILE=../influx-backup.tar.gz
INFLUX_BACKUP_NAME=upc-influx-backup.tar.gz

/usr/bin/python3 ../internet-monitoring/upload_data.py -s INFLUX_BACKUP_FILE -d $INFLUX_BACKUP_NAME
