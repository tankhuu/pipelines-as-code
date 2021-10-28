#!/bin/bash

# VARIABLES #
SERVICE=$1
SERVICE_NAME=$2
BUILD_VERSION=$3
S3_PATH=$4
BASE_DIR="/opt/athena/src"
VER_DIR="/opt/athena/versions"

# EXECUTE #
cd /tmp
aws s3 cp $S3_PATH .
if [ $? -ne 0 ]; then
  echo "=> Can't Download the Artifact ${S3_PATH}"
  exit 1
fi
tar zxvf ${BUILD_VERSION}.tar.gz
mv ${BUILD_VERSION}/* $BASE_DIR


# Run DB Migration
. /opt/athena/env/athena.env
sudo java -Ddb.server=${DB_HOST} -Ddb.name=Athena -jar -XX:+UseG1GC -Xms256m -Xmx1024m ${BASE_DIR}/RoutingMigration.jar
if [ $? -ne 0 ]; then
  echo "=> RoutingMigration run failure! Please check related logs"
  exit 1
fi
# Apply Athena services
sudo systemctl restart middle
sudo systemctl restart backend
sudo systemctl restart plannedrollover
sudo systemctl restart reportsserver

# Versioning Service
cd $VER_DIR
cp -p ${SERVICE_NAME} ${SERVICE_NAME}.prev
echo "${BUILD_VERSION}" > ${SERVICE_NAME}
cat ${SERVICE_NAME}

# CLEANUP #
cd /tmp
rm -rf ${BUILD_VERSION}
rm -f ${BUILD_VERSION}.tar.gz
