import sqlite3
from datetime import datetime
import csv

# ---------------------------
# 1. CONNECT TO DATABASE
# ---------------------------
def connect_db(db_name="finance.db"):
    conn = sqlite3.connect(db_name)
    return conn


# ---------------------------
# 2. CREATE TABLES
# ---------------------------
def create_tables(conn):
    cursor = conn.cursor()

    # Income Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            source TEXT NOT NULL
        )
    ''')

    # Expense Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT
        )
    ''') 
    # user table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)


    conn.commit()
    

# ---------------------------
# 3. VALIDATION FUNCTIONS
# ---------------------------
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')  # format: 2024-05-12
        return True
    except ValueError:
        return False


def is_positive_number(value):
    return value > 0


# ---------------------------
# 4. ADD INCOME
# ---------------------------
def add_income(conn, amount, date, source):
    if not is_positive_number(amount):
        print("❌ ERROR: Amount must be positive.")
        return False

    if not is_valid_date(date):
        print("❌ ERROR: Invalid date format. Use YYYY-MM-DD.")
        return False

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO income (amount, date, source) VALUES (?, ?, ?)",
        (amount, date, source)
    )
    conn.commit()
    return True


# ---------------------------
# 5. ADD EXPENSE
# ---------------------------
def add_expense(conn, amount, date, category, description):
    if not is_positive_number(amount):
        print("❌ ERROR: Amount must be positive.")
        return False

    if not is_valid_date(date):
        print("❌ ERROR: Invalid date format. Use YYYY-MM-DD.")
        return False

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (amount, date, category, description) VALUES (?, ?, ?, ?)",
        (amount, date, category, description)
    )
    conn.commit()
    return True


# ---------------------------
# 6. GET INCOME RECORDS
# ---------------------------
def get_all_income(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM income")
    return cursor.fetchall()


# ---------------------------
# 7. GET EXPENSE RECORDS
# ---------------------------
def get_all_expenses(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    return cursor.fetchall()
# ---------------------------
# 8. USER AUTHENTICATION SYSTEM
# ---------------------------
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(conn, username, password):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (username, hash_password(password)))
        conn.commit()
        return True
    except:
        return False

def login_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users 
        WHERE username = ? AND password = ?
    """, (username, hash_password(password)))
    return cursor.fetchone()

#  9--- montly and yearly report 
def get_monthly_income_report(conn, year):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT strftime('%m', date) AS month, SUM(amount) AS total_income
        FROM income
        WHERE strftime('%Y', date) = ?
        GROUP BY month
        ORDER BY month
    ''', (str(year),))
    return cursor.fetchall()

def get_monthly_expense_report(conn, year):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT strftime('%m', date) AS month, SUM(amount) AS total_expense
        FROM expenses
        WHERE strftime('%Y', date) = ?
        GROUP BY month
        ORDER BY month
    ''', (str(year),))
    return cursor.fetchall()


def get_yearly_income_report(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT strftime('%Y', date) AS year, SUM(amount) AS total_income
        FROM income
        GROUP BY year
        ORDER BY year
    ''')
    return cursor.fetchall()

def get_yearly_expense_report(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT strftime('%Y', date) AS year, SUM(amount) AS total_expense
        FROM expenses
        GROUP BY year
        ORDER BY year
    ''')
    return cursor.fetchall()


  # 10 Create the csv file

def export_income_to_csv(conn, file_path):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM income")
    records = cursor.fetchall()
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Amount", "Date", "Source"])
        for row in records:
            writer.writerow(row)
    print(f"✅ Income data exported to {file_path} successfully!")


def export_expenses_to_csv(conn, file_path):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    records = cursor.fetchall()
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Amount", "Date", "Category", "Description"])
        for row in records:
            writer.writerow(row)
    print(f"✅ Expense data exported to {file_path} successfully!")
