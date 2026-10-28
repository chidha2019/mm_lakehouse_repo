import hashlib
from pathlib import Path
from azure.storage.blob import BlobServiceClient
from .config import Config
from .contracts import CONTRACTS

def upload(source="data/generated", prefix="landing", config=None):
    cfg=config or Config()
    if not cfg.azure_connection: raise ValueError("AZURE_STORAGE_CONNECTION_STRING required")
    client=BlobServiceClient.from_connection_string(cfg.azure_connection)
    container=client.get_container_client(cfg.container)
    try: container.create_container()
    except Exception as exc:
        from azure.core.exceptions import ResourceExistsError
        if not isinstance(exc,ResourceExistsError): raise
    report=[]
    for name in CONTRACTS:
        path=Path(source)/f"{name}.csv"
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        blob=f"{prefix}/{name}/{digest[:12]}/{name}.csv"
        with path.open("rb") as stream:
            container.upload_blob(name=blob,data=stream,overwrite=True,metadata={"sha256":digest})
        report.append({"dataset":name,"blob":blob,"sha256":digest})
    return report
