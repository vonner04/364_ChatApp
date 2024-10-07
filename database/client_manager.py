import sqlite3
import bcrypt


# User table schema with id, username, and password columns
def create_user_table():
    conn = sqlite3.connect("chatapp.db")
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


# Registers user if username does not exist
def register_user(username, password):

    if not username or not password:
        return "Username or password cannot be empty"

    conn = sqlite3.connect("chatapp.db")
    cur = conn.cursor()

    try:
        cur.execute(
            """INSERT INTO users(username, password) VALUES(?, ?)""",
            (username, hash_password(password)),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


# Logins user if user exists, else registers user
def login_user(username, password):
    if not username or not password:
        return "Username or password cannot be empty"

    try:
        conn = sqlite3.connect("chatapp.db")
        cur = conn.cursor()

        # Check if user exists
        cur.execute("""SELECT password FROM users WHERE username = ?""", (username,))
        user = cur.fetchone()

        # Check password if user exists
        if user:
            stored_hashed_password = user[0]
            if check_password(password, stored_hashed_password):
                conn.close()
                return "Login successful"
            else:
                conn.close()
                return "Incorrect password"
        else:  # Register user if user does not exist
            conn.close()
            if register_user(username, password):
                return "User not found, New user registered"
            else:
                return "Username already exists"
    finally:
        conn.close()


# Password hashing and verification functions via bcrypt library.
def hash_password(password):
    # Convert password to array of bytes and hash it
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
