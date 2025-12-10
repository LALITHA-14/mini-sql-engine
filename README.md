# 🧠 Mini SQL Engine

A lightweight **in-memory SQL interpreter** built in Python.  
Supports basic SQL features like:

✔️ `SELECT`  
✔️ `WHERE` filters  
✔️ Comparison operators  
✔️ `COUNT()` aggregation  
✔️ Loading CSV files using `LOAD <table>`  

This project demonstrates how SQL queries are parsed and executed internally.

---

## 🚀 Project Overview
Mini SQL Engine is a simple SQL interpreter that loads CSV files into memory and executes basic SQL queries.  
It is designed for understanding:

- How SQL parsing works  
- How filtering and projections are applied  
- How aggregation functions are evaluated  

---

## 🛠️ Setup Instructions

### 1️⃣ Requirements
- Python **3.10+**

### 2️⃣ Clone the repository
```bash
git clone https://github.com/LALITHA-14/mini-sql-engine
   ```
3. Navigate to the project folder:
    cd mini-sql-engine
4. Run the CLI:
    python cli.py
5. At the sql> prompt, type your queries (no semicolon needed), for example:
    LOAD employees
    SELECT * FROM employees
    LOAD customers
    SELECT * FROM customers

### 📘 SQL Grammar Supported
➤ 1. LOAD Command
LOAD <table_name>


Loads <table_name>.csv from the project folder

Only filenames (without extension) are allowed

Example:

LOAD employees

➤ 2. SELECT Statement
SELECT <columns> FROM <table_name> [WHERE <condition>]

Columns:

*

Single column: name

Multiple columns (commas allowed with or without spaces):

SELECT name, age
SELECT name,age

Case-insensitivity:

select, SELECT, SeLeCt → all valid

WHERE condition is also case-insensitive

➤ 3. WHERE Conditions

Supported operators:

Operator	Meaning
=	Equal
!=	Not equal
>	Greater than
<	Less than
>=	Greater or equal
<=	Less or equal

Examples:

age >= 30
department = 'HR'
salary != 50000

➤ 4. Aggregation

Supported:

COUNT(*)
COUNT(column)


Example:

SELECT COUNT(*) FROM employees
SELECT COUNT(salary) FROM employees WHERE department = 'Engineering'

### 📂 Project Structure
``` mini-sql-engine/
│
│── cli.py                      # Interactive SQL command-line interface
│── engine.py                   # Core SQL execution engine
│── parser.py                   # SQL query parser
│── utils.py                    # Helper functions
│── README.md                   # Project documentation
│── query_outputs_employees.csv # Stored example outputs
│── query_outputs_customers.csv # Stored example outputs
│
├── sample_data/                # Sample CSV datasets
│     ├── customers.csv
│     └── employees.csv
│
├── tests/                      # Unit tests for parser & engine
│     ├── test_engine.py
│     ├── test_parser.py
│     ├── cli.py
│     ├── engine.py
│     ├── parser.py
│     ├── utils.py
│     └── __init__.py
│
└── __pycache__/                # Auto-generated compiled Python files
      ├── engine.cpython-314.pyc
      ├── parser.cpython-314.pyc
      └── utils.cpython-314.pyc
```
### 📊 Sample Query Outputs
🔹 employees.csv

**Query:** `LOAD customers`
**Output:**
```
Loaded: 5 rows.
```

**Query:** `SELECT * FROM employees`
**Output:**
| id | name    | age | department  | salary | email                 |
| -- | ------- | --- | ----------- | ------ | -----------------     |  
| 1  | Alice   | 30  | Engineering | 90000  | `alice@example.com`   |
| 2  | Bob     | 24  | Sales       | 45000  | `bob@example.com`     |
| 3  | Charlie | 29  | Engineering | 87000  | `charlie@example.com` |
| 4  | Diana   | 35  | HR          | 60000  | `diana@example.com`   |
| 5  | Elon    | 40  | Management  | 150000 | `elon@example.com`    |


**Query:** `SELECT name, salary FROM employees`
**Output:**
| name    | salary |
| ------- | ------ |
| Alice   | 90000  |
| Bob     | 45000  |
| Charlie | 87000  |
| Diana   | 60000  |
| Elon    | 150000 |


**Query:** `SELECT name FROM employees WHERE department = 'HR'`
**Output:**
| name  |
| ----- |
| Diana |


**Query:** `SELECT name, age FROM employees WHERE salary > 60000`
**Output:**
| name    | age |
| ------- | --- |
| Alice   | 30  |
| Charlie | 29  |
| Elon    | 40  |


**Query:** `SELECT name FROM employees WHERE age >= 30`
**Output:**
| name  |
| ----- |
| Alice |
| Diana |
| Elon  |


**Query:** `SELECT name FROM employees WHERE age <= 30`
**Output:**
| name    |
| ------- |
| Alice   |
| Bob     |
| Charlie |


**Query:** `SELECT name FROM employees WHERE department != 'Engineering'`
**Output:**
| name  |
| ----- |
| Bob   |
| Diana |
| Elon  |


**Query:** `SELECT COUNT(*) FROM employees`
**Output:**
| count |
| ----- |
| 5     |


**Query:** `SELECT COUNT(salary) FROM employees`
**Output:**
| count |
| ----- |
| 5     |


**Query:** `SELECT COUNT(salary) FROM employees WHERE department = 'Engineering'`
**Output:**
| count |
| ----- |
| 2     |


**Query:** `SELECT salary FROM employees WHERE salary >= 90000`
**Output:**
| salary |
| ------ |
| 90000  |
| 150000 |


**Query:** `SELECT xyz FROM employees`
**Output:**
```
Error: 'Column not found in table: xyz'
```


**Query:** `SELECT name FROM unknown_table`
**Output:**
Error: [Errno 2] No such file or directory: 'unknown_table.csv'


🔹 customers.csv
**Query:** `LOAD customers`
**Output:**
```
Loaded: 5 rows.
```

**Query:** `SELECT * FROM customers`
**Output:**
| id | name  | age | country | purchases | email               |
| -- | ----- | --- | ------- | --------- | ------------------  |
| 1  | John  | 28  | USA     | 5         | `john@example.com`  |
| 2  | Mary  | 35  | UK      | 12        | `mary@example.com`  |
| 3  | Steve | 40  | USA     | 8         | `steve@example.com` |
| 4  | Linda | 22  | Canada  | 3         | `linda@example.com` |
| 5  | Emma  | 30  | USA     | 7         | `emma@example.com`  |


**Query:** `SELECT name, country FROM customers WHERE purchases > 5`
**Output:**
| name  | country |
| ----- | ------- |
| Mary  | UK      |
| Steve | USA     |
| Emma  | USA     |


**Query:** `SELECT COUNT(*) FROM customers`
**Output:**
| count |
| ----- |
| 5     |


**Query:** `SELECT COUNT(purchases) FROM customers WHERE country = 'USA'`
**Output:**
| count |
| ----- |
| 3     |
