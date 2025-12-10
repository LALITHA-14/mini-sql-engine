# tests/test_parser.py
from parser import parse_sql

def test_select_star():
    q = "SELECT * FROM employees"
    p = parse_sql(q)
    assert p["select"] == "*"
    assert p["from"] == "employees"

def test_select_columns_and_where():
    q = "SELECT name, age FROM customers WHERE country = 'USA'"
    p = parse_sql(q)
    assert isinstance(p["select"], list)
    assert p["where"]["col"] == "country"
    assert p["where"]["op"] == "="
    assert p["where"]["val"] == "USA"

def test_count():
    q = "SELECT COUNT(*) FROM employees"
    p = parse_sql(q)
    assert p["agg"][0].upper() == "COUNT"
    assert p["agg"][1] == "*"
