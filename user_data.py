import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("data", "govassist.db")

os.makedirs("data", exist_ok=True)


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_user_scope():
    conn = _connect()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # Add user_id to applications if it does not exist
    # --------------------------------------------------------

    cursor.execute("""
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

    # Check existing columns.
    cursor.execute("PRAGMA table_info(applications)")
    columns = [row["name"] for row in cursor.fetchall()]

    if "user_id" not in columns:
        cursor.execute("""
            ALTER TABLE applications
            ADD COLUMN user_id INTEGER
        """)

    # --------------------------------------------------------
    # Add user_id to notifications
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT,
            reminder_date TEXT
        )
    """)

    cursor.execute("PRAGMA table_info(notifications)")
    notification_columns = [
        row["name"] for row in cursor.fetchall()
    ]

    if "user_id" not in notification_columns:
        cursor.execute("""
            ALTER TABLE notifications
            ADD COLUMN user_id INTEGER
        """)

    conn.commit()
    conn.close()


def create_user_application(
    user_id,
    service_name,
    reference_number="",
    notes="",
    application_date=""
):
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applications
        (
            user_id,
            service_name,
            reference_number,
            notes,
            application_date,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        service_name,
        reference_number,
        notes,
        application_date,
        "Submitted",
        datetime.now().isoformat()
    ))

    conn.commit()

    application_id = cursor.lastrowid

    conn.close()

    return application_id


def get_user_applications(user_id):
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM applications
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def update_user_application_status(
    user_id,
    application_id,
    status
):
    allowed_statuses = [
        "Draft",
        "Submitted",
        "Under Review",
        "Documents Required",
        "Approved",
        "Rejected",
        "Completed"
    ]

    if status not in allowed_statuses:
        return False

    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE applications
        SET status = ?
        WHERE id = ?
        AND user_id = ?
    """, (
        status,
        application_id,
        user_id
    ))

    changed = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return changed


def create_user_notification(
    user_id,
    title,
    message,
    reminder_date=None
):
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notifications
        (
            user_id,
            title,
            message,
            created_at,
            reminder_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        title,
        message,
        datetime.now().isoformat(),
        reminder_date
    ))

    conn.commit()
    conn.close()


def get_user_notifications(user_id):
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM notifications
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_user_statistics(user_id):
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE user_id = ?
    """, (user_id,))

    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE user_id = ?
        AND status = 'Approved'
    """, (user_id,))

    approved = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE user_id = ?
        AND status = 'Rejected'
    """, (user_id,))

    rejected = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM applications
        WHERE user_id = ?
        AND status IN ('Submitted', 'Under Review')
    """, (user_id,))

    active = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM notifications
        WHERE user_id = ?
    """, (user_id,))

    notifications = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "approved": approved,
        "rejected": rejected,
        "active": active,
        "notifications": notifications
    }


init_user_scope()
