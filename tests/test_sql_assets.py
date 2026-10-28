from pathlib import Path

def test_expected_sql_assets():
    root=Path(__file__).parents[1]
    for name in ['00_setup.sql','01_tables.sql','02_bronze_load.sql','03_silver.sql','04_curated.sql','05_quality.sql']:
        assert (root/'sql'/name).stat().st_size>100
    sql=(root/'sql'/'04_curated.sql').read_text()
    assert 'FACT_POLICY_PREMIUM' in sql and 'FACT_WEALTH_POSITION' in sql
