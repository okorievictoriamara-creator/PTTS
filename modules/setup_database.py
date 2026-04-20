import sqlite3
import os
import hashlib

# Database path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "database",
    "ptts.db"
)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # USERS TABLE (master table)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # STUDENT TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            class TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)

    # TUTOR TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tutor (
            tutor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            subject TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)

    # PARENT TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parent (
            parent_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            child_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)

    # STAFF TABLE (Admins)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            position TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)

    # MEETINGS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            meeting_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            tutor_id INTEGER,
            date TEXT,
            notes TEXT,
            completed INTEGER DEFAULT 0,
            FOREIGN KEY(student_id) REFERENCES student(student_id),
            FOREIGN KEY(tutor_id) REFERENCES tutor(tutor_id)
        )
    """)

    # ---------------------------------------------------------
    # INSERT SAMPLE USERS (4 students, 4 tutors, 4 parents, 4 admins)
    # ---------------------------------------------------------

    sample_users = [
        # username, role
        ("student1", "student"),
        ("student2", "student"),
        ("student3", "student"),
        ("student4", "student"),

        ("tutor1", "tutor"),
        ("tutor2", "tutor"),
        ("tutor3", "tutor"),
        ("tutor4", "tutor"),

        ("parent1", "parent"),
        ("parent2", "parent"),
        ("parent3", "parent"),
        ("parent4", "parent"),

        ("admin1", "admin"),
        ("admin2", "admin"),
        ("admin3", "admin"),
        ("admin4", "admin")
    ]

    # Insert users with hashed password "pass123"
    hashed = hash_password("pass123")

    for username, role in sample_users:
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (username, hashed, role))

    # ---------------------------------------------------------
    # INSERT STUDENT RECORDS
    # ---------------------------------------------------------
    student_records = [
        ("student1", "Alice Green", "Year 10"),
        ("student2", "Ben White", "Year 11"),
        ("student3", "Chloe Black", "Year 9"),
        ("student4", "Daniel Grey", "Year 12")
    ]

    for username, name, class_name in student_records:
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT OR IGNORE INTO student (user_id, name, class)
            VALUES (?, ?, ?)
        """, (user_id, name, class_name))

    # ---------------------------------------------------------
    # INSERT TUTOR RECORDS
    # ---------------------------------------------------------
    tutor_records = [
        ("tutor1", "Mr. Johnson", "Mathematics"),
        ("tutor2", "Ms. Smith", "English"),
        ("tutor3", "Dr. Brown", "Physics"),
        ("tutor4", "Mrs. Adams", "Biology")
    ]

    for username, name, subject in tutor_records:
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT OR IGNORE INTO tutor (user_id, name, subject)
            VALUES (?, ?, ?)
        """, (user_id, name, subject))

    # ---------------------------------------------------------
    # INSERT PARENT RECORDS
    # ---------------------------------------------------------
    parent_records = [
        ("parent1", "Mrs. Green", 1),
        ("parent2", "Mr. White", 2),
        ("parent3", "Mrs. Black", 3),
        ("parent4", "Mr. Grey", 4)
    ]

    for username, name, child_id in parent_records:
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT OR IGNORE INTO parent (user_id, name, child_id)
            VALUES (?, ?, ?)
        """, (user_id, name, child_id))

    # ---------------------------------------------------------
    # INSERT ADMIN (STAFF) RECORDS
    # ---------------------------------------------------------
    admin_records = [
        ("admin1", "Mr. Stone", "Head of Admin"),
        ("admin2", "Ms. Rose", "Assistant Admin"),
        ("admin3", "Mr. King", "Records Manager"),
        ("admin4", "Mrs. Queen", "Scheduling Manager")
    ]

    for username, name, position in admin_records:
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT OR IGNORE INTO staff (user_id, name, position)
            VALUES (?, ?, ?)
        """, (user_id, name, position))

    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
