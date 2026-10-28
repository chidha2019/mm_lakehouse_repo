# Deployment runbook

1. Provision two Azure Blob containers: `insurance-landing` and `insurance-iceberg`. Prefer separate accounts or policies for real use.
2. Provision Snowflake warehouse and role. Grant database/schema permissions, integration usage, external volume usage and warehouse usage per least privilege.
3. Copy `.env.example` to `.env` and set credentials. Never commit `.env`.
4. Install with `python -m pip install -r requirements.txt` then set `PYTHONPATH=src` (or install package).
5. `PYTHONPATH=src python -m mm_lakehouse.cli generate --customers 100`.
6. `PYTHONPATH=src python -m mm_lakehouse.cli drift` (should be all `OK`).
7. Configure Azure Snowflake storage integration and external volume using commented DDL in `sql/00_setup.sql`. Admin must approve Entra service principal and assign Reader to landing and Contributor to Iceberg container. Confirm external volume verification before proceeding.
8. Uncomment stage creation in setup SQL; remove angle-bracket placeholders. Run `bootstrap` only after configuring the volume, editing/uncommenting the stage SQL, and approving the Azure integration. `bootstrap` executes setup then table DDL.
9. `PYTHONPATH=src python -m mm_lakehouse.cli upload`.
10. `PYTHONPATH=src python -m mm_lakehouse.cli run`.
11. Validate `SELECT * FROM MM_REFERENCE.CURATED.MONTHLY_PREMIUM_BY_PRODUCT;` and `SELECT * FROM MM_REFERENCE.CURATED.FACT_WEALTH_POSITION;`.
12. `PYTHONPATH=src python -m mm_lakehouse.cli graph` then ingest `artifacts/knowledge_graph.json` into Neo4j/ContextHub.

## Operational considerations

- This is a reference application, not a deploy-without-review regulated-financial production system.
- CSV transfers are full-file content-addressed; COPY load-history handles duplicate files. Bronze append ingestion and Silver upserts tolerate reruns, but deletions are not propagated to Silver/Curated. Add tombstone/CDC semantics for production.
- Source schemas are contract-checked before upload; breaking drift blocks transfer. Added columns only warn but may still require updated ingestion mapping.
- Azure connection strings are demonstration-only; prefer managed identity, private endpoints, Key Vault and federated auth in production.
- Protect PII, enforce retention and audit access; these records are fictional.
- Current Gold is snapshot/current state, not historical SCD2; month's premium summary is an as-of-current-month snapshot, not earned premiums or payment receipts.
- The sample SQL requires cloud acceptance testing; `pytest` verifies Python and static assets, not actual Snowflake execution.
