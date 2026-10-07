import sqlite3
import os
import hashlib
import secrets
import hmac
from datetime import datetime

DB_PATH = os.path.join("data", "govassist.db")

os.makedirs("data", exist_ok=True)


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_auth_tables():
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    """
    PBKDF2-HMAC-SHA256 password hashing.
    310,000 iterations provides significantly better
    password protection than a single SHA-256 hash.
    """
    salt = secrets.token_bytes(32)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        310000
    )

    return (
        password_hash.hex(),
        salt.hex()
    )


def verify_password(password, stored_hash, stored_salt):
    try:
        salt = bytes.fromhex(stored_salt)

        calculated_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            310000
        ).hex()

        return hmac.compare_digest(
            calculated_hash,
            stored_hash
        )

    except Exception:
        return False


def register_user(name, email, password):
    name = name.strip()
    email = email.strip().lower()

    if not name:
        return False, "Name is required."

    if not email:
        return False, "Email is required."

    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    password_hash, salt = hash_password(password)

    conn = _connect()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users
            (name, email, password_hash, salt, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            email,
            password_hash,
            salt,
            "citizen",
            datetime.now().isoformat()
        ))

        conn.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."

    except Exception as e:
        return False, f"Registration failed: {e}"

    finally:
        conn.close()


def authenticate_user(email, password):
    email = email.strip().lower()

    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    if not user:
        conn.close()
        return None, "Invalid email or password."

    if not verify_password(
        password,
        user["password_hash"],
        user["salt"]
    ):
        conn.close()
        return None, "Invalid email or password."

    cursor.execute("""
        UPDATE users
        SET last_login = ?
        WHERE id = ?
    """, (
        datetime.now().isoformat(),
        user["id"]
    ))

    conn.commit()
    conn.close()

    return dict(user), "Login successful."


def create_session(user_id):
    token = secrets.token_urlsafe(48)

    created = datetime.now()

    # Session expires after 24 hours.
    from datetime import timedelta
    expires = created + timedelta(hours=24)

    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO login_sessions
        (user_id, session_token, created_at, expires_at, active)
        VALUES (?, ?, ?, ?, 1)
    """, (
        user_id,
        token,
        created.isoformat(),
        expires.isoformat()
    ))

    conn.commit()
    conn.close()

    return token


def validate_session(token):
    if not token:
        return None

    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            login_sessions.*,
            users.name,
            users.email,
            users.role
        FROM login_sessions
        JOIN users
            ON login_sessions.user_id = users.id
        WHERE login_sessions.session_token = ?
        AND login_sessions.active = 1
    """, (token,))

    session = cursor.fetchone()

    if not session:
        conn.close()
        return None

    try:
        expires = datetime.fromisoformat(
            session["expires_at"]
        )

        if datetime.now() > expires:
            cursor.execute("""
                UPDATE login_sessions
                SET active = 0
                WHERE session_token = ?
            """, (token,))

            conn.commit()
            conn.close()

            return None

    except Exception:
        conn.close()
        return None

    result = dict(session)

    conn.close()

    return result


def logout_session(token):
    if not token:
        return

    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE login_sessions
        SET active = 0
        WHERE session_token = ?
    """, (token,))

    conn.commit()
    conn.close()


def get_user_by_id(user_id):
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, role, created_at, last_login
        FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    return dict(user) if user else None


def get_user_count():
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")

    count = cursor.fetchone()[0]

    conn.close()

    return count


init_auth_tables()
