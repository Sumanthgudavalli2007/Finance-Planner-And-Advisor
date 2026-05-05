import sqlite3

def get_connection():
    return sqlite3.connect("finance.db")

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    # DEFAULT ADMIN
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES ('admin', 'admin123', 'admin')
        """)

    # DEFAULT CLIENT
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='client'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES ('user', 'user123', 'client')
        """)

    # FINANCE DATA TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finance_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            income REAL,
            expenses REAL,
            savings REAL,
            entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ADMIN REPORT TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            file_data BLOB,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def authenticate(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def save_admin_report(file_name, file_bytes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO admin_reports (file_name, file_data) VALUES (?, ?)",
        (file_name, file_bytes)
    )
    conn.commit()
    conn.close()


def get_latest_admin_report():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_name, file_data FROM admin_reports ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()
    conn.close()
    return data


def save_finance(income, expenses, savings):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO finance_data (income, expenses, savings) VALUES (?, ?, ?)",
        (income, expenses, savings)
    )
    conn.commit()
    conn.close()