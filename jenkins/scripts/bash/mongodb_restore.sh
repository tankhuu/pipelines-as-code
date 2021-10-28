#!/bin/bash

env=$1
siteName=$2
mongoHost=$3
bkFilePath=$4

aws s3 cp $bkFilePath .
mongo --host $mongoHost < mongodb_drop_database.js
mongorestore --host $mongoHost --gzip --archive=$(ls mongodb-*.gz) > /dev/null
if [ $? -gt 0 ]; then
  exit 1
fi
