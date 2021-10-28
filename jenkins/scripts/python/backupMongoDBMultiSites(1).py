#!/usr/bin/env python3
from fire import Fire
import boto3
from botocore.config import Config
from datetime import datetime
import subprocess

def connect(service: str = 'ec2', profile: str = 'default', region: str = 'us-east-2'):
  try:
    config = Config(region_name=region)
    session = boto3.Session(profile_name=profile)

    return session.client(service, config=config)
  except Exception as err:
    print('connect.error', err)
    raise err

def getIp(EC2, inst_id: str):
  """Get Private IP Address of Instance in an ASG

  Args:
      asgName (str): AWS AutoScaling Group Name
  """
  
  inst = EC2.describe_instances(InstanceIds=[inst_id])
  if inst:
    instance = inst['Reservations'][0]['Instances'][0]
    if instance:
      private_ip = instance['PrivateIpAddress']
      return private_ip

def collectASGInfo(sitesList, totalSites, ASG, EC2, token):
  if token:
    resp = ASG.describe_auto_scaling_groups(NextToken=token)
  else:
    resp = ASG.describe_auto_scaling_groups()
  if resp:
    asgs = resp.get('AutoScalingGroups')
    if asgs and len(asgs) > 0:
      for a in asgs:
        name = a.get('AutoScalingGroupName')
        nameParts = name.split('-')
        if len(nameParts) > 4:
          if nameParts[0] == 'athena' and nameParts[-4] == 'CQASGStack':
            # Get site name by removing un-used part in nameParts
            nameParts.pop(0)
            for i in range(4):
              nameParts.pop()
            site = '-'.join(nameParts)
            instances = a['Instances']
            if len(instances) > 0:
              for inst in instances:
                inst_id = inst['InstanceId']
                if inst_id:
                  sitesList[site] = {
                    'ip': getIp(EC2, inst_id)
                  }
                        
            totalSites += 1
    nextToken = resp.get('NextToken')
    if nextToken:
      return collectASGInfo(sitesList, totalSites, ASG, EC2, nextToken)
  return sitesList, totalSites, nextToken


def backup(envType: str = 'nonprod', s3Bucket: str = 'edulog-athena-backup'):
  SUPPORTED_ENVTYPES = ['nonprod', 'prod']
  if envType not in SUPPORTED_ENVTYPES:
    raise Exception('backupMongoDB.error: unsupported')

  sitesList = {} # List of information of Sites that need to run backup
  totalSites = 0 # Total of sites which will be run
  backupDate = datetime.now().strftime('%Y%m%d-%H%M%S')

  ASG = connect('autoscaling')
  EC2 = connect('ec2')
  if envType == 'prod':
    ASG = connect('autoscaling', 'prod')
    EC2 = connect('ec2', 'prod')

  try:
    sitesList, totalSites, token = collectASGInfo(sitesList, totalSites, ASG, EC2, '')

    if totalSites > 0:
      for site, att in sitesList.items():
        ip = att.get('ip')
        if ip:
          command = 'sh scripts/bash/mongodb_backup.sh {} {} {} {} {}'.format(envType, site, ip, s3Bucket, backupDate)
          process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
          output, error = process.communicate()
          if error:
            sitesList[site]['error'] = error
          # else:
          #   sitesList[site]['success'] = output

    print('result', sitesList)
    print('total', totalSites)
  except Exception as err:
    print('backupMongoDB.error', err)
    raise err

# Test
if __name__ == '__main__':
  Fire(backup)