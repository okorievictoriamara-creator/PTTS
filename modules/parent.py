import tkinter as tk
from ui_components import go_home, load_logo, rounded_card

def launch_parent():
    window = tk.Tk()
    window.title("PTTS - Parent Sign In")
    window.geometry("900x600")
    window.configure(bg="#f4f4f4")

    tk.Button(window, text="← Back to Home", font=("Helvetica", 11, "bold"),
              bg="#f4f4f4", fg="#007acc", bd=0, cursor="hand2",
              command=lambda: go_home(window)).pack(anchor="w", padx=20, pady=10)

    logo = load_logo()
    tk.Label(window, image=logo, bg="#f4f4f4").pack(pady=10)
    window.logo = logo

    tk.Label(window, text="Parent Sign In", font=("Helvetica", 28, "bold"),
             bg="#f4f4f4").pack(pady=10)

    card = rounded_card(window)

    tk.Label(card, text="Username", font=("Helvetica", 12), bg="white").pack(anchor="w")
    tk.Entry(card, width=30, font=("Helvetica", 12)).pack(pady=5)

    tk.Label(card, text="Password", font=("Helvetica", 12), bg="white").pack(anchor="w")
    tk.Entry(card, width=30, font=("Helvetica", 12), show="*").pack(pady=5)

    tk.Button(card, text="Sign In", font=("Helvetica", 12, "bold"),
              bg="#33cc33", fg="white", width=20, cursor="hand2",
              relief="flat").pack(pady=20)

    tk.Label(window, text="Contact IT support for sign-in issues",
             font=("Helvetica", 10, "italic"), bg="#f4f4f4", fg="#777").pack(pady=20)

    window.mainloop()
