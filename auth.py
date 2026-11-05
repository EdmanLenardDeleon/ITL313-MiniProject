import hashlib
import hmac
import os
import sqlite3
from database import get_connection

def hash_password(password, salt=None):
    """Return (salt_hex, hash_hex). A new random salt is made if none is given."""
    if salt is None:
        salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return salt.hex(), digest.hex()

def register_user(username, password):
    if not username or len(password) < 6:
        return False, "Username required and password must be 6+ characters."
    salt, pw_hash = hash_password(password)
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
            (username, salt, pw_hash),
        )
        conn.commit()
        conn.close()
        return True, "Account created. You can now log in."
    except sqlite3.IntegrityError:
        return False, "Username already exists."

def login_user(username, password):
    conn = get_connection()
    row = conn.execute(
        "SELECT salt, password_hash FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    if row is None:
        return False
    salt_hex, stored_hash = row
    _, new_hash = hash_password(password, bytes.fromhex(salt_hex))
    return hmac.compare_digest(new_hash, stored_hash)