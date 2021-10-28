#!/usr/bin/env python3
from fire import Fire
from lib_connect_aws import connect
import json

def get(siteName: str, envType: str = 'nonprod', region: str = 'us-east-2'):
  version = ''
  domain = 'athena-nonprod.com'
  awsProfile = 'default'
  s3Bucket = ''
  versionFilePath = ''

  if envType == 'prod':
    domain = 'etstack.io'
    awsProfile = 'prod'

  s3Bucket = '{}.{}'.format(siteName, domain)
  versionFilePath = 'assets/systemconfig.json'

  try:
    s3 = connect(service='s3', region=region, profile=awsProfile)
    resp = s3.get_object(Bucket=s3Bucket, Key=versionFilePath)
    version = json.loads(resp.get('Body').read()).get('version')

    return version
  except Exception as err:
    print('getFeVersion.error', err)
    raise err

if __name__ == '__main__':
  Fire(get) 

# Usage
## python3 getFeVersion.py --siteName=south-lane