# Demo - Deployment Tool v2

## Sites

- uat-midland: clone from Prod Site: midlandpublicschools

  - TenantId: 8ef0c1ad-650a-40f4-be71-d402c0154008
  - FE: 1.29.20
  - BE: 1.29.35
  - RDSSnapshot: arn:aws:rds:us-east-2:690893158275:snapshot:athena-midlandpublicschools-rds-snapshotforuat
  - DB: 2.090,1.11 (athena, geocode)
  - User: uat-midland@edulog.com / Athen@uat-midland1

- uat-southlane: clone from Prod Site: south-lane
  - TenantId: 8ef0c1ad-650a-40f4-be71-d402c0154008
  - FE: 1.30.7
  - BE: 1.30.11
  - RDSSnapshot: arn:aws:rds:us-east-2:690893158275:snapshot:athena-south-lane-rds-snapshotforuat
  - DB: 2.091,1.11 (athena, geocode)
  - User: uat-southlane@edulog.com / Athen@uat-southlane1

## Scenarios

- Deploy: Upgrade uat-midland from 1.29.x to 1.33.x (runtime: ~ 12 minutes)
- Rollback: Rollback uat-southlane from 1.33.x to 1.30.x (runtime: ~ 12 minutes)

### uat-midland

> Upgrade from 1.29.x to 1.33.x

Expectations:

- Versions are captured and saved to SSM-PS on keys:
  - /edulog/athena/prod/deployment/uat-midland/last/fe_version
  - /edulog/athena/prod/deployment/uat-midland/last/be_version
  - /edulog/athena/prod/deployment/uat-midland/last/db_version
- Snapshot is created and saved to SSM-PS on key: /edulog/athena/prod/deployment/uat-midland/last/db_snapshot
- Backend upgraded to 1.33.5
- Frontend upgraded to 1.33.5
- Database upgraded to 2.095,1.15 (athena, geocode)

Steps:

- Run deploy job with params:
  - siteName: uat-midland
  - feVersion: 1.33.5
  - beVersion: 1.33.5

Notes:

- From 1.29 to 1.33, GeoCodeService DB Migration run a heavily CPU load on DB & BE Instances which can cause BE Instances scaled out to 2 Instances.

### uat-southlane

> Rollback (from 1.33.x back to 1.30.x)

Expectations:

- Get Last Versions saved from the last deployment:
  - /edulog/athena/prod/deployment/uat-midland/last/fe_version
  - /edulog/athena/prod/deployment/uat-midland/last/be_version
  - /edulog/athena/prod/deployment/uat-midland/last/db_version
- Snapshot current DB before rollback
- Restore Snapshot from last Deployment which got from /edulog/athena/prod/deployment/uat-midland/last/db_snapshot
- Rollback Backend to 1.30.11
- Rollback Frontend to 1.30.7
- Database Version got to 2.091,1.11 (athena, geocode)

Steps:

- Run rollback job with params:
  - siteName: uat-soutlane

### uat-southlane

> Upgrade from 1.30.x to 1.33.x

Expectations:

- Versions are captured and saved to SSM-PS on keys:
  - /edulog/athena/prod/deployment/uat-southlane/last/fe_version
  - /edulog/athena/prod/deployment/uat-southlane/last/be_version
  - /edulog/athena/prod/deployment/uat-southlane/last/db_version
- Snapshot is created and saved to SSM-PS on key: /edulog/athena/prod/deployment/uat-southlane/last/db_snapshot
- Backend upgraded to 1.33.5
- Frontend upgraded to 1.33.5
- Database upgraded to 2.096, 1.17 (athena, geocode)

Steps:

- Run deploy job with params:
  - siteName: uat-southlane
  - feVersion: 1.33.5
  - beVersion: 1.33.5

Notes:

### uat-midland

> Rollback (from 1.33.x to 1.29.x)

Expectations:

- Versions are captured and saved to SSM-PS on keys:
  - /edulog/athena/prod/deployment/uat-southlane/last/fe_version
  - /edulog/athena/prod/deployment/uat-southlane/last/be_version
  - /edulog/athena/prod/deployment/uat-southlane/last/db_version
- Snapshot is created and saved to SSM-PS on key: /edulog/athena/prod/deployment/uat-southlane/last/db_snapshot
- Backend upgraded to 1.34.5
- Frontend upgraded to 1.34.2
- Database upgraded to 2.096, 1.17 (athena, geocode)

Steps:

- Run deploy job with params:
  - siteName: uat-southlane
  - feVersion: 1.34.2
  - beVersion: 1.34.5

Notes:

- If you run rollback here, the expectations of versions must be: 1.33.x

> Upgrade from 1.33.x to 1.34.x

Expectations:

- Versions are captured and saved to SSM-PS on keys:
  - /edulog/athena/prod/deployment/uat-southlane/last/fe_version
  - /edulog/athena/prod/deployment/uat-southlane/last/be_version
  - /edulog/athena/prod/deployment/uat-southlane/last/db_version
- Snapshot is created and saved to SSM-PS on key: /edulog/athena/prod/deployment/uat-southlane/last/db_snapshot
- Backend upgraded to 1.34.5
- Frontend upgraded to 1.34.2
- Database upgraded to 2.096, 1.17 (athena, geocode)

Steps:

- Run deploy job with params:
  - siteName: uat-southlane
  - feVersion: 1.34.2
  - beVersion: 1.34.5

Notes:

- If you run rollback here, the expectations of versions must be: 1.33.x

### Check DB Schema Version

```
SELECT
	(SELECT version FROM public.flyway_schema_history ORDER BY installed_rank DESC LIMIT 1) AS athena_version,
	(SELECT sql_version FROM public.geo_tenant_info) AS geocode_version
```
