import tkinter as tk
from tkinter import messagebox
from modules.auth import authenticate
from modules.ui_components import go_home, load_logo, rounded_card

def launch_student():
    window = tk.Toplevel()
    window.iconbitmap("assets/blank.ico")
    window.title("PTTS - Student Sign In")
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
    tk.Label(window, image=logo, bg="#f4f4f4").pack(pady=10)
    window.logo = logo

    # Title
    tk.Label(window, text="Student Sign In", font=("Helvetica", 28, "bold"),
             bg="#f4f4f4").pack(pady=10)

    # Rounded card
    card = rounded_card(window)

    # Username
    tk.Label(card, text="Username", font=("Helvetica", 12), bg="white").pack(anchor="w")
    username_entry = tk.Entry(card, width=30, font=("Helvetica", 12))
    username_entry.pack(pady=5)

    # Password
    tk.Label(card, text="Password", font=("Helvetica", 12), bg="white").pack(anchor="w")
    password_entry = tk.Entry(card, width=30, font=("Helvetica", 12), show="*")
    password_entry.pack(pady=5)

    # Authentication Logic
    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()

        result = authenticate(username, password, role="student")

        if result is None:
            messagebox.showerror("Login Failed", "Invalid login credentials. Contact IT support.")
            return

        if result["role"] != "student":
            messagebox.showerror("Access Denied", "This account is not a student account.")
            return

        # window.destroy()
        from modules.student_dashboard import launch_student_dashboard
        launch_student_dashboard(result["user_id"], result["name"])


    # Sign In Button
    tk.Button(
        card, text="Sign In", font=("Helvetica", 12, "bold"),
        bg="#4da6ff", fg="white", width=20, cursor="hand2",
        relief="flat", command=attempt_login
    ).pack(pady=20)

    # Footer
    tk.Label(window, text="Contact IT support for sign-in issues",
             font=("Helvetica", 10, "italic"), bg="#f4f4f4", fg="#777").pack(pady=20)

    window.mainloop()
