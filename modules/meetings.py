import sqlite3
import os

# print(os.path.abspath(os.path.join(os.path.dirname(__file__), "database", "meetings.db")))

# DB_PATH = os.path.join(os.path.dirname(__file__), "database", "meetings.db")
# DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "meetings.db")
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),  # go up from /modules to /PTTS
    "database",
    "ptts.db"
)



# ---------------------------------------------------------
# STUDENT FUNCTIONS
# ---------------------------------------------------------

def get_available_tutors():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tutor_id, name, subject
        FROM tutor
        ORDER BY name ASC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def book_meeting(student_id, tutor_id, date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO meetings (student_id, tutor_id, date, completed, notes)
        VALUES (?, ?, ?, 0, '')
    """, (student_id, tutor_id, date))

    conn.commit()
    conn.close()


def get_student_meetings(student_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT m.meeting_id, t.name, m.date, m.notes
        FROM meetings m
        JOIN tutor t ON m.tutor_id = t.tutor_id
        WHERE m.student_id = ?
        ORDER BY m.date ASC
    """, (student_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def cancel_meeting(meeting_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM meetings WHERE meeting_id = ?", (meeting_id,))
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# TUTOR FUNCTIONS
# ---------------------------------------------------------

def get_tutor_meetings(tutor_id, completed=False):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT m.meeting_id, s.name, m.date, m.notes
        FROM meetings m
        JOIN student s ON m.student_id = s.student_id
        WHERE m.tutor_id = ? AND m.completed = ?
        ORDER BY m.date ASC
    """, (tutor_id, 1 if completed else 0))

    rows = cursor.fetchall()
    conn.close()
    return rows


def mark_meeting_completed(meeting_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("UPDATE meetings SET completed = 1 WHERE meeting_id = ?", (meeting_id,))
    conn.commit()
    conn.close()


def update_meeting_notes(meeting_id, notes):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("UPDATE meetings SET notes = ? WHERE meeting_id = ?", (notes, meeting_id))
    conn.commit()
    conn.close()
