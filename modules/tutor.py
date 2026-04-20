import tkinter as tk
from tkinter import messagebox
from modules.auth import authenticate
from modules.ui_components import go_home, load_logo
from modules.tutor_dashboard import launch_tutor_dashboard


def launch_tutor():
    window = tk.Toplevel()
    window.iconbitmap("assets/blank.ico")
    window.title("PTTS - Tutor Sign In")
    window.geometry("900x600")
    window.configure(bg="#f4f4f4")

    # Back to Home
    tk.Button(
        window, text="← Back to Home", font=("Helvetica", 11, "bold"),
        bg="#f4f4f4", fg="#007acc", bd=0, cursor="hand2",
        command=lambda: go_home(window)
    ).pack(anchor="w", padx=20, pady=10)

    # Logo
    logo = load_logo()
    if logo:
        tk.Label(window, image=logo, bg="#f4f4f4").pack(pady=10)
        window.logo = logo

    # Title
    tk.Label(
        window, text="Tutor Sign In",
        font=("Helvetica", 28, "bold"), bg="#f4f4f4"
    ).pack(pady=10)

    # Username
    tk.Label(window, text="Username:", font=("Helvetica", 14), bg="#f4f4f4").pack()
    username_entry = tk.Entry(window, font=("Helvetica", 14), width=30)
    username_entry.pack(pady=5)

    # Password
    tk.Label(window, text="Password:", font=("Helvetica", 14), bg="#f4f4f4").pack()
    password_entry = tk.Entry(window, font=("Helvetica", 14), width=30, show="*")
    password_entry.pack(pady=5)

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()

        user = authenticate(username, password, role="tutor")
        if user:
            tutor_id = user["tutor_id"]
            tutor_name = user["name"]
            subject = user["subject"]
            window.destroy()
            launch_tutor_dashboard(tutor_id, tutor_name, subject)

        else:
            messagebox.showerror("Error", "Invalid tutor credentials.")

    tk.Button(
        window, text="Sign In",
        font=("Helvetica", 14, "bold"),
        bg="#4da6ff", fg="white",
        width=20, cursor="hand2",
        command=attempt_login
    ).pack(pady=20)

    tk.Label(
        window, text="Contact IT support for sign-in issues.",
        font=("Helvetica", 10), bg="#f4f4f4", fg="gray"
    ).pack(pady=10)

    window.mainloop()
