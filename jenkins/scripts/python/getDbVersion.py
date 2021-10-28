#!/usr/bin/env python3
from fire import Fire
import psycopg2
import json

def get(siteName: str, envType: str = 'nonprod', region: str = 'us-east-2'):

  version = []
  domain = 'cr5mzwdlkiuv.us-east-2.rds.amazonaws.com'
  # This is a temporary fix for sites hosted in Region eu-west-3
  if region == 'eu-west-3':
    domain = 'cnps54oq41tx.eu-west-3.rds.amazonaws.com'
  if envType == 'prod':
    domain = 'ctspwoqaxc3p.us-east-2.rds.amazonaws.com'
  dbHost = f'athena-{siteName}-rds.{domain}'
  dbPort = '5432'
  dbUser = 'edulog'
  dbPass = 'edul0g'
  dbName = 'Athena'

  try:
    con = psycopg2.connect(database=dbName, user=dbUser, password=dbPass, host=dbHost, port=dbPort)
    cur = con.cursor()
    query = f'''
      SELECT 
        (SELECT version FROM public.flyway_schema_history ORDER BY installed_rank DESC LIMIT 1) AS athena_version
    '''
        # (SELECT sql_version FROM public.geo_tenant_info) AS geocode_version
        # (SELECT sql_version FROM public.ivin_tenant_info) AS ivin_version,
        # (SELECT sql_version FROM public.edta_tenant_info) AS edta_version
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
      for field in row:
        version.append(field)
    
    return ','.join(version)
  except Exception as err:
    print('getDbVersion.error', err)
    raise err

if __name__ == '__main__':
  Fire(get) 

# Usage
## python3 getFeVersion.py --siteName=south-lane