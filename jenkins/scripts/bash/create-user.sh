#!/bin/bash
db_host=$1
postgres_pass=$2

export PGPASSWORD=$postgres_pass
psql -U postgres -h $db_host -d "Athena" -f create-user.new.sql