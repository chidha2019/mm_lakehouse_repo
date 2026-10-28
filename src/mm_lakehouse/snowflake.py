from pathlib import Path
import snowflake.connector
from .config import Config

def connect(cfg=None):
    cfg=cfg or Config()
    if not (cfg.sf_account and cfg.sf_user and cfg.sf_password):
        raise ValueError("SNOWFLAKE_ACCOUNT, USER, PASSWORD required")
    return snowflake.connector.connect(account=cfg.sf_account,user=cfg.sf_user,password=cfg.sf_password,role=cfg.sf_role,warehouse=cfg.sf_warehouse,session_parameters={"QUERY_TAG":"mm_reference_lakehouse"})

def execute_script(connection, path):
    """Execute semicolon-separated SQL via Snowflake's native statement parser."""
    from snowflake.connector.util_text import split_statements
    with Path(path).open(encoding="utf-8") as stream:
        statements=list(split_statements(stream))
    with connection.cursor() as cur:
        for sql, _ in statements:
            if sql.strip():
                cur.execute(sql)
                if Path(path).name == "05_quality.sql" and sql.lstrip().upper().startswith("SELECT"):
                    row=cur.fetchone()
                    if row and row[0] != "PASS":
                        raise RuntimeError(f"Data quality assertion failed: {row[0]}")

def run_files(paths,cfg=None):
    conn=connect(cfg)
    try:
        for path in paths:execute_script(conn,path)
    finally:conn.close()
