#!/usr/bin/env python3
from fire import Fire
import psycopg2
import json

def get(siteName: str, envType: str = 'nonprod'):
  registrations = []
  domain = 'cr5mzwdlkiuv.us-east-2.rds.amazonaws.com'
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
      SELECT * FROM public.registered_command_rest_hooks
      ORDER BY application_id ASC
    '''
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
      service = row[1]
      url = row[4]
      registrations.append('{}: {}'.format(service, url))
    
    return '\n'.join(registrations)
  except Exception as err:
    print('getACDSRegistration.error', err)
    raise err

if __name__ == '__main__':
  Fire(get) 

# Usage
## python3 getFeVersion.py --siteName=south-lane