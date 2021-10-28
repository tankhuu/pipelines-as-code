#!/bin/bash -xe

# VARIABLES #
SERVICE=$1
SERVICE_NAME=$2
BUILD_VERSION=$3
S3_PATH=$4
S3_ARTIFACTS="edulog-athena-artifacts"
BASE_DIR="/opt/athena/src"
VER_DIR="/opt/athena/versions"

# EXECUTE #
echo $SERVICE
echo $SERVICE_NAME
echo $BUILD_VERSION
echo $S3_PATH

cd $BASE_DIR
# Pull service src from S3
aws s3 cp $S3_PATH ./${SERVICE_NAME}.jar
# Versioning Service
mkdir -p $VER_DIR
cd $VER_DIR
# Backup previous version of service
cp -p ${SERVICE_NAME} ${SERVICE_NAME}.prev
echo "${BUILD_VERSION}" > ${SERVICE_NAME}

# Apply service
echo `date`
echo "Restarting ${SERVICE} ..."
sudo systemctl restart ${SERVICE}
echo `date`

