#!/usr/bin/env python3
from fire import Fire
from lib_connect_aws import connect

# handler goes here
def add(envType: str = 'nonprod', region: str = 'us-east-2'):
  # Production Site List
  dbPass = '2ASU0sGt9UXz'
  cloudfrontIdsList = [
    'caddo-community',
    'chiefleschi-mvp-2',
    'chiefleschi-mvp',
    'edulog-training',
    'edulogsales',
    'emmett-id',
    'frenchtown-1',
    'frenchtown-2',
    'manitouspring',
    'mattoon-il',
    'midlandpublicschools',
    'redlakemn',
    'santaritaca-ca',
    'south-lane',
    'uat01',
    'uat02',
  ]

  # NonProd Site List
  # dbPass = 'rU18iWV4qxKU'
  # cloudfrontIdsList = [
  #   'smokeleg',
  #   'e2esdi',
  #   'edulogsales',
  #   'emmetidaho',
  #   'frenchtown-5',
  #   'frenchtown-demo',
  #   'frenchtown-sales-1',
  #   'frenchtown-sales',
  #   'frenchtown-transfers',
  #   'manitou-co-internal',
  #   'midland',
  #   'missoula5',
  #   'missoula6',
  #   'missoula7',
  #   'missoula8',
  #   'missoulacloud1',
  #   'missoulacloud2',
  #   'missoulacloud3',
  #   'missoulacloud4',
  #   'opt-release-2',
  #   'opt-release',
  #   'release-3',
  #   'release-2',
  #   'south-lane',
  #   'telematics-demo',
  #   'telematics',
  #   'telematics-sales',
  #   'test-deployment-1',
  #   'test-deployment-2',
  #   'test-deployment-3',
  #   'test-deployment-4',
  #   'vb-e1',
  #   'vb-e3',
  #   'vb',
  #   'vb-sales',
  #   'vb-static',
  #   'vb-staticdynamic',
  # ]
  awsProfile = 'default'
  if envType == 'prod':
    awsProfile = 'prod'

  try:

    SSM = connect(service='ssm', region=region, profile=awsProfile)
    for siteName in cloudfrontIdsList:
      name = f'/edulog/athena/{envType}/{siteName}/db_pass'
      value = dbPass
      resp = SSM.put_parameter(Name=name, Value=value, Type='SecureString', Overwrite=True)
      print(siteName, dbPass, resp)
  
  except Exception as err:
    print('addCloudFrontId.error', err)
    raise err


if __name__ == '__main__':
  Fire(add) 