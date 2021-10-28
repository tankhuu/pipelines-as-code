# Improve Release Tool

## Scenarios

- Sites: midland, southlane (clone to uat-midland, uat-southlane)
- Upgrade to v1.34 (GeoCode Service Migration can run heavy updates in DB which can cause connection to DB hang or other service startup failed)

## Test uat-midland & uat-southlane

```
name: uat-midland
TenantId: 8ef0c1ad-650a-40f4-be71-d402c0154008
FE: 1.29.20
BE: 1.29.35
DB: 2.090,1.11
```

User: uat-midland@edulog.com
pass: Athen@uat-midland1

> Test 1 > Upgrade to 1.33.5 from 1.29.x

> Test 2 > Rollback (will be on 1.29.x)

```
name: uat-southlane
TenantID: 94fb3e33-f207-4809-a19c-1623c567c4e9
FE: 1.30.7
BE: 1.30.11
DB: 2.091,1.11
```

User: uat-southlane@edulog.com
pass: Athen@uat-southlane1

## Must do

- Add cf_id into SSM parameter store for all of current sites (done) `scripts/python/addCloudFrontId.py` -> done
- Add db_pass into SSM parameter store (SecureString) for all of current sites `scripts/python/addDBPass.py` -> done
- Update list of current sites (nonprod & prod)

## Needs

### Deployment

- Collection info before upgrade
  - DB version
  - BE version
  - FE version
- Take Snapshot before upgrade, upload to S3 with proper prefix
- Backend Deployment
  - Resume ASG Processes
  - Deploy
  - Check Service Status
  - Check DB Migration
- Suspend ASG Processes
- Deploy Frontend

### Rollback

- Get previous Versions: FE, BE, DB
- Restore DB Snapshot
- Resume ASG Processes
- Deploy Backend
- Post Deployment
- Suspend ASG Processes
- Deploy Frontend

### Check Deployment Job

- Wait for new instance launched & old instance terminated.
- Check DB Schema Versions: (athena, geocode, ivin, edta)
- Check Backend Services startup status
- Check status of Backend Services after deployment, with /actuator info

### Notification

## Status: Success | Failure

EnvType: nonprod | prod
Site: {siteName}.{domain}

---

_Before Deployment_
FE Version:
BE Version:
DB Version:

---

_After Deployment_
FE Version:
BE Version:
DB Version:

---

Snapshot:

### Data Store

Dir: ~/athena/deployment/{envType}/{siteName}/{jobNumber}

Files:

- snapshot output
- frontend output
- backend output
- check deployment output

### Jenkins Jobs

- Take Snapshot
- Restore Snapshot
- Deploy Frontend
- Deploy Backend
- Check Deployment
- Send Notification
- Capture Deployment Information
- Clone Site
  - Source: envType, tenantId, siteName
  - Destination: envType, tenantId, siteName
  - Show Users in AthenaDB

## Midland

SiteName: test-midland (midlandpublicschools)

- TenantId: 893a3e72-9b91-4a56-bf5c-474ae84c25bb
- FEVersion: 1.29.20
- BEVersion: 1.29.35

SiteName: test-southlane (south-lane)

- TenantId: 174010ff-937a-4cac-bf88-84706ae25490
- FEVersion: 1.30.7
- BEVersion: 1.30.11

# Snapshot

## Midland

s3://edulog-athena-backup/athena/database/prod/midlandpublicschools/Athena-midlandpublicschools.20210628-072358.bak

## Southlane

s3://edulog-athena-backup/athena/database/prod/south-lane/Athena-south-lane.20210628-072515.bak

# Cleanup Site Steps

- Empty S3 Bucket:
  - AthenaUI
  - WebQuery
- Delete CFN Stack
