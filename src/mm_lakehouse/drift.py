import csv
from pathlib import Path
from .contracts import CONTRACTS

def detect(directory="data/generated"):
    """Deterministic header comparison, not speculative rename inference."""
    result=[]
    for name,expected in CONTRACTS.items():
        path=Path(directory)/f"{name}.csv"
        if not path.exists():
            result.append({"dataset":name,"severity":"ERROR","issue":"missing_file"});continue
        with path.open(newline="",encoding="utf-8-sig") as stream:
            found=next(csv.reader(stream),[])
        added=sorted(set(found)-set(expected));removed=sorted(set(expected)-set(found))
        reordered=not(added or removed) and found!=expected
        result.append({"dataset":name,"added":added,"removed":removed,"reordered":reordered,"severity":"BLOCK" if removed or reordered else "WARN" if added else "OK"})
    return result
