#!/bin/bash -e

siteName=$1
envType=$2
runDate=`date +%Y%m%d-%H%M%S`
s3Bucket="edulog-athena-backup"
if [ $envType = 'prod' ]; 
then
  s3Bucket="edulogvn-backup"
fi

# Backup to S3
sudo aws s3 cp --recursive /opt/athena/data/geoserver/ s3://$s3Bucket/athena/data/$siteName/geoserver/$runDate/
echo "BackupPath: s3://$s3Bucket/athena/data/$siteName/geoserver/$runDate/"
