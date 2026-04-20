import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
from modules.meetings import get_tutor_meetings, mark_meeting_completed, update_meeting_notes
from modules.ui_components import go_home


def launch_tutor_dashboard(tutor_id, tutor_name, subject):
    window = tk.Toplevel()
    window.iconbitmap("assets/blank.ico")
    window.title("PTTS - Tutor Dashboard")
    window.geometry("1250x760")  # slightly shorter height
    window.configure(bg="#F5F7FA")

    # ---------------- HEADER ----------------
    header = tk.Frame(window, bg="#FFFFFF", height=70)
    header.pack(fill="x")

    tk.Label(
        header,
        text=f"Welcome, {tutor_name}",
        font=("Segoe UI", 20, "bold"),
        bg="#FFFFFF",
        fg="#2C3E50"
    ).pack(side="left", padx=25, pady=15)

    tk.Label(
        header,
        text=f"Subject: {subject}",
        font=("Segoe UI", 11),
        bg="#FFFFFF",
        fg="#7F8C8D"
    ).pack(side="left", padx=10)

    tk.Button(
        header,
        text="Logout",
        font=("Segoe UI", 10, "bold"),
        bg="#E74C3C",
        fg="white",
        relief="flat",
        padx=12,
        pady=4,
        cursor="hand2",
        command=lambda: go_home(window)
    ).pack(side="right", padx=25)

    # ---------------- SUMMARY CARDS ----------------
    summary_frame = tk.Frame(window, bg="#F5F7FA")
    summary_frame.pack(fill="x", padx=25, pady=8)

    card_style = {"font": ("Segoe UI", 13, "bold"), "bg": "#FFFFFF", "fg": "#2C3E50"}

    upcoming_card = tk.Frame(summary_frame, bg="#FFFFFF", bd=1, relief="solid")
    upcoming_card.pack(side="left", padx=8)
    tk.Label(upcoming_card, text="Upcoming Sessions", **card_style).pack(padx=15, pady=8)
    upcoming_count_label = tk.Label(
        upcoming_card,
        text="0",
        font=("Segoe UI", 22, "bold"),
        bg="#FFFFFF",
        fg="#3498DB"
    )
    upcoming_count_label.pack(pady=5)

    completed_card = tk.Frame(summary_frame, bg="#FFFFFF", bd=1, relief="solid")
    completed_card.pack(side="left", padx=8)
    tk.Label(completed_card, text="Completed Sessions", **card_style).pack(padx=15, pady=8)
    completed_count_label = tk.Label(
        completed_card,
        text="0",
        font=("Segoe UI", 22, "bold"),
        bg="#FFFFFF",
        fg="#27AE60"
    )
    completed_count_label.pack(pady=5)

    # ---------------- MAIN LAYOUT ----------------
    main = tk.Frame(window, bg="#F5F7FA")
    main.pack(fill="both", expand=True, padx=20, pady=10)
    main.columnconfigure(0, weight=1)
    main.columnconfigure(1, weight=2)

    # ---------------- LEFT: CALENDAR ----------------
    left_frame = tk.Frame(main, bg="#FFFFFF", bd=1, relief="solid")
    left_frame.grid(row=0, column=0, sticky="nsew", padx=10)

    tk.Label(
        left_frame,
        text="Session Calendar",
        font=("Segoe UI", 15, "bold"),
        bg="#FFFFFF",
        fg="#34495E"
    ).pack(anchor="w", padx=15, pady=8)

    cal = Calendar(left_frame, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(padx=15, pady=10)

    # ---------------- RIGHT SIDE ----------------
    right_frame = tk.Frame(main, bg="#F5F7FA")
    right_frame.grid(row=0, column=1, sticky="nsew", padx=10)

    # ============================================================
    # ⭐ UPCOMING SESSIONS TABLE (MEDIUM HEIGHT)
    # ============================================================
    upcoming_frame = tk.Frame(right_frame, bg="#FFFFFF", bd=1, relief="solid")
    upcoming_frame.pack(fill="x", pady=8)

    tk.Label(
        upcoming_frame,
        text="Upcoming Sessions (Next 7 Days)",
        font=("Segoe UI", 13, "bold"),
        bg="#FFFFFF",
        fg="#2C3E50"
    ).pack(anchor="w", padx=15, pady=8)

    upcoming_table_container = tk.Frame(upcoming_frame, bg="#FFFFFF")
    upcoming_table_container.pack(fill="x", padx=15)

    upcoming_scrollbar = tk.Scrollbar(upcoming_table_container, orient="vertical")
    upcoming_tree = ttk.Treeview(
        upcoming_table_container,
        columns=("Student", "Date", "Notes"),
        show="headings",
        height=4,   # MEDIUM height
        yscrollcommand=upcoming_scrollbar.set
    )
    upcoming_scrollbar.config(command=upcoming_tree.yview)
    upcoming_scrollbar.pack(side="right", fill="y")
    upcoming_tree.pack(side="left", fill="x", expand=True)

    for col in ("Student", "Date", "Notes"):
        upcoming_tree.heading(col, text=col)
        upcoming_tree.column(col, width=180 if col != "Notes" else 350)

    upcoming_tree.tag_configure("highlight", background="#D6EAF8")

    def highlight_upcoming(event=None):
        for item in upcoming_tree.get_children():
            upcoming_tree.item(item, tags="")
        selected = upcoming_tree.selection()
        if selected:
            upcoming_tree.item(selected[0], tags=("highlight",))

    upcoming_tree.bind("<<TreeviewSelect>>", highlight_upcoming)

    # Buttons
    upcoming_btn_frame = tk.Frame(upcoming_frame, bg="#FFFFFF")
    upcoming_btn_frame.pack(pady=5)

    tk.Button(
        upcoming_btn_frame,
        text="Mark Completed",
        font=("Segoe UI", 10, "bold"),
        bg="#27AE60",
        fg="white",
        relief="flat",
        padx=12,
        pady=4,
        command=lambda: mark_from_table(upcoming_tree, completed=False)
    ).pack(side="left", padx=8)

    tk.Button(
        upcoming_btn_frame,
        text="Add Notes",
        font=("Segoe UI", 10, "bold"),
        bg="#2980B9",
        fg="white",
        relief="flat",
        padx=12,
        pady=4,
        command=lambda: notes_from_table(upcoming_tree)
    ).pack(side="left", padx=8)

    # ============================================================
    # ⭐ COMPLETED SESSIONS TABLE (MEDIUM HEIGHT)
    # ============================================================
    completed_frame = tk.Frame(right_frame, bg="#FFFFFF", bd=1, relief="solid")
    completed_frame.pack(fill="x", pady=8)

    tk.Label(
        completed_frame,
        text="Completed Sessions (Past 7 Days)",
        font=("Segoe UI", 13, "bold"),
        bg="#FFFFFF",
        fg="#2C3E50"
    ).pack(anchor="w", padx=15, pady=8)

    completed_table_container = tk.Frame(completed_frame, bg="#FFFFFF")
    completed_table_container.pack(fill="x", padx=15)

    completed_scrollbar = tk.Scrollbar(completed_table_container, orient="vertical")
    completed_tree = ttk.Treeview(
        completed_table_container,
        columns=("Student", "Date", "Notes"),
        show="headings",
        height=4,   # MEDIUM height
        yscrollcommand=completed_scrollbar.set
    )
    completed_scrollbar.config(command=completed_tree.yview)
    completed_scrollbar.pack(side="right", fill="y")
    completed_tree.pack(side="left", fill="x", expand=True)

    for col in ("Student", "Date", "Notes"):
        completed_tree.heading(col, text=col)
        completed_tree.column(col, width=180 if col != "Notes" else 350)

    completed_tree.tag_configure("highlight", background="#E8DAEF")

    def highlight_completed(event=None):
        for item in completed_tree.get_children():
            completed_tree.item(item, tags="")
        selected = completed_tree.selection()
        if selected:
            completed_tree.item(selected[0], tags=("highlight",))

    completed_tree.bind("<<TreeviewSelect>>", highlight_completed)

    # Buttons
    completed_btn_frame = tk.Frame(completed_frame, bg="#FFFFFF")
    completed_btn_frame.pack(pady=5)

    tk.Button(
        completed_btn_frame,
        text="Add/Edit Notes",
        font=("Segoe UI", 10, "bold"),
        bg="#8E44AD",
        fg="white",
        relief="flat",
        padx=12,
        pady=4,
        command=lambda: notes_from_table(completed_tree)
    ).pack(side="left", padx=8)

    # ============================================================
    # ⭐ FUNCTIONS
    # ============================================================
    def refresh_dashboard():
        upcoming_tree.delete(*upcoming_tree.get_children())
        completed_tree.delete(*completed_tree.get_children())

        today = datetime.today().date()
        upcoming_cutoff = today + timedelta(days=7)
        completed_cutoff = today - timedelta(days=7)

        upcoming_sessions = [
            m for m in get_tutor_meetings(tutor_id, completed=False)
            if datetime.strptime(m[2], "%Y-%m-%d").date() <= upcoming_cutoff
        ]
        completed_sessions = [
            m for m in get_tutor_meetings(tutor_id, completed=True)
            if datetime.strptime(m[2], "%Y-%m-%d").date() >= completed_cutoff
        ]

        upcoming_count_label.config(text=str(len(upcoming_sessions)))
        completed_count_label.config(text=str(len(completed_sessions)))

        for m in upcoming_sessions:
            upcoming_tree.insert("", "end", values=(m[1], m[2], m[3]))

        for m in completed_sessions:
            completed_tree.insert("", "end", values=(m[1], m[2], m[3]))

    def mark_from_table(tree, completed):
        selection = tree.selection()
        if not selection:
            messagebox.showerror("Error", "Select a session first.")
            return

        student, date, notes = tree.item(selection[0], "values")

        meetings = get_tutor_meetings(tutor_id, completed=completed)
        meeting_id = None
        for m in meetings:
            if m[1] == student and m[2] == date:
                meeting_id = m[0]
                break

        if meeting_id is None:
            messagebox.showerror("Error", "Session not found.")
            return

        mark_meeting_completed(meeting_id)
        messagebox.showinfo("Success", "Session marked as completed.")
        refresh_dashboard()

    def notes_from_table(tree):
        selection = tree.selection()
        if not selection:
            messagebox.showerror("Error", "Select a session first.")
            return

        student, date, notes = tree.item(selection[0], "values")

        all_meetings = get_tutor_meetings(tutor_id, completed=False) + \
                       get_tutor_meetings(tutor_id, completed=True)

        meeting_id = None
        for m in all_meetings:
            if m[1] == student and m[2] == date:
                meeting_id = m[0]
                break

        if meeting_id is None:
            messagebox.showerror("Error", "Session not found.")
            return

        open_notes_popup(meeting_id, notes)

    def open_notes_popup(meeting_id, current_notes):
        popup = tk.Toplevel(window)
        popup.iconbitmap("assets/blank.ico")
        popup.title("Add Notes")
        popup.geometry("450x350")
        popup.configure(bg="#FFFFFF")

        tk.Label(
            popup,
            text="Notes",
            font=("Segoe UI", 14, "bold"),
            bg="#FFFFFF",
            fg="#2C3E50"
        ).pack(pady=10)

        notes_box = tk.Text(
            popup,
            width=50,
            height=12,
            font=("Segoe UI", 11),
            bg="#FAFAFA",
            bd=1,
            relief="solid"
        )
        notes_box.pack(padx=20)
        notes_box.insert("1.0", current_notes)

        tk.Button(
            popup,
            text="Save",
            font=("Segoe UI", 12, "bold"),
            bg="#27AE60",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            command=lambda: save_notes(meeting_id, notes_box.get("1.0", tk.END).strip(), popup)
        ).pack(pady=15)

    def save_notes(meeting_id, new_notes, popup):
        update_meeting_notes(meeting_id, new_notes)
        popup.destroy()
        refresh_dashboard()
        messagebox.showinfo("Success", "Notes updated.")

    refresh_dashboard()
    window.mainloop()
