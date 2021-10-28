#!/usr/bin/env python3
from fire import Fire
import psycopg2
import json

def get(siteName: str, envType: str = 'nonprod'):
  users = []
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
      SELECT email FROM rp_master."user"
    '''
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
      for field in row:
        users.append(field)
    
    return users
  except Exception as err:
    print('getSiteUsers.error', err)
    raise err

if __name__ == '__main__':
  Fire(get) 

# Usage
## python3 getFeVersion.py --siteName=south-lane