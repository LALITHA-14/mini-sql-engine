# cli.py
from parser import parse_sql
from engine import execute_query, load_table
from utils import format_table
import os

def _basename_no_ext(path: str) -> str:
    base = os.path.basename(path)
    if base.lower().endswith(".csv"):
        return base[:-4]
    return base

def repl(default_csv: str = None) -> None:
    print("Mini SQL Engine — REPL")
    print("Commands:")
    print("  LOAD <csv-path>     -> load a CSV into default table")
    print("  Type SQL queries (SELECT...) and press Enter.")
    print("  exit or quit to leave.")
    if default_csv:
        print(f"Default CSV: {default_csv}")

    loaded_csv = default_csv
    loaded_rows = None
    loaded_headers = None

    if loaded_csv:
        try:
            loaded_rows, loaded_headers = load_table(loaded_csv)
            print(f"Loaded {loaded_csv} ({len(loaded_rows)} rows).")
        except FileNotFoundError:
            print(f"Could not load default CSV: {loaded_csv}")
            loaded_csv = None

    while True:
        try:
            line = input("\nsql> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            return
        if not line:
            continue
        if line.lower() in ("exit", "quit"):
            print("Goodbye.")
            return
        if line.lower().startswith("load "):
            path = line.split(" ", 1)[1].strip()
            try:
                loaded_rows, loaded_headers = load_table(path)
                loaded_csv = path
                print(f"Loaded: {path} ({len(loaded_rows)} rows).")
            except FileNotFoundError as e:
                print(f"Error: {e}")
            continue

        # If user omitted FROM, inject loaded table if available
        q = line
        if " from " not in q.lower() and loaded_csv:
            table_name = _basename_no_ext(loaded_csv)
            q = q.rstrip(";") + f" FROM {table_name}"

            # We must ensure the CSV filename matches table name used by engine.
            # So if table_name != actual filename without .csv, create symlink? Simpler: copy rows to a temp file named table_name.csv
            # But to keep simple, if loaded_csv path's basename without ext equals table_name, ensure load_table can find it.
            # We'll set parsed['from'] after parsing if parser returned a from that differs. We'll handle in execution below.

        # parse
        try:
            parsed = parse_sql(q)
        except ValueError as e:
            print(f"Parse error: {e}")
            continue

        # If parsed['from'] refers to a bare table name equal to loaded file's basename, and loaded_csv is set,
        # temporarily write loaded_rows to a file with that name (if needed) OR bypass by calling engine.execute_query with modified parsed.
        # Simpler approach: if parsed['from'] equals basename no-ext of loaded_csv, then call execute_query after copying loaded rows to in-memory temporary file is complicated.
        # But engine.execute_query always loads from disk; easiest: if user used LOAD, we will create a temp file named <table>.csv in cwd linking to the loaded CSV path.
        # Implement small helper: if parsed['from'] != loaded_csv and loaded_csv and parsed['from'] == basename_no_ext(loaded_csv): set parsed['from'] to loaded_csv path.
        if loaded_csv:
            parsed_from = parsed.get("from")
            if parsed_from == _basename_no_ext(loaded_csv):
                parsed["from"] = loaded_csv

        # execute
        try:
            headers, rows = execute_query(parsed)
            # rows is list[dict]
            print(format_table(headers, rows))
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except KeyError as e:
            print(f"Error: {e}")
        except TypeError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    repl()
