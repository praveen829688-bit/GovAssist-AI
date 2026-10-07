import sqlite3
import hashlib
import secrets
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "govassist.db"


def get_connection():
    connection = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def init_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'citizen',
            language TEXT DEFAULT 'English',
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_type TEXT NOT NULL,
            item_name TEXT NOT NULL,
            source TEXT,
            created_at TEXT NOT NULL,
            UNIQUE(user_id, item_type, item_name)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            service_name TEXT NOT NULL,
            application_number TEXT,
            status TEXT DEFAULT 'Draft',
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            query TEXT NOT NULL,
            result_type TEXT,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def register_user(name, email, password, language="English"):

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO users
            (name, email, password_hash, language, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name.strip(),
                email.strip().lower(),
                hash_password(password),
                language,
                datetime.now().isoformat()
            )
        )

        connection.commit()

        return True, "Registration successful."

    except sqlite3.IntegrityError:

        return False, "An account with this email already exists."

    finally:
        connection.close()


def login_user(email, password):

    connection = get_connection()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        AND password_hash = ?
        """,
        (
            email.strip().lower(),
            hash_password(password)
        )
    ).fetchone()

    connection.close()

    if user:
        return dict(user)

    return None


def get_user(user_id):

    connection = get_connection()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    return dict(user) if user else None


def save_item(user_id, item_type, item_name, source=""):

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT OR IGNORE INTO saved_items
            (user_id, item_type, item_name, source, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                item_type,
                item_name,
                source,
                datetime.now().isoformat()
            )
        )

        connection.commit()

    finally:
        connection.close()


def remove_item(user_id, item_type, item_name):

    connection = get_connection()

    connection.execute(
        """
        DELETE FROM saved_items
        WHERE user_id = ?
        AND item_type = ?
        AND item_name = ?
        """,
        (
            user_id,
            item_type,
            item_name
        )
    )

    connection.commit()
    connection.close()


def get_saved_items(user_id, item_type=None):

    connection = get_connection()

    if item_type:

        rows = connection.execute(
            """
            SELECT *
            FROM saved_items
            WHERE user_id = ?
            AND item_type = ?
            ORDER BY created_at DESC
            """,
            (
                user_id,
                item_type
            )
        ).fetchall()

    else:

        rows = connection.execute(
            """
            SELECT *
            FROM saved_items
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,)
        ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def create_application(
    user_id,
    service_name,
    application_number="",
    notes=""
):

    connection = get_connection()

    now = datetime.now().isoformat()

    cursor = connection.execute(
        """
        INSERT INTO applications
        (
            user_id,
            service_name,
            application_number,
            status,
            notes,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            service_name,
            application_number,
            "Draft",
            notes,
            now,
            now
        )
    )

    connection.commit()

    application_id = cursor.lastrowid

    connection.close()

    return application_id


def get_applications(user_id):

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM applications
        WHERE user_id = ?
        ORDER BY updated_at DESC
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def update_application_status(
    application_id,
    status,
    notes=""
):

    connection = get_connection()

    connection.execute(
        """
        UPDATE applications
        SET status = ?,
            notes = ?,
            updated_at = ?
        WHERE id = ?
        """,
        (
            status,
            notes,
            datetime.now().isoformat(),
            application_id
        )
    )

    connection.commit()
    connection.close()


def add_history(
    user_id,
    query,
    result_type="search"
):

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO history
        (user_id, query, result_type, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            query,
            result_type,
            datetime.now().isoformat()
        )
    )

    connection.commit()
    connection.close()


def get_history(user_id, limit=50):

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM history
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (
            user_id,
            limit
        )
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def add_notification(
    user_id,
    title,
    message
):

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO notifications
        (user_id, title, message, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            title,
            message,
            datetime.now().isoformat()
        )
    )

    connection.commit()
    connection.close()


def get_notifications(user_id):

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM notifications
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def mark_notifications_read(user_id):

    connection = get_connection()

    connection.execute(
        """
        UPDATE notifications
        SET is_read = 1
        WHERE user_id = ?
        """,
        (user_id,)
    )

    connection.commit()
    connection.close()


def get_admin_statistics():

    connection = get_connection()

    users = connection.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    applications = connection.execute(
        "SELECT COUNT(*) FROM applications"
    ).fetchone()[0]

    searches = connection.execute(
        "SELECT COUNT(*) FROM history"
    ).fetchone()[0]

    saved = connection.execute(
        "SELECT COUNT(*) FROM saved_items"
    ).fetchone()[0]

    connection.close()

    return {
        "users": users,
        "applications": applications,
        "searches": searches,
        "saved": saved
    }


init_database()
