import csv
from mm_lakehouse.generate import generate
from mm_lakehouse.drift import detect
from mm_lakehouse.contracts import CONTRACTS
from mm_lakehouse.graph import export

def test_generate_and_drift(tmp_path):
    directory=tmp_path/'data'; result=generate(str(directory),12)
    assert set(result)==set(CONTRACTS)
    assert all(item['severity']=='OK' for item in detect(str(directory)))
    f=directory/'policy.csv';rows=list(csv.reader(f.open()))
    rows[0].remove('annual_premium')
    with f.open('w',newline='') as out:csv.writer(out).writerows(rows)
    assert next(i for i in detect(str(directory)) if i['dataset']=='policy')['severity']=='BLOCK'

def test_graph_export(tmp_path):
    summary=export(str(tmp_path),'graph.json')
    assert summary['nodes']>10
    assert (tmp_path/'graph.json').exists()
