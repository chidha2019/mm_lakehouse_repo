-- Run after configuring Azure RBAC and granting Snowflake Azure service principal access.
-- Replace placeholders, run with ACCOUNTADMIN for integrations/volume, then least privilege.
CREATE DATABASE IF NOT EXISTS MM_REFERENCE;
CREATE SCHEMA IF NOT EXISTS MM_REFERENCE.RAW_CSV;
CREATE SCHEMA IF NOT EXISTS MM_REFERENCE.BRONZE;
CREATE SCHEMA IF NOT EXISTS MM_REFERENCE.SILVER;
CREATE SCHEMA IF NOT EXISTS MM_REFERENCE.CURATED;
USE DATABASE MM_REFERENCE;
-- Azure landing storage integration: read permissions to landing container.
-- CREATE STORAGE INTEGRATION MM_AZURE_CSV_INT TYPE = EXTERNAL_STAGE
-- STORAGE_PROVIDER = 'AZURE' ENABLED = TRUE
-- AZURE_TENANT_ID = '<tenant-id>'
-- STORAGE_ALLOWED_LOCATIONS = ('azure://<account>.blob.core.windows.net/insurance-landing/');
-- DESCRIBE INTEGRATION MM_AZURE_CSV_INT; -- grant consent to AZURE_CONSENT_URL and Storage Blob Data Reader to service principal
-- Iceberg storage (separate Azure path/container from incoming CSV files):
-- CREATE EXTERNAL VOLUME MM_ICEBERG_VOLUME STORAGE_LOCATIONS =
-- ((NAME = 'azure_iceberg', STORAGE_PROVIDER = 'AZURE',
-- STORAGE_BASE_URL = 'azure://<account>.blob.core.windows.net/insurance-iceberg/',
-- AZURE_TENANT_ID = '<tenant-id>'));
-- DESCRIBE EXTERNAL VOLUME MM_ICEBERG_VOLUME; -- consent; Storage Blob Data Contributor
-- SELECT SYSTEM$VERIFY_EXTERNAL_VOLUME('MM_ICEBERG_VOLUME');
CREATE FILE FORMAT IF NOT EXISTS MM_REFERENCE.RAW_CSV.CSV_FORMAT
 TYPE=CSV FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1 EMPTY_FIELD_AS_NULL=TRUE;
-- Once MM_AZURE_CSV_INT is activated, uncomment (do not place credentials in SQL):
-- CREATE STAGE IF NOT EXISTS MM_REFERENCE.RAW_CSV.AZURE_LANDING
-- URL='azure://<account>.blob.core.windows.net/insurance-landing/landing/'
-- STORAGE_INTEGRATION=MM_AZURE_CSV_INT
-- FILE_FORMAT=MM_REFERENCE.RAW_CSV.CSV_FORMAT;
