import sqlite3
import os
import hashlib

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "database",
    "ptts.db"
)

def authenticate(username, password, role):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Hash the password before comparing
    hashed = hashlib.sha256(password.encode()).hexdigest()
    # print("AUTH DB PATH:", DB_PATH)
    # print("Typed password:", password)
    # print("Hashed password:", hashed)


    cursor.execute("""
        SELECT user_id
        FROM users
        WHERE username = ? AND password = ? AND role = ?
    """, (username, hashed, role))

    user = cursor.fetchone()

    if not user:
        conn.close()
        return None

    user_id = user[0]

    # Role-specific lookup
    if role == "student":
        cursor.execute("""
            SELECT student_id, name, class
            FROM student
            WHERE user_id = ?
        """, (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return {
                "user_id": user_id,
                "student_id": result[0],
                "name": result[1],
                "class": result[2],
                "role": "student"
            }

    elif role == "tutor":
        cursor.execute("""
            SELECT tutor_id, name, subject
            FROM tutor
            WHERE user_id = ?
        """, (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return {
                "user_id": user_id,
                "tutor_id": result[0],
                "name": result[1],
                "subject": result[2],
                "role": "tutor"
            }

    elif role == "parent":
        cursor.execute("""
            SELECT parent_id, name
            FROM parent
            WHERE user_id = ?
        """, (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return {
                "user_id": user_id,
                "parent_id": result[0],
                "name": result[1],
                "role": "parent"
            }

    elif role == "admin":
        conn.close()
        return {
            "user_id": user_id,
            "username": username,
            "role": "admin"
            }

    conn.close()
    return None
