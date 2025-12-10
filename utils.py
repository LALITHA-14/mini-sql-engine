# utils.py
from typing import Any, List, Dict, Optional

def try_cast(value: Optional[str]) -> Any:
    """Try to cast CSV string to int/float; treat empty string as None."""
    if value is None:
        return None
    v = value.strip()
    if v == "":
        return None
    # int
    try:
        return int(v)
    except ValueError:
        pass
    # float
    try:
        return float(v)
    except ValueError:
        pass
    # strip surrounding quotes
    if (v.startswith("'") and v.endswith("'")) or (v.startswith('"') and v.endswith('"')):
        return v[1:-1]
    return v

def format_table(headers: List[str], rows: List[Dict[str, Any]]) -> str:
    """Pretty-print rows (list of dicts) with aligned columns."""
    if not headers:
        return "(no columns)"
    # compute widths
    widths = {h: len(str(h)) for h in headers}
    for r in rows:
        for h in headers:
            s = '' if r.get(h) is None else str(r.get(h))
            widths[h] = max(widths[h], len(s))
    # build lines
    sep = " | "
    header_line = sep.join(h.ljust(widths[h]) for h in headers)
    sep_line = "-+-".join("-" * widths[h] for h in headers)
    data_lines = []
    for r in rows:
        line = sep.join((str(r.get(h)) if r.get(h) is not None else "").ljust(widths[h]) for h in headers)
        data_lines.append(line)
    if not rows:
        data_lines = ["(0 rows)"]
    return "\n".join([header_line, sep_line, *data_lines])
