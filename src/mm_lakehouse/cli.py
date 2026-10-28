import argparse,json
from pathlib import Path
from .generate import generate
from .drift import detect
from .graph import export

def main():
    p=argparse.ArgumentParser(description="Synthetic insurance/wealth lakehouse")
    p.add_argument("command",choices=["generate","drift","upload","bootstrap","bronze","silver","curated","run","graph"])
    p.add_argument("--data-dir",default="data/generated")
    p.add_argument("--customers",type=int,default=50)
    args=p.parse_args(); root=Path(__file__).resolve().parents[2]
    if args.command=="generate":result=generate(args.data_dir,args.customers)
    elif args.command=="drift":result=detect(args.data_dir)
    elif args.command=="upload":
        from .azure import upload
        dr=detect(args.data_dir)
        if any(i['severity']=="BLOCK" for i in dr):raise SystemExit("Blocking schema drift; upload aborted")
        result=upload(args.data_dir)
    elif args.command=="graph":result=export(root)
    else:
        steps={"bootstrap":["00_setup.sql","01_tables.sql"],"bronze":["02_bronze_load.sql"],"silver":["03_silver.sql"],"curated":["04_curated.sql"],"run":["02_bronze_load.sql","03_silver.sql","04_curated.sql","05_quality.sql"]}
        from .snowflake import run_files
        run_files([root/"sql"/f for f in steps[args.command]]);result={"completed":args.command}
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
