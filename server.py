import sqlite3
import bcrypt


def create_user_table():
    conn = sqlite3.connect("example.db")
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
                )
            """
    )

    conn.commit()
    conn.close()


def register_user(username, password):
    conn = sqlite3.connect("example.db")
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO users(username, password) VALUES(?, ?)""",
        (username, hash_password(password)),
    )

    conn.commit()
    conn.close()


def hash_password(password):
    # Convert password to array of bytes and hash it
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
