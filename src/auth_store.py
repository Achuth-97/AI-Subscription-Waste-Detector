import hashlib
import hmac
import secrets
import sqlite3
from io import StringIO
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = ROOT / "runtime_data" / "subscriptions.sqlite3"
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1
SCRYPT_DKLEN = 64
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 1024
_DUMMY_SALT = b"subscription-app-login-check"


class RegistrationError(ValueError):
    pass


class UsernameAlreadyExists(RegistrationError):
    pass


def _connect(database_path=DATABASE_PATH):
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def _validated_user_id(user_id):
    if isinstance(user_id, bool) or not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("An authenticated user ID is required.")
    return user_id


def _normalize_username(username):
    if not isinstance(username, str):
        raise RegistrationError("Username must be text.")
    normalized = username.strip()
    if not 3 <= len(normalized) <= 64:
        raise RegistrationError("Username must be between 3 and 64 characters.")
    return normalized, normalized.casefold()


def _validate_password(password):
    if not isinstance(password, str):
        raise RegistrationError("Password must be text.")
    if not MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
        raise RegistrationError(
            f"Password must be between {MIN_PASSWORD_LENGTH} and "
            f"{MAX_PASSWORD_LENGTH} characters."
        )


def _hash_password(password, salt):
    return hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=SCRYPT_DKLEN,
    )


def initialize_database(database_path=DATABASE_PATH):
    Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    with _connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                username_key TEXT NOT NULL UNIQUE,
                password_salt BLOB NOT NULL,
                password_hash BLOB NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS user_subscriptions (
                user_id INTEGER PRIMARY KEY,
                data_json TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
            """
        )


def register_user(username, password, database_path=DATABASE_PATH):
    display_username, username_key = _normalize_username(username)
    _validate_password(password)
    salt = secrets.token_bytes(16)
    password_hash = _hash_password(password, salt)
    try:
        with _connect(database_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO users
                    (username, username_key, password_salt, password_hash)
                VALUES (?, ?, ?, ?)
                """,
                (display_username, username_key, salt, password_hash),
            )
            return int(cursor.lastrowid)
    except sqlite3.IntegrityError as error:
        if "username_key" in str(error).lower():
            raise UsernameAlreadyExists("An account with that username already exists.") from error
        raise


def authenticate_user(username, password, database_path=DATABASE_PATH):
    if not isinstance(username, str) or not isinstance(password, str):
        return None
    username_key = username.strip().casefold()
    if not username_key or len(password) > MAX_PASSWORD_LENGTH:
        return None

    with _connect(database_path) as connection:
        user = connection.execute(
            """
            SELECT user_id, username, password_salt, password_hash
            FROM users
            WHERE username_key = ?
            """,
            (username_key,),
        ).fetchone()

    salt = user[2] if user else _DUMMY_SALT
    expected_hash = user[3] if user else _hash_password(
        "not-a-valid-password", _DUMMY_SALT
    )
    supplied_hash = _hash_password(password, salt)
    if user is None or not hmac.compare_digest(supplied_hash, expected_hash):
        return None
    return int(user[0]), user[1]


def load_subscriptions(user_id, database_path=DATABASE_PATH):
    authenticated_user_id = _validated_user_id(user_id)
    with _connect(database_path) as connection:
        row = connection.execute(
            "SELECT data_json FROM user_subscriptions WHERE user_id = ?",
            (authenticated_user_id,),
        ).fetchone()
    if row is None:
        return None
    return pd.read_json(StringIO(row[0]), orient="split")


def save_subscriptions(user_id, subscriptions, database_path=DATABASE_PATH):
    authenticated_user_id = _validated_user_id(user_id)
    if not isinstance(subscriptions, pd.DataFrame):
        raise TypeError("Subscriptions must be provided as a pandas DataFrame.")
    data_json = subscriptions.to_json(
        orient="split",
        force_ascii=False,
        date_format="iso",
    )
    with _connect(database_path) as connection:
        owner = connection.execute(
            "SELECT 1 FROM users WHERE user_id = ?",
            (authenticated_user_id,),
        ).fetchone()
        if owner is None:
            raise ValueError("Authenticated user account does not exist.")
        connection.execute(
            """
            INSERT INTO user_subscriptions (user_id, data_json)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                data_json = excluded.data_json,
                updated_at = CURRENT_TIMESTAMP
            """,
            (authenticated_user_id, data_json),
        )
