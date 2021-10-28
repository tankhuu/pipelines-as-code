#!/usr/bin/env python3
from fire import Fire
from lib_connect_aws import connect

# handler goes here
def add(envType: str = 'nonprod', region: str = 'us-east-2'):
  # Production Site List
  # cloudfrontIdsList = {
  #   'caddo-community': 'E1U5XI0JB0MBKN',
  #   'chiefleschi-mvp-2': 'E3CQ18GF26CDTP',
  #   'chiefleschi-mvp': 'EHBPJTVP3PVYD',
  #   'edulog-training': 'EML6P7JO34YQ1',
  #   'edulogsales': 'E20NYS8J6YSRL8',
  #   'emmett-id': 'E2TBWMYLIOB9H2',
  #   'frenchtown-1': 'E3KD6EC4HC21M',
  #   'frenchtown-2': 'E26J61I9R80RJ9',
  #   'manitouspring': 'E1MKWWV36DW4OG',
  #   'mattoon-il': 'E9E30ORK7ZL6N',
  #   'midlandpublicschools': 'E2BIDT9V3O7JFT',
  #   'redlakemn': 'E2U6MGZ3QIGNOL',
  #   'santaritaca-ca': 'E5MGFURF3WUTE',
  #   'south-lane': 'E141S253TM9ZHA',
  #   'uat01': 'E1AT4A84EXWB0E',
  #   'uat02': 'E2CDHIMIGDA29R',
  # }

  # NonProd Site List
  cloudfrontIdsList = {
    'smokeleg': 'E2V9HDF0IYB90I',
    'e2esdi': 'E1NHCKJCXLPI28',
    'edulogsales': 'EWN4HJ6J58U4E',
    'emmetidaho': 'E3M6QIECQAKT6P',
    'frenchtown-5': 'E1WVBTTOG4VT8W',
    'frenchtown-demo': 'EA9V1YERLPBER',
    'frenchtown-sales-1': 'E3VR95O1T7GIEL',
    'frenchtown-sales': 'E2N2WG1SWC15DM',
    'frenchtown-transfers': 'E1E5IJYK4GJ2LX',
    'manitou-co-internal': 'E11S5BB9OIYQUZ',
    'midland': 'E1JGBO4BCZIL7C',
    'missoula5': 'E65O85GUFUR7Y',
    'missoula6': 'E2CET9L69726FJ',
    'missoula7': 'E2IO2H0DYCVERE',
    'missoula8': 'E35SSVAEHY9OK2',
    'missoulacloud1': 'E2RJSA9FDP0JIQ',
    'missoulacloud2': 'E3FKHJO69N14E0',
    'missoulacloud3': 'EDDCEP0Y9XT1B',
    'missoulacloud4': 'E2LZ60CKI36GB4',
    'opt-release-2': 'E2H3FOY5ZDQ12V',
    'opt-release': 'EQJIRP4LU9YFR',
    'release-3': 'E36RZW41VY8GQA',
    'release-2': 'E2SIZQ7QT5S3MA',
    'south-lane': 'E2Q0TH07IQSBOY',
    'telematics-demo': 'E36LS069M290V3',
    'telematics': 'E1UXVW3AM4PDTL',
    'telematics-sales': 'E134DIET99EOZ6',
    'test-deployment-1': 'ENZFR2LEL3VET',
    'test-deployment-2': 'EKJIVUOC0F78X',
    'test-deployment-3': 'E15SPJQDG65PZ5',
    'test-deployment-4': 'E2H4Z6UYP6T3YT',
    'vb-e1': 'E2GUTOC7IV24SS',
    'vb-e3': 'E1YUP6ISXH3V7C',
    'vb': 'EYN2HJSHM7C9W',
    'vb-sales': 'E38H74FX5ROE4Y',
    'vb-static': 'E27JQJUEKDFQ2B',
    'vb-staticdynamic': 'E3CQ596M86QDF',
  }
  awsProfile = 'default'
  if envType == 'prod':
    awsProfile = 'prod'

  try:

    SSM = connect(service='ssm', region=region, profile=awsProfile)
    for siteName, cfId in cloudfrontIdsList.items():
      name = f'/edulog/athena/{envType}/{siteName}/fe_cf_id'
      value = cfId
      resp = SSM.put_parameter(Name=name, Value=value, Type='String', Overwrite=True)
      print(siteName, cfId, resp)
  
  except Exception as err:
    print('addCloudFrontId.error', err)
    raise err


if __name__ == '__main__':
  Fire(add) 