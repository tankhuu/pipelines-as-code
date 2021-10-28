#!/bin/bash

env=$1
tenant=$2
db_host=$3
db_pass=$4
s3_bucket=$5
db_name="Athena"
#bk_date=`date +%Y%m%d-%H%M%S`
bk_date=$6

bk_file=${db_name}-${tenant}.${bk_date}.bak
s3_prefix="athena/database/${env}/${tenant}"
s3_path="s3://${s3_bucket}/${s3_prefix}"

export PGPASSWORD=$db_pass;
pg_dump -U postgres -h $db_host ${db_name} > $bk_file

if [ $? -gt 0 ]; then
  exit 1
fi

if [ -s $bk_file ]; then
  aws s3 cp $bk_file $s3_path/
  echo "${s3_prefix}/$bk_file" > TMP_S3_KEY
  exit 0
fi

exit 1