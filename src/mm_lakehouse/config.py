import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

@dataclass(frozen=True)
class Config:
    azure_connection: str = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    container: str = os.getenv("AZURE_CONTAINER", "insurance-landing")
    sf_account: str = os.getenv("SNOWFLAKE_ACCOUNT", "")
    sf_user: str = os.getenv("SNOWFLAKE_USER", "")
    sf_password: str = os.getenv("SNOWFLAKE_PASSWORD", "")
    sf_role: str = os.getenv("SNOWFLAKE_ROLE", "SYSADMIN")
    sf_warehouse: str = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    sf_database: str = os.getenv("SNOWFLAKE_DATABASE", "MM_REFERENCE")
    stage: str = os.getenv("SNOWFLAKE_STAGE", "MM_REFERENCE.RAW_CSV.AZURE_LANDING")
