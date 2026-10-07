import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(
    "data",
    "govassist.db"
)

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Ensure tables exist.

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    role TEXT DEFAULT 'citizen',
    created_at TEXT NOT NULL,
    last_login TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    service_name TEXT NOT NULL,
    reference_number TEXT,
    notes TEXT,
    application_date TEXT,
    status TEXT DEFAULT 'Submitted',
    created_at TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TEXT,
    reminder_date TEXT
)
""")

conn.commit()
conn.close()

print("Database tables verified.")
print("No demo passwords or fake citizen accounts were created.")
