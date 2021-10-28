#!/bin/bash
AWS_CMD=$1
NAME=$2
VALUE=$3
TYPE=$4
REGION=$5

if [ $REGION = 'eu-west-3' ]; then
  AWS_CMD="$AWS_CMD --region $REGION"
fi

$AWS_CMD ssm put-parameter --overwrite --cli-input-json "{\"Name\":\"$NAME\",\"Value\":\"$VALUE\",\"Type\":\"$TYPE\"}"