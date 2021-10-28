import boto3
from botocore.config import Config

def connect(service: str = 'ec2', region: str = 'us-east-2', profile: str = 'default'):
  try:
    config = Config(region_name=region)
    session = boto3.Session(profile_name=profile)

    return session.client(service, config=config)
  except Exception as err:
    print('connect.error', err)
    raise err
