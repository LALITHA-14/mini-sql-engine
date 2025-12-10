# parser.py
import re
from typing import Dict, Any, Optional

SQL_RE = re.compile(
    r"^\s*SELECT\s+(?P<select>.+?)\s+FROM\s+(?P<from>\S+)(?:\s+WHERE\s+(?P<where>.+))?\s*$",
    re.IGNORECASE,
)
WHERE_RE = re.compile(r"^(?P<col>\w+)\s*(?P<op>=|!=|>=|<=|>|<)\s*(?P<val>.+)$")

def _parse_value_literal(token: str) -> Any:
    t = token.strip()
    # quoted string
    if (t.startswith("'") and t.endswith("'")) or (t.startswith('"') and t.endswith('"')):
        return t[1:-1]
    # try int
    try:
        return int(t)
    except ValueError:
        pass
    # try float
    try:
        return float(t)
    except ValueError:
        pass
    # fallback plain string
    return t

def parse_sql(query: str) -> Dict[str, Any]:
    """
    Parse a limited SQL query and return dict:
    { 'select': '*' or [col,...] or None,
      'agg': ('COUNT', arg) or None,
      'from': table_name,
      'where': {'col','op','val'} or None }
    Raises ValueError on parse errors.
    """
    m = SQL_RE.match(query)
    if not m:
        raise ValueError("Invalid SQL. Expected: SELECT <cols> FROM <table> [WHERE <cond>].")
    select_part = m.group("select").strip()
    from_part = m.group("from").strip()
    where_part = m.group("where")

    select = None
    agg = None
    sp_upper = select_part.upper()
    # COUNT aggregate?
    if sp_upper.startswith("COUNT(") and select_part.endswith(")"):
        inner = select_part[select_part.find("(")+1:-1].strip()
        agg = ("COUNT", inner)
    elif select_part == "*":
        select = "*"
    else:
        cols = [c.strip() for c in select_part.split(",") if c.strip()]
        if not cols:
            raise ValueError("No columns specified in SELECT.")
        select = cols

    where = None
    if where_part:
        wm = WHERE_RE.match(where_part.strip())
        if not wm:
            raise ValueError("Invalid WHERE clause. Expected: column operator value")
        col = wm.group("col")
        op = wm.group("op")
        val_token = wm.group("val").strip()
        val = _parse_value_literal(val_token)
        where = {"col": col, "op": op, "val": val}

    return {"select": select, "agg": agg, "from": from_part, "where": where}
