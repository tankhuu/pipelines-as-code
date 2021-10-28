#!/bin/bash
db_host=$1
postgres_pass=$2
snapshot_path=$3
db_name="Athena"
user="edulog"
schema=""

echo $db_host
echo $postgres_pass
echo $snapshot_path

aws s3 cp $snapshot_path .

export PGPASSWORD=$postgres_pass

echo "=> Drop Database on Dest"
psql -U postgres -h $db_host -c "ALTER DATABASE \""${db_name}"\" OWNER TO postgres";
psql -U postgres -h $db_host -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '${db_name}';"
psql -U postgres -h $db_host -c "DROP DATABASE \"${db_name}\""

echo "=> Recreate Database on Dest"
psql -U postgres -h $db_host -c "CREATE DATABASE \"${db_name}\";" 
psql -U postgres -h $db_host -c "CREATE EXTENSION postgis;" $db_name

ls -l
psql -U postgres -h $db_host -d "Athena" -f *.bak

# Update previleges for user in DB
psql -U postgres -h $db_host -c "ALTER DATABASE \""${db_name}"\" OWNER TO "${user}"";

psql -U postgres -h $db_host -c "GRANT ALL PRIVILEGES ON DATABASE \""${db_name}"\" to "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT USAGE ON SCHEMA geo_master TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON SCHEMA geo_master TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA geo_master TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA geo_master TO "${user}"";

psql -U postgres -h $db_host -d ${db_name} -c "GRANT USAGE ON SCHEMA public TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON SCHEMA public TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "${user}"";

psql -U postgres -h $db_host -d ${db_name} -c "GRANT USAGE ON SCHEMA settings TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON SCHEMA settings TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA settings TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA settings TO "${user}"";

psql -U postgres -h $db_host -d ${db_name} -c "GRANT USAGE ON SCHEMA edta TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON SCHEMA edta TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA edta TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA edta TO "${user}"";

psql -U postgres -h $db_host -d ${db_name} -c "GRANT USAGE ON SCHEMA rp_master TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON SCHEMA rp_master TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA rp_master TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA rp_master TO "${user}"";

psql -U postgres -h $db_host -d ${db_name} -c "GRANT USAGE ON SCHEMA ivin TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON SCHEMA ivin TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA ivin TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA ivin TO "${user}"";

psql -U postgres -h $db_host -d ${db_name} -c "GRANT USAGE ON SCHEMA geo_plan TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON SCHEMA geo_plan TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA geo_plan TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA geo_plan TO "${user}"";

psql -U postgres -h $db_host -d ${db_name} -c "GRANT USAGE ON SCHEMA rp_plan TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON SCHEMA rp_plan TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA rp_plan TO "${user}"";
psql -U postgres -h $db_host -d ${db_name} -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA rp_plan TO "${user}"";

# Update owner for Athena Schemas
# geo_plan | public | rp_master | rp_plan | settings
schema="geo_plan"
for table in `psql -U postgres -h $db_host -tc "select tablename from pg_tables where schemaname = '${schema}';" ${db_name}` ; do  psql -U postgres -h $db_host -c "alter table ${schema}.${table} owner to ${user}" ${db_name} ; done
schema="geo_master"
for table in `psql -U postgres -h $db_host -tc "select tablename from pg_tables where schemaname = '${schema}';" ${db_name}` ; do  psql -U postgres -h $db_host -c "alter table ${schema}.${table} owner to ${user}" ${db_name} ; done
schema="public"
for table in `psql -U postgres -h $db_host -tc "select tablename from pg_tables where schemaname = '${schema}';" ${db_name}` ; do  psql -U postgres -h $db_host -c "alter table ${schema}.${table} owner to ${user}" ${db_name} ; done
schema="rp_master"
for table in `psql -U postgres -h $db_host -tc "select tablename from pg_tables where schemaname = '${schema}';" ${db_name}` ; do  psql -U postgres -h $db_host -c "alter table ${schema}.${table} owner to ${user}" ${db_name} ; done
schema="rp_plan"
for table in `psql -U postgres -h $db_host -tc "select tablename from pg_tables where schemaname = '${schema}';" ${db_name}` ; do  psql -U postgres -h $db_host -c "alter table ${schema}.${table} owner to ${user}" ${db_name} ; done
schema="settings"
for table in `psql -U postgres -h $db_host -tc "select tablename from pg_tables where schemaname = '${schema}';" ${db_name}` ; do  psql -U postgres -h $db_host -c "alter table ${schema}.${table} owner to ${user}" ${db_name} ; done

# Change owner 