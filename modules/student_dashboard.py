import tkinter as tk
import os
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from modules.sessions import get_student_sessions, book_new_session, cancel_session
from modules.ui_components import go_home
import sqlite3

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),  # go up from /modules to /PTTS
    "database",
    "ptts.db"
)

def launch_student_dashboard(student_id, student_name):
    window = tk.Toplevel()
    window.iconbitmap("assets/blank.ico")
    window.title("PTTS - Student Dashboard")
    window.geometry("1250x760")
    window.configure(bg="#F5F7FA")

    # ---------------- HEADER ----------------
    header = tk.Frame(window, bg="#FFFFFF", height=70)
    header.pack(fill="x")

    tk.Label(
        header,
        text=f"Hi {student_name}!",
        font=("Segoe UI", 20, "bold"),
        bg="#FFFFFF",
        fg="#2C3E50"
    ).pack(side="left", padx=25, pady=15)

    tk.Button(
        header,
        text="Book New Session",
        font=("Segoe UI", 10, "bold"),
        bg="#3498DB",
        fg="white",
        relief="flat",
        padx=15,
        pady=5,
        cursor="hand2",
        command=lambda: open_booking_popup()
    ).pack(side="left", padx=10)

    tk.Button(
        header,
        text="View History",
        font=("Segoe UI", 10, "bold"),
        bg="#8E44AD",
        fg="white",
        relief="flat",
        padx=15,
        pady=5,
        cursor="hand2",
        command=lambda: show_history()
    ).pack(side="left", padx=10)

    tk.Button(
        header,
        text="Logout",
        font=("Segoe UI", 10, "bold"),
        bg="#E74C3C",
        fg="white",
        relief="flat",
        padx=15,
        pady=5,
        cursor="hand2",
        command=lambda: go_home(window)
    ).pack(side="right", padx=25)

    # ---------------- MAIN LAYOUT ----------------
    main = tk.Frame(window, bg="#F5F7FA")
    main.pack(fill="both", expand=True, padx=20, pady=10)
    main.columnconfigure(0, weight=1)
    main.columnconfigure(1, weight=1)

    # ---------------- UPCOMING SESSIONS ----------------
    upcoming_frame = tk.Frame(main, bg="#FFFFFF", bd=1, relief="solid")
    upcoming_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(
        upcoming_frame,
        text="Upcoming Sessions",
        font=("Segoe UI", 14, "bold"),
        bg="#FFFFFF",
        fg="#2C3E50"
    ).pack(anchor="w", padx=20, pady=10)

    upcoming_container = tk.Frame(upcoming_frame, bg="#FFFFFF")
    upcoming_container.pack(fill="both", expand=True, padx=20, pady=5)

    # ---------------- COMPLETED SESSIONS ----------------
    completed_frame = tk.Frame(main, bg="#FFFFFF", bd=1, relief="solid")
    completed_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    tk.Label(
        completed_frame,
        text="Completed Sessions",
        font=("Segoe UI", 14, "bold"),
        bg="#FFFFFF",
        fg="#2C3E50"
    ).pack(anchor="w", padx=20, pady=10)

    completed_container = tk.Frame(completed_frame, bg="#FFFFFF")
    completed_container.pack(fill="both", expand=True, padx=20, pady=5)

    # ---------------- FUNCTIONS ----------------
    def refresh_dashboard():
        for widget in upcoming_container.winfo_children():
            widget.destroy()
        for widget in completed_container.winfo_children():
            widget.destroy()

        sessions = get_student_sessions(student_id)
        upcoming = [s for s in sessions if s["status"] == "Upcoming"]
        completed = [s for s in sessions if s["status"] == "Completed"]

        # Upcoming cards
        if not upcoming:
            tk.Label(
                upcoming_container,
                text="No upcoming sessions.",
                font=("Segoe UI", 11),
                bg="#FFFFFF",
                fg="#7F8C8D"
            ).pack(pady=10)
        else:
            for s in upcoming:
                card = tk.Frame(upcoming_container, bg="#ECF6FD", bd=1, relief="solid")
                card.pack(fill="x", pady=6)

                tk.Label(
                    card,
                    text=f"{s['date']}",
                    font=("Segoe UI", 12, "bold"),
                    bg="#ECF6FD",
                    fg="#2C3E50"
                ).grid(row=0, column=0, sticky="w", padx=10, pady=5)

                tk.Label(
                    card,
                    text=f"Tutor: {s['tutor']}",
                    font=("Segoe UI", 11),
                    bg="#ECF6FD",
                    fg="#34495E"
                ).grid(row=1, column=0, sticky="w", padx=10)

                btn_frame = tk.Frame(card, bg="#ECF6FD")
                btn_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=5)

                tk.Button(
                    btn_frame,
                    text="Cancel Session",
                    font=("Segoe UI", 10, "bold"),
                    bg="#E74C3C",
                    fg="white",
                    relief="flat",
                    padx=12,
                    pady=4,
                    command=lambda sid=s['id']: cancel_session_action(sid)
                ).pack(side="top", pady=3)

        # Completed cards
        if not completed:
            tk.Label(
                completed_container,
                text="No completed sessions.",
                font=("Segoe UI", 11),
                bg="#FFFFFF",
                fg="#7F8C8D"
            ).pack(pady=10)
        else:
            for s in completed:
                card = tk.Frame(completed_container, bg="#E9F7EF", bd=1, relief="solid")
                card.pack(fill="x", pady=6)

                tk.Label(
                    card,
                    text=f"{s['date']}",
                    font=("Segoe UI", 12, "bold"),
                    bg="#E9F7EF",
                    fg="#2C3E50"
                ).grid(row=0, column=0, sticky="w", padx=10, pady=5)

                tk.Label(
                    card,
                    text=f"Tutor: {s['tutor']}",
                    font=("Segoe UI", 11),
                    bg="#E9F7EF",
                    fg="#34495E"
                ).grid(row=1, column=0, sticky="w", padx=10)

                btn_frame = tk.Frame(card, bg="#E9F7EF")
                btn_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=5)

                tk.Button(
                    btn_frame,
                    text="View Notes",
                    font=("Segoe UI", 10, "bold"),
                    bg="#27AE60",
                    fg="white",
                    relief="flat",
                    padx=12,
                    pady=4,
                    command=lambda notes=s['notes']: view_notes_popup(notes)
                ).pack(side="top", pady=3)

    def open_booking_popup():
        popup = tk.Toplevel(window)
        popup.iconbitmap("assets/blank.ico")
        popup.title("Book New Session")
        popup.geometry("400x420")
        popup.configure(bg="#FFFFFF")

        tk.Label(
            popup,
            text="Book a New Session",
            font=("Segoe UI", 14, "bold"),
            bg="#FFFFFF",
            fg="#2C3E50"
        ).pack(pady=10)

        # Date
        tk.Label(popup, text="Select Date", font=("Segoe UI", 11),
                 bg="#FFFFFF", fg="#34495E").pack(pady=5)
        cal = Calendar(popup, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(pady=5)

        # Tutor dropdown
        tk.Label(popup, text="Select Tutor", font=("Segoe UI", 11),
                 bg="#FFFFFF", fg="#34495E").pack(pady=5)

        tutors = get_all_tutors()
        tutor_names = [t[1] for t in tutors]
        tutor_ids = {t[1]: t[0] for t in tutors}

        tutor_entry = ttk.Combobox(popup, values=tutor_names, state="readonly")
        tutor_entry.pack(pady=5)

        tk.Button(
            popup,
            text="Book Session",
            font=("Segoe UI", 11, "bold"),
            bg="#3498DB",
            fg="white",
            relief="flat",
            padx=15,
            pady=6,
            command=lambda: book_session_action(
                cal.get_date(),
                tutor_ids.get(tutor_entry.get()),
                popup
            )
        ).pack(pady=15)

    def get_all_tutors():
        conn = sqlite3.connect(DB_PATH)
        print("Using DB:", DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT tutor_id, name FROM tutor")
        tutors = cursor.fetchall()
        conn.close()
        return tutors

    def book_session_action(date, tutor_id, popup):
        if not date or not tutor_id:
            messagebox.showerror("Error", "Please select all fields.")
            return

        book_new_session(student_id, tutor_id, date)
        popup.destroy()
        refresh_dashboard()
        messagebox.showinfo("Success", "Session booked successfully.")

    def cancel_session_action(meeting_id):
        cancel_session(meeting_id)
        refresh_dashboard()
        messagebox.showinfo("Success", "Session cancelled.")

    def view_notes_popup(notes):
        popup = tk.Toplevel(window)
        popup.iconbitmap("assets/blank.ico")
        popup.title("Session Notes")
        popup.geometry("400x300")
        popup.configure(bg="#FFFFFF")

        tk.Label(
            popup,
            text="Session Notes",
            font=("Segoe UI", 14, "bold"),
            bg="#FFFFFF",
            fg="#2C3E50"
        ).pack(pady=10)

        notes_box = tk.Text(
            popup,
            width=45,
            height=10,
            font=("Segoe UI", 11),
            bg="#FAFAFA",
            bd=1,
            relief="solid"
        )
        notes_box.pack(padx=20)
        notes_box.insert("1.0", notes)

    def show_history():
        messagebox.showinfo("Info", "Scroll down to see your completed sessions.")

    refresh_dashboard()
    window.mainloop()
