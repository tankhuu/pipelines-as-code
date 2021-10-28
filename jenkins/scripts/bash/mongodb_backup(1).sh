#!/bin/bash

env=$1
siteName=$2
mongoHost=$3
s3Bucket=$4
bkDate=$5

s3Prefix="athena/mongodb/${env}/${siteName}"
s3Path="s3://${s3Bucket}/${s3Prefix}"
bkFile=mongodb-${siteName}.${bkDate}

mongodump --host $mongoHost --gzip --archive=$bkFile.gz > /dev/null
if [ $? -gt 0 ]; then
  exit 1
fi

if [ -s $bkFile.gz ]; then
  aws s3 cp $bkFile.gz $s3Path/
  ls -lh $bkFile.gz
  echo "
  S3_FULL_PATH: $s3Path/$bkFile.gz"
  exit 0
fi
exit 1
