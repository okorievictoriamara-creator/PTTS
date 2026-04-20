import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure




# -------------------- DATABASE PATH --------------------
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "database",
    "ptts.db"
)


def get_connection():
    return sqlite3.connect(DB_PATH)


# -------------------- DATA HELPERS --------------------

def get_counts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users WHERE role='tutor'")
    total_tutors = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE role='student'")
    total_students = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM meetings WHERE completed=0")
    upcoming = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM meetings WHERE completed=1")
    completed = cur.fetchone()[0]

    conn.close()

    return {
        "total_tutors": total_tutors,
        "total_students": total_students,
        "upcoming": upcoming,
        "completed": completed
    }


def get_users_by_role(role):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT userid, username, role
        FROM users
        WHERE role = ?
    """, (role,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_all_sessions():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.meeting_id,
               s.username AS student,
               t.username AS tutor,
               m.date,
               m.completed
        FROM meetings m
        JOIN users s ON m.student_id = s.userid
        JOIN users t ON m.tutor_id = t.userid
        ORDER BY m.date DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_recent_sessions(limit=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.meeting_id,
               s.username AS student,
               t.username AS tutor,
               m.date,
               m.completed
        FROM meetings m
        JOIN users s ON m.student_id = s.user_id
        JOIN users t ON m.tutor_id = t.user_id
        ORDER BY m.date DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows


# -------------------- MAIN ADMIN DASHBOARD --------------------

def launch_admin_dashboard(admin_name="Admin"):
    window = tk.Toplevel()
    window.iconbitmap("assets/blank.ico")
    window.title("PTTS - Admin Dashboard")
    window.geometry("1300x820")
    window.configure(bg="#F5F7FA")

    # -------------------- HEADER --------------------
    header = tk.Frame(window, bg="#FFFFFF", height=70)
    header.pack(fill="x")

    tk.Label(
        header,
        text=f"Welcome, {admin_name}",
        font=("Segoe UI", 20, "bold"),
        bg="#FFFFFF",
        fg="#2C3E50"
    ).pack(side="left", padx=25, pady=15)

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
        command=window.destroy
    ).pack(side="right", padx=25)

    # -------------------- MAIN AREA --------------------
    main = tk.Frame(window, bg="#F5F7FA")
    main.pack(fill="both", expand=True, padx=20, pady=10)

    # -------------------- TOP ROW: CARDS + STACKED BAR --------------------
    top_row = tk.Frame(main, bg="#F5F7FA")
    top_row.pack(fill="x")

    analytics_frame = tk.Frame(top_row, bg="#F5F7FA", width=850)
    analytics_frame.pack(side="left", anchor="n")
    analytics_frame.pack_propagate(False)

    chart_frame = tk.Frame(top_row, bg="#F5F7FA", width=420, height=120)
    chart_frame.pack(side="right", anchor="n", padx=10)
    chart_frame.pack_propagate(False)

    # -------------------- ANALYTICS CARDS --------------------
    counts = get_counts()

    def create_stat_card(parent, title, value, color):
        frame = tk.Frame(parent, bg=color, width=200, height=90)
        frame.pack_propagate(False)
        frame.pack(side="left", padx=10, pady=10)

        tk.Label(frame, text=title, font=("Segoe UI", 11), bg=color, fg="white").pack(anchor="w", padx=10)
        tk.Label(frame, text=str(value), font=("Segoe UI", 20, "bold"), bg=color, fg="white").pack(anchor="w", padx=10)

    create_stat_card(analytics_frame, "Total Tutors", counts["total_tutors"], "#3498DB")
    create_stat_card(analytics_frame, "Total Students", counts["total_students"], "#9B59B6")
    create_stat_card(analytics_frame, "Upcoming Sessions", counts["upcoming"], "#F1C40F")
    create_stat_card(analytics_frame, "Completed Sessions", counts["completed"], "#27AE60")

    # -------------------- THIN STACKED BAR CHART --------------------
    sns.set_theme(style="whitegrid")

    fig = Figure(figsize=(4.5, 0.6), dpi=100)
    ax = fig.add_subplot(111)

    completed = counts["completed"]
    upcoming = counts["upcoming"]

    colors = sns.color_palette("Set2", 2)

    ax.barh([""], completed, color=colors[0])
    ax.barh([""], upcoming, left=completed, color=colors[1])

    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_title("Sessions Overview", fontsize=10)

    sns.despine(left=True, bottom=True)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=(5, 0))

    tk.Label(chart_frame, text=f"Completed: {completed}", font=("Segoe UI", 9), bg="#F5F7FA").pack(anchor="w", padx=10)
    tk.Label(chart_frame, text=f"Upcoming:  {upcoming}", font=("Segoe UI", 9), bg="#F5F7FA").pack(anchor="w", padx=10)

    # -------------------- ACTION CARDS --------------------
    cards_frame = tk.Frame(main, bg="#F5F7FA")
    cards_frame.pack(fill="x", pady=20)

    def create_action_card(parent, title, subtitle, color, command=None, coming_soon=False):
        frame = tk.Frame(parent, bg=color, width=200, height=120, bd=1, relief="solid")
        frame.pack_propagate(False)
        frame.pack(side="left", padx=10)

        tk.Label(frame, text=title, font=("Segoe UI", 12, "bold"), bg=color, fg="white").pack(anchor="w", padx=10)
        tk.Label(frame, text=subtitle, font=("Segoe UI", 10), bg=color, fg="#ECF0F1").pack(anchor="w", padx=10)

        if coming_soon:
            tk.Label(frame, text="Coming Soon", font=("Segoe UI", 9, "bold"),
                     bg="#E74C3C", fg="white", padx=6, pady=2).pack(anchor="e", padx=8, pady=4)
        else:
            tk.Button(frame, text="Open", font=("Segoe UI", 9, "bold"),
                      bg="#2C3E50", fg="white", relief="flat",
                      padx=10, pady=4, cursor="hand2",
                      command=command).pack(anchor="e", padx=8, pady=4)

    def open_manage_tutors():
        open_user_window("tutor", "Manage Tutors")

    def open_manage_students():
        open_user_window("student", "Manage Students")

    def open_sessions():
        open_sessions_window()

    create_action_card(cards_frame, "Manage Tutors", "View and manage tutors", "#2980B9", open_manage_tutors)
    create_action_card(cards_frame, "Manage Students", "View and manage students", "#8E44AD", open_manage_students)
    create_action_card(cards_frame, "View All Sessions", "See all scheduled sessions", "#16A085", open_sessions)
    create_action_card(cards_frame, "Approvals", "Coming Soon", "#D35400", coming_soon=True)
    create_action_card(cards_frame, "Subjects", "Coming Soon", "#7F8C8D", coming_soon=True)
    create_action_card(cards_frame, "System Settings", "Coming Soon", "#7F8C8D", coming_soon=True)

    # -------------------- RECENT MEETINGS TABLE (MODERN) --------------------
    bottom_frame = tk.Frame(main, bg="#FFFFFF", bd=1, relief="solid")
    bottom_frame.pack(fill="both", expand=True, pady=(0, 5))

    tk.Label(
        bottom_frame,
        text="Recent Meetings",
        font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF",
        fg="#2C3E50"
    ).pack(anchor="w", padx=15, pady=10)

    # Modern Treeview style
    style = ttk.Style()
    style.configure("Modern.Treeview",
                    background="#FFFFFF",
                    foreground="#2C3E50",
                    rowheight=32,
                    fieldbackground="#FFFFFF",
                    bordercolor="#E0E6ED",
                    borderwidth=0)
    style.configure("Modern.Treeview.Heading",
                    font=("Segoe UI", 10, "bold"),
                    background="#010F1D",
                    foreground="black",
                    relief="flat")
    # style.map("Modern.Treeview.Heading",
    #           background=[("!active", "#001020"), ("active", "#34495E")],
    #           foreground=[("!active", "black"), ("active", "black")])

    cols = ("meeting_id", "student", "tutor", "date", "status")
    tree = ttk.Treeview(bottom_frame, columns=cols, show="headings", style="Modern.Treeview")
    tree.pack(fill="both", expand=True, padx=15, pady=(0, 10))

    # Column widths
    tree.column("meeting_id", width=90)
    tree.column("student", width=180)
    tree.column("tutor", width=180)
    tree.column("date", width=10)
    tree.column("status", width=160)

    # Headings
    for c in cols:
        tree.heading(c, text=c.capitalize())

    # Insert rows with zebra striping + emoji pills
    recent = get_recent_sessions(limit=10)
    for index, row in enumerate(recent):
        meeting_id, student, tutor, date, completed_flag = row
        status = "🟢 Completed" if completed_flag == 1 else "🟡 Upcoming"

        tag = "oddrow" if index % 2 else "evenrow"
        tree.insert("", "end", values=(meeting_id, student, tutor, date, status), tags=(tag,))

    tree.tag_configure("oddrow", background="#F7F9FC")
    tree.tag_configure("evenrow", background="#FFFFFF")

    # -------------------- SUBWINDOWS --------------------

    def open_user_window(role, title):
        win = tk.Toplevel(window)
        win.title(title)
        win.geometry("800x500")
        win.configure(bg="white")

        tk.Label(win, text=title, font=("Segoe UI", 14, "bold"), bg="white").pack(anchor="w", padx=15, pady=10)

        cols_u = ("userid", "username", "role")
        tree_u = ttk.Treeview(win, columns=cols_u, show="headings")
        for c in cols_u:
            tree_u.heading(c, text=c.capitalize())
            tree_u.column(c, width=200)
        tree_u.pack(fill="both", expand=True, padx=15, pady=10)

        for row in get_users_by_role(role):
            tree_u.insert("", "end", values=row)

    def open_sessions_window():
        win = tk.Toplevel(window)
        win.iconbitmap("assets/blank.ico")
        win.title("All Sessions")
        win.geometry("900x500")
        win.configure(bg="white")

        tk.Label(win, text="All Sessions", font=("Segoe UI", 14, "bold"), bg="white").pack(anchor="w", padx=15, pady=10)

        cols_s = ("meeting_id", "student", "tutor", "date", "status")
        tree_s = ttk.Treeview(win, columns=cols_s, show="headings")
        for c in cols_s:
            tree_s.heading(c, text=c.capitalize())
            tree_s.column(c, width=160)
        tree_s.pack(fill="both", expand=True, padx=15, pady=10)

        for row in get_all_sessions():
            meeting_id, student, tutor, date, completed_flag = row
            status = "🟢 Completed" if completed_flag == 1 else "🟡 Upcoming"
            tree_s.insert("", "end", values=(meeting_id, student, tutor, date, status))

    window.mainloop()
