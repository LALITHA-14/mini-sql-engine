# tests/test_engine.py
from engine import load_table, execute_query

def test_load_and_count():
    parsed = {"select": None, "agg": ("COUNT", "*"), "from": "sample_data/employees.csv", "where": None}
    headers, rows = execute_query(parsed)
    # rows is [{'count': 5}]
    assert headers == ["count"]
    assert rows[0]["count"] == 5

def test_select_specific_columns():
    parsed = {"select": ["name", "age"], "agg": None, "from": "sample_data/employees.csv", "where": None}
    headers, rows = execute_query(parsed)
    assert headers == ["name", "age"]
    assert len(rows) == 5
    assert "name" in rows[0] and "age" in rows[0]
