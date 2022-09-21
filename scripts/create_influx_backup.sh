#!/bin/bash

INFLUX_BACKUP=../influx-backup
INFLUX_BACKUP_FILE=../influx-backup.tar.gz

if [ ! -d ../]
mkdir -p
rm -rf $INFLUX_BACKUP/*
rm -f $INFLUX_BACKUP_FILE
DOCKER_INFLUX=`docker ps | grep influxdb | cut -c 1-12`
docker exec "$DOCKER_INFLUX" influxd backup -portable /data-backup
tar -czvf $INFLUX_BACKUP_FILE $INFLUX_BACKUP/*
