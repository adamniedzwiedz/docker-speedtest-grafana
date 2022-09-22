#!/bin/bash

BASEDIR="$(dirname ${BASH_SOURCE})"
if [ ! ${BASEDIR:0:1} == / ]; then
  BASEDIR="$(pwd)/$BASEDIR"
fi

INFLUX_BACKUP_FOLDER="$(BASEDIR)/../influx-backup"
INFLUX_BACKUP_FILE="$(BASEDIR)/../influx-backup.tar.gz"

if [ -d "$INFLUX_BACKUP_FOLDER" ] && rm -rf "$INFLUX_BACKUP_FOLDER/*" || mkdir -p "$INFLUX_BACKUP_FOLDER"
if [ -f "$INFLUX_BACKUP_FILE" ] && rm -f $INFLUX_BACKUP_FILE
DOCKER_INFLUX=`docker ps | grep influxdb | cut -c 1-12`
docker exec "$DOCKER_INFLUX" influxd backup -portable /data-backup
tar -czvf "$INFLUX_BACKUP_FILE" "$INFLUX_BACKUP_FOLDER/*"
