import sqlite3


# -------------------------------------------------
# CREATE DATABASE
# -------------------------------------------------
def create_database():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    # -------------------------------------------------
    # USERS TABLE
    # -------------------------------------------------
    cursor.execute("""

        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,

            password TEXT,

            role TEXT
        )

    """)

    conn.commit()

    conn.close()


# -------------------------------------------------
# ADD DEFAULT USERS
# -------------------------------------------------
def add_default_users():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    users = [

        ("hod", "hod123", "HOD"),

        ("class_teacher", "class123", "Class Teacher"),

        ("subject_teacher", "subject123", "Subject Teacher")
    ]

    for user in users:

        try:

            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                user
            )

        except:
            pass

    conn.commit()

    conn.close()