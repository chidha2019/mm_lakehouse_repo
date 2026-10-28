import json,re
from pathlib import Path
from .contracts import CONTRACTS

def export(root=".",output="artifacts/knowledge_graph.json"):
    """Produce deterministic source-code and data-lineage graph seed for ContextHub ingestion."""
    root=Path(root); nodes={}; edges=[]
    def node(i,kind,**props): nodes[i]={"id":i,"kind":kind,**props}
    def edge(a,b,relation):
        item={"source":a,"target":b,"relation":relation}
        if item not in edges:edges.append(item)
    for ds,cols in CONTRACTS.items():
        source=f"csv:{ds}";bronze=f"table:BRONZE.{ds.upper()}";silver=f"table:SILVER.{ds.upper()}"
        node(source,"SourceFile",path=f"landing/{ds}/");node(bronze,"IcebergTable",layer="bronze");node(silver,"IcebergTable",layer="silver")
        edge(source,bronze,"FEEDS");edge(bronze,silver,"TRANSFORMS_INTO")
        for col in cols:
            node(f"column:SILVER.{ds.upper()}.{col.upper()}","Column",name=col)
            edge(silver,f"column:SILVER.{ds.upper()}.{col.upper()}","HAS_COLUMN")
    for sql in sorted((root/'sql').rglob('*.sql')):
        fid=f"code:{sql.relative_to(root)}";node(fid,"SQLAsset",path=str(sql.relative_to(root)))
        content=sql.read_text(encoding="utf-8")
        for schema,table in re.findall(r"\b(?:FROM|JOIN)\s+(BRONZE|SILVER|CURATED)\.([A-Z_]+)",content,re.I):
            tid=f"table:{schema.upper()}.{table.upper()}";node(tid,"IcebergTable",layer=schema.lower());edge(fid,tid,"READS_FROM")
        for schema,table in re.findall(r"\b(?:MERGE\s+INTO|INSERT\s+INTO|CREATE\s+(?:OR\s+REPLACE\s+)?ICEBERG\s+TABLE)\s+(BRONZE|SILVER|CURATED)\.([A-Z_]+)",content,re.I):
            tid=f"table:{schema.upper()}.{table.upper()}";node(tid,"IcebergTable",layer=schema.lower());edge(fid,tid,"WRITES_TO")
    target=root/output;target.parent.mkdir(parents=True,exist_ok=True)
    result={"schema_version":"1.0","nodes":list(nodes.values()),"edges":edges};target.write_text(json.dumps(result,indent=2),encoding="utf-8")
    return {"nodes":len(nodes),"edges":len(edges),"path":str(target)}
