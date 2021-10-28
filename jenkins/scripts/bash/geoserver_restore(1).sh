#!/bin/bash -e

siteName=$1
bkPath=$2
runDate=`date +%Y%m%d-%H%M%S`

# Download backup files from S3
rm -rf /opt/athena/data/restore/
mkdir -p /opt/athena/data/restore/
cd /opt/athena/data/restore/
aws s3 cp --recursive $bkPath .

# Stop GeoServer & Overlay Services
docker stop geoserver
sudo systemctl stop overlay

# Restore data into 
cd ..
mv geoserver/ geoserver-$runDate
mv restore/ geoserver
sudo chown -R ubuntu: geoserver

docker start geoserver
docker ps
sudo systemctl start overlay
