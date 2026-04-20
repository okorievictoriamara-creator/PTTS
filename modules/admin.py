import tkinter as tk
from tkinter import messagebox
from modules.auth import authenticate
from modules.admin_dashboard import launch_admin_dashboard
from modules.ui_components import go_home, load_logo, rounded_card

def launch_admin():
    window = tk.Toplevel()
    window.iconbitmap("assets/blank.ico")
    window.title("PTTS - Admin Sign In")
    window.geometry("900x600")
    window.configure(bg="#f4f4f4")

    tk.Button(window, text="← Back to Home", font=("Helvetica", 11, "bold"),
              bg="#f4f4f4", fg="#007acc", bd=0, cursor="hand2",
              command=lambda: go_home(window)).pack(anchor="w", padx=20, pady=10)

    logo = load_logo()
    tk.Label(window, image=logo, bg="#f4f4f4").pack(pady=10)
    window.logo = logo

    tk.Label(window, text="Admin Sign In", font=("Helvetica", 28, "bold"),
             bg="#f4f4f4").pack(pady=10)

    card = rounded_card(window)

    tk.Label(card, text="Username", font=("Helvetica", 12), bg="white").pack(anchor="w")
    username_entry = tk.Entry(card, width=30, font=("Helvetica", 12))
    username_entry.pack(pady=5)

    tk.Label(card, text="Password", font=("Helvetica", 12), bg="white").pack(anchor="w")
    password_entry = tk.Entry(card, width=30, font=("Helvetica", 12), show="*")
    password_entry.pack(pady=5)

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()

        result = authenticate(username, password, role="admin")

        if result is None:
            messagebox.showerror("Login Failed", "Invalid login credentials. Contact IT support.")
            return

        if result["role"] != "admin":
            messagebox.showerror("Access Denied", "This account is not an admin account.")
            return

        # window.destroy()
        # print("Admin logged in:", result["user_id"])
        # # TODO: launch_admin_dashboard(result["user_id"])
        
        launch_admin_dashboard(result["username"])

    tk.Button(
        card, text="Sign In", font=("Helvetica", 12, "bold"),
        bg="#9966cc", fg="white", width=20, cursor="hand2",
        relief="flat", command=attempt_login
    ).pack(pady=20)

    tk.Label(window, text="Contact IT support for sign-in issues",
             font=("Helvetica", 10, "italic"), bg="#f4f4f4", fg="#777").pack(pady=20)

    window.mainloop()
