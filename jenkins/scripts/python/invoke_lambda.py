#!/usr/bin/env python3
from fire import Fire
import json
import boto3
from botocore.config import Config

def connect(envType: str = 'nonprod', region: str = 'us-east-2'):
  if envType == 'prod':
    session = boto3.Session(profile_name=envType, region_name=region)
  else:
    session = boto3.Session(region_name=region)

  LD = session.client('lambda')
  return LD

# handler goes here
def invoke(name: str, eventFile: str, envType: str = 'nonprod', region: str = 'us-east-2'):
  try:
    with open(eventFile, 'r') as f:
      event = json.loads(f.read())
      LD = connect(envType, region)

      resp = LD.invoke(FunctionName=name, Payload=json.dumps(event))
      payload = json.loads(resp['Payload'].read().decode("utf-8"))
      if payload.get('statusCode') != 200:
        raise Exception(payload.get('body').get('message'))

  except Exception as err:
    print('Invoke.error', err)
    raise err

if __name__ == '__main__':
  Fire(invoke) 
