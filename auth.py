import sqlite3


# -------------------------------------------------
# LOGIN FUNCTION
# -------------------------------------------------
def login_user(username, password, role):

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT * FROM users
        WHERE username=?
        AND password=?
        AND role=?
        """,

        (username, password, role)
    )

    user = cursor.fetchone()

    conn.close()

    return user