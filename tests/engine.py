# engine.py
import csv
from typing import List, Dict, Any, Tuple
from utils import try_cast

def load_table(table_name: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Load CSV (table_name may end with or without .csv). Returns rows list[dict] and headers list."""
    fname = table_name if table_name.lower().endswith(".csv") else table_name + ".csv"
    with open(fname, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = []
        for r in reader:
            cast_row = {k: try_cast(v) for k, v in r.items()}
            rows.append(cast_row)
    return rows, headers

def _compare(left: Any, op: str, right: Any) -> bool:
    # handle None
    if left is None:
        if op == "=":
            return right is None
        if op == "!=":
            return right is not None
        return False
    # numeric compare if both numeric
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        if op == "=":
            return left == right
        if op == "!=":
            return left != right
        if op == ">":
            return left > right
        if op == "<":
            return left < right
        if op == ">=":
            return left >= right
        if op == "<=":
            return left <= right
    # string compare (coerce both to str)
    l = str(left)
    r = str(right)
    if op == "=":
        return l == r
    if op == "!=":
        return l != r
    if op == ">":
        return l > r
    if op == "<":
        return l < r
    if op == ">=":
        return l >= r
    if op == "<=":
        return l <= r
    raise TypeError(f"Unsupported comparison: {left} {op} {right}")

def eval_condition(row: Dict[str, Any], cond: Dict[str, Any]) -> bool:
    col = cond["col"]
    if col not in row:
        raise KeyError(f"Column not found in table: {col}")
    left = row[col]
    return _compare(left, cond["op"], cond["val"])

def execute_query(parsed: Dict[str, Any]) -> Tuple[List[str], List[Dict[str, Any]]]:
    """
    Execute parsed query (from parse_sql). Returns headers and rows (list of dicts).
    Aggregation COUNT returns headers ['count'] and rows [{'count': n}].
    """
    rows, headers = load_table(parsed["from"])

    # WHERE
    if parsed.get("where"):
        cond = parsed["where"]
        filtered = []
        for r in rows:
            try:
                if eval_condition(r, cond):
                    filtered.append(r)
            except KeyError:
                raise
            except TypeError:
                raise
        rows = filtered

    # Aggregation
    if parsed.get("agg"):
        func, arg = parsed["agg"]
        if func.upper() != "COUNT":
            raise ValueError(f"Unsupported aggregate: {func}")
        if arg == "*":
            cnt = len(rows)
        else:
            if arg not in headers:
                raise KeyError(f"Column not found in table: {arg}")
            cnt = sum(1 for r in rows if r.get(arg) is not None and r.get(arg) != "")
        return ["count"], [{"count": cnt}]

    # Projection
    select = parsed["select"]
    if select == "*":
        return headers, rows
    else:
        # validate columns
        for c in select:
            if c not in headers:
                raise KeyError(f"Column not found in table: {c}")
        projected = [{c: r.get(c) for c in select} for r in rows]
        return select, projected
