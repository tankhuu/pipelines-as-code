#!/usr/bin/env python3
from fire import Fire
from lib_connect_aws import connect
import json

def get(siteName: str, envType: str = 'nonprod', region: str = 'us-east-2'):
  version = ''
  domain = 'athena-nonprod.com'
  awsProfile = 'default'
  if envType == 'prod':
    domain = 'etstack.io'
    awsProfile = 'prod'
  stackName = 'athena-{}'.format(siteName)

  try:
    beAmiId = ''
    cfn = connect(service='cloudformation', region=region, profile=awsProfile)
    stack = cfn.describe_stacks(StackName=stackName)
    if stack:
      params = stack.get('Stacks')[0].get('Parameters')
      if params:
        for p in params:
          if p.get('ParameterKey') == 'BackendAMIId':
            beAmiId = p.get('ParameterValue').strip()
    if beAmiId:
      ec2 = connect(service='ec2', region=region, profile=awsProfile)
      images = ec2.describe_images(ImageIds=[beAmiId])
      if images:
        image = images.get('Images')[0]
        tags = image.get('Tags')
        version = list(filter(lambda t: t['Key'] == 'release_version', tags))[0].get('Value')

    return version
  except Exception as err:
    print('getBeVersion.error', err)
    raise err

if __name__ == '__main__':
  Fire(get) 

# Usage
## python3 getBeVersion.py --siteName=south-lane