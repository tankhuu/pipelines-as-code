#!/bin/bash -xe

TENANT=$1
ENV_TYPE=$2
DB_PASS=$3
REGION=$4

DB_NAME="Athena"
DB_USER="postgres"
PATH_SCRIPT="Athena-DBScripts/sql/script_verify_athena_db_after_deploy.sql"

if [[ ${ENV_TYPE} == "nonprod" ]]
then
#  DB_PASS="rU18iWV4qxKU"
  RDS_EP=$(aws ssm get-parameter --name /edulog/athena/${ENV_TYPE}/${TENANT}/rds_endpoint --output text --query 'Parameter.[Value]' --region ${REGION})
else
#  DB_PASS="2ASU0sGt9UXz"
  RDS_EP=$(aws ssm get-parameter --name /edulog/athena/${ENV_TYPE}/${TENANT}/rds_endpoint --output text --query 'Parameter.[Value]' --region ${REGION} --profile prod)
fi

export PGPASSWORD=$DB_PASS

psql \
   --host=${RDS_EP} \
   --username=$DB_USER \
   --dbname=$DB_NAME   \
   --file=$PATH_SCRIPT