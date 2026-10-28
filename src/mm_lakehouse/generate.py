import csv
from datetime import date, timedelta
from pathlib import Path
from random import Random
from .contracts import CONTRACTS

def generate(output: str="data/generated", customers: int=50, seed: int=21):
    """Generate mutually consistent, fictional insurance + wealth CSV records."""
    rng=Random(seed); root=Path(output); root.mkdir(parents=True, exist_ok=True)
    people=[];products=[];policies=[];coverages=[];advisors=[];accounts=[];holdings=[];transactions=[]
    for i in range(1,customers+1):
        people.append([f"C{i:05d}",f"Demo{i}","Customer",rng.choice(["MA","NC","NY","OH"]),"1985-06-15"])
    for j,(name,lob) in enumerate([("Whole Life","LIFE"),("Term Life","LIFE"),("Disability Income","DI"),("Fixed Annuity","ANNUITY")],1):
        products.append([f"P{j:03d}",name,lob])
    for j in range(1,6): advisors.append([f"A{j:03d}",f"Advisor {j}",rng.choice(["EAST","WEST"])])
    for i in range(1,customers+1):
        pid=f"POL{i:05d}"; acct=f"W{i:05d}"; cid=f"C{i:05d}"
        policies.append([pid,cid,f"P{rng.randint(1,4):03d}",rng.choice(["ACTIVE","ACTIVE","LAPSED"]),"2024-01-01",str(rng.randint(60,900)*12),"2026-10-01T10:00:00"])
        coverages.append([f"CV{i:05d}",pid,"BASE",str(rng.randint(100,750)*1000)])
        accounts.append([acct,cid,f"A{(i%5)+1:03d}",rng.choice(["BROKERAGE","IRA"]),"2024-02-01","OPEN"])
        for h,sym in enumerate(["ETF_A","BOND_B"],1):
            holdings.append([f"H{i:05d}{h}",acct,sym,str(rng.randint(1,100)),str(rng.randint(50,180)),"2026-10-01"])
        transactions.append([f"T{i:05d}",acct,"2026-10-01","CONTRIBUTION",str(rng.randint(100,2500))])
    datasets={"customer":people,"insurance_product":products,"policy":policies,"coverage":coverages,"advisor":advisors,"wealth_account":accounts,"holding":holdings,"transaction":transactions}
    for name,rows in datasets.items():
        with (root/f"{name}.csv").open("w",newline="",encoding="utf-8") as stream:
            writer=csv.writer(stream);writer.writerow(CONTRACTS[name]);writer.writerows(rows)
    return {name:len(rows) for name,rows in datasets.items()}
