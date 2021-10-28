#!/bin/bash -xe

# VARIABLES #
while getopts s: flag
do
  case "${flag}" in
    s) schedule=${OPTARG};;
    [?]) print >&2 "Usage: $0 [-s cron_schedule] file ..."
        exit 1;;
  esac
done

RUN_FILE="/opt/athena/run/plannedrollover.sh"

# EXECUTE #
echo "delete old schedule"
sed -i '14d' $RUN_FILE
# Add new Schedule
echo "add new schedule ${schedule}"
sed -i "13 a -Dplanned.rollover.cron=\"${schedule}\" \\\ " $RUN_FILE
sed -i "14s/[ \t]*$//" $RUN_FILE
cat $RUN_FILE
