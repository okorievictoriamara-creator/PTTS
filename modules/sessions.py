import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),  # go up from /modules to /PTTS
    "database",
    "ptts.db"
)


def get_student_sessions(student_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT m.meeting_id, m.tutor_id, t.name, m.date, m.notes, m.completed
        FROM meetings m
        JOIN tutor t ON m.tutor_id = t.tutor_id
        WHERE m.student_id = ?
        ORDER BY m.date DESC
    """, (student_id,))

    rows = cursor.fetchall()
    conn.close()

    sessions = []
    for r in rows:
        sessions.append({
            "id": r[0],
            "tutor_id": r[1],
            "tutor": r[2],
            "date": r[3],
            "notes": r[4] if r[4] else "",
            "status": "Completed" if r[5] == 1 else "Upcoming"
        })

    return sessions


def book_new_session(student_id, tutor_id, date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO meetings (student_id, tutor_id, date, notes, completed)
        VALUES (?, ?, ?, '', 0)
    """, (student_id, tutor_id, date))

    conn.commit()
    conn.close()


def cancel_session(meeting_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM meetings WHERE meeting_id = ?", (meeting_id,))
    conn.commit()
    conn.close()
