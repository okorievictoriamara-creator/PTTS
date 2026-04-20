import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# -------------------- DATABASE PATH --------------------
DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "database",
    "ptts.db"
)


def get_connection():
    return sqlite3.connect(DB_PATH)


# -------------------- DATA HELPERS --------------------

def get_children_of_parent(parent_id):
    """Returns all child IDs linked to this parent."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT child_id FROM parent WHERE parent_id = ?", (parent_id,))
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]


def get_user_info(user_id):
    """Returns username and role for a given user."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, role FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row if row else ("Unknown", "Unknown")


def get_child_sessions(child_id):
    """Returns all sessions for a specific child."""
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
        WHERE m.student_id = ?
        ORDER BY m.date DESC
    """, (child_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_child_counts(child_id):
    """Returns total, upcoming, completed counts for a child."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM meetings WHERE student_id=? AND completed=0", (child_id,))
    upcoming = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM meetings WHERE student_id=? AND completed=1", (child_id,))
    completed = cur.fetchone()[0]

    total = upcoming + completed

    conn.close()
    return total, upcoming, completed


# -------------------- MAIN PARENT DASHBOARD --------------------

def launch_parent_dashboard(parent_id, parent_name="Parent"):
    window = tk.Toplevel()
    window.iconbitmap("assets/blank.ico")
    window.title("PTTS - Parent Dashboard")
    window.geometry("1300x820")
    window.configure(bg="#F5F7FA")

    # -------------------- HEADER --------------------
    header = tk.Frame(window, bg="#FFFFFF", height=70)
    header.pack(fill="x")

    tk.Label(
        header,
        text=f"Welcome, {parent_name}",
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

    # -------------------- CHILD SELECTOR --------------------
    selector_frame = tk.Frame(main, bg="#F5F7FA")
    selector_frame.pack(fill="x", pady=(0, 10))

    tk.Label(selector_frame, text="Select Child:", font=("Segoe UI", 11, "bold"),
             bg="#F5F7FA", fg="#2C3E50").pack(side="left", padx=10)

    children_ids = get_children_of_parent(parent_id)
    children_names = [get_user_info(cid)[0] for cid in children_ids]

    child_var = tk.StringVar()
    child_dropdown = ttk.Combobox(selector_frame, textvariable=child_var,
                                  values=children_names, state="readonly", width=30)
    child_dropdown.pack(side="left", padx=10)

    # -------------------- CHILD DASHBOARD AREA --------------------
    child_area = tk.Frame(main, bg="#F5F7FA")
    child_area.pack(fill="both", expand=True)

    def refresh_child_dashboard(*args):
        for widget in child_area.winfo_children():
            widget.destroy()

        if not child_var.get():
            return

        selected_index = children_names.index(child_var.get())
        child_id = children_ids[selected_index]

        build_child_dashboard(child_area, child_id)

    child_dropdown.bind("<<ComboboxSelected>>", refresh_child_dashboard)

    # Auto-select first child if available
    if children_names:
        child_dropdown.current(0)
        refresh_child_dashboard()

    window.mainloop()


# -------------------- CHILD DASHBOARD BUILDER --------------------

def build_child_dashboard(parent_frame, child_id):
    child_name, _ = get_user_info(child_id)
    total, upcoming, completed = get_child_counts(child_id)

    # -------------------- TOP ROW: CARDS + STACKED BAR --------------------
    top_row = tk.Frame(parent_frame, bg="#F5F7FA")
    top_row.pack(fill="x")

    analytics_frame = tk.Frame(top_row, bg="#F5F7FA", width=850)
    analytics_frame.pack(side="left", anchor="n")
    analytics_frame.pack_propagate(False)

    chart_frame = tk.Frame(top_row, bg="#F5F7FA", width=420, height=120)
    chart_frame.pack(side="right", anchor="n", padx=10)
    chart_frame.pack_propagate(False)

    # -------------------- CHILD PROFILE CARD --------------------
    profile_card = tk.Frame(analytics_frame, bg="#2980B9", width=200, height=90)
    profile_card.pack_propagate(False)
    profile_card.pack(side="left", padx=10, pady=10)

    tk.Label(profile_card, text="Child", font=("Segoe UI", 11), bg="#2980B9", fg="white").pack(anchor="w", padx=10)
    tk.Label(profile_card, text=child_name, font=("Segoe UI", 18, "bold"),
             bg="#2980B9", fg="white").pack(anchor="w", padx=10)

    # -------------------- ANALYTICS CARDS --------------------
    def create_stat_card(parent, title, value, color):
        frame = tk.Frame(parent, bg=color, width=200, height=90)
        frame.pack_propagate(False)
        frame.pack(side="left", padx=10, pady=10)

        tk.Label(frame, text=title, font=("Segoe UI", 11), bg=color, fg="white").pack(anchor="w", padx=10)
        tk.Label(frame, text=str(value), font=("Segoe UI", 20, "bold"), bg=color, fg="white").pack(anchor="w", padx=10)

    create_stat_card(analytics_frame, "Total Sessions", total, "#9B59B6")
    create_stat_card(analytics_frame, "Upcoming", upcoming, "#F1C40F")
    create_stat_card(analytics_frame, "Completed", completed, "#27AE60")

    # -------------------- THIN STACKED BAR CHART --------------------
    sns.set_theme(style="whitegrid")

    fig = Figure(figsize=(4.5, 0.6), dpi=100)
    ax = fig.add_subplot(111)

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

    tk.Label(chart_frame, text=f"Completed: {completed}", font=("Segoe UI", 9),
             bg="#F5F7FA").pack(anchor="w", padx=10)
    tk.Label(chart_frame, text=f"Upcoming:  {upcoming}", font=("Segoe UI", 9),
             bg="#F5F7FA").pack(anchor="w", padx=10)

    # -------------------- ACTION CARDS --------------------
    cards_frame = tk.Frame(parent_frame, bg="#F5F7FA")
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

    create_action_card(cards_frame, "Book a Session", "Schedule a new session", "#8E44AD", coming_soon=True)
    create_action_card(cards_frame, "View All Sessions", "See all sessions", "#16A085",
                       command=lambda: open_child_sessions_window(child_id))
    create_action_card(cards_frame, "Notes", "Tutor notes", "#7F8C8D", coming_soon=True)

    # -------------------- TABLES --------------------
    build_child_tables(parent_frame, child_id)


# -------------------- TABLE BUILDER --------------------

def build_child_tables(parent_frame, child_id):
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
                    background="#2C3E50",
                    foreground="black",
                    relief="flat")
    style.map("Modern.Treeview.Heading",
              background=[("active", "#34495E"), ("!active", "#00070E")],
              foreground=[("active", "white"), ("!active", "black")])

    # -------------------- UPCOMING TABLE --------------------
    upcoming_frame = tk.Frame(parent_frame, bg="#FFFFFF", bd=1, relief="solid")
    upcoming_frame.pack(fill="both", expand=True, pady=(0, 10))

    tk.Label(upcoming_frame, text="Upcoming Sessions", font=("Segoe UI", 12, "bold"),
             bg="#FFFFFF", fg="#2C3E50").pack(anchor="w", padx=15, pady=10)

    cols = ("meeting_id", "tutor", "date", "status")
    tree_up = ttk.Treeview(upcoming_frame, columns=cols, show="headings", style="Modern.Treeview")
    tree_up.pack(fill="both", expand=True, padx=15, pady=(0, 10))

    for c in cols:
        tree_up.heading(c, text=c.capitalize())
        tree_up.column(c, width=180)

    sessions = get_child_sessions(child_id)
    upcoming = [s for s in sessions if s[4] == 0]

    for index, row in enumerate(upcoming):
        meeting_id, student, tutor, date, completed_flag = row
        status = "🟡 Upcoming"
        tag = "oddrow" if index % 2 else "evenrow"
        tree_up.insert("", "end", values=(meeting_id, tutor, date, status), tags=(tag,))

    tree_up.tag_configure("oddrow", background="#F7F9FC")
    tree_up.tag_configure("evenrow", background="#FFFFFF")

    # -------------------- COMPLETED TABLE --------------------
    completed_frame = tk.Frame(parent_frame, bg="#FFFFFF", bd=1, relief="solid")
    completed_frame.pack(fill="both", expand=True, pady=(0, 10))

    tk.Label(completed_frame, text="Completed Sessions", font=("Segoe UI", 12, "bold"),
             bg="#FFFFFF", fg="#2C3E50").pack(anchor="w", padx=15, pady=10)

    tree_co = ttk.Treeview(completed_frame, columns=cols, show="headings", style="Modern.Treeview")
    tree_co.pack(fill="both", expand=True, padx=15, pady=(0, 10))

    for c in cols:
        tree_co.heading(c, text=c.capitalize())
        tree_co.column(c, width=180)

    completed = [s for s in sessions if s[4] == 1]

    for index, row in enumerate(completed):
        meeting_id, student, tutor, date, completed_flag = row
        status = "🟢 Completed"
        tag = "oddrow" if index % 2 else "evenrow"
        tree_co.insert("", "end", values=(meeting_id, tutor, date, status), tags=(tag,))

    tree_co.tag_configure("oddrow", background="#F7F9FC")
    tree_co.tag_configure("evenrow", background="#FFFFFF")


# -------------------- CHILD SESSIONS WINDOW --------------------

def open_child_sessions_window(child_id):
    win = tk.Toplevel()
    win.iconbitmap("assets/blank.ico")
    win.title("All Sessions")
    win.geometry("900x500")
    win.configure(bg="white")

    tk.Label(win, text="All Sessions", font=("Segoe UI", 14, "bold"),
             bg="white").pack(anchor="w", padx=15, pady=10)

    cols = ("meeting_id", "tutor", "date", "status")
    tree = ttk.Treeview(win, columns=cols, show="headings")
    tree.pack(fill="both", expand=True, padx=15, pady=10)

    for c in cols:
        tree.heading(c, text=c.capitalize())
        tree.column(c, width=180)

    sessions = get_child_sessions(child_id)

    for row in sessions:
        meeting_id, student, tutor, date, completed_flag = row
        status = "🟢 Completed" if completed_flag == 1 else "🟡 Upcoming"
        tree.insert("", "end", values=(meeting_id, tutor, date, status))
