import sqlite3
import hashlib

def connect():
    conn = sqlite3.connect("ukbuddy.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visa_verification(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        dob TEXT,
        passport TEXT
    )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(email, password):
    conn = sqlite3.connect("ukbuddy.db")
    cursor = conn.cursor()

    hashed = hash_password(password)

    try:
        cursor.execute("INSERT INTO users(email,password) VALUES(?,?)",
                       (email, hashed))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login_user(email, password):
    conn = sqlite3.connect("ukbuddy.db")
    cursor = conn.cursor()

    hashed = hash_password(password)

    cursor.execute("SELECT * FROM users WHERE email=? AND password=?",
                   (email, hashed))

    user = cursor.fetchone()
    conn.close()
    return user


def save_verification(email, dob, passport):
    conn = sqlite3.connect("ukbuddy.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO visa_verification(email,dob,passport) VALUES(?,?,?)",
                   (email,dob,passport))

    conn.commit()
    conn.close()