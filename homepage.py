import tkinter as tk
from PIL import Image, ImageTk
import os

from modules.student import launch_student
from modules.tutor import launch_tutor
from modules.parent import launch_parent
from modules.admin import launch_admin

# --- Base directory for assets ---
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")



# --- Function to load and resize images ---
def load_icon(filename):
    path = os.path.join(ASSETS_DIR, filename)
    img = Image.open(path)
    img = img.resize((80, 80), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)


# --- Main window setup ---
def launch_homepage():
    root = tk.Toplevel()
    root.iconbitmap("assets/blank.ico")
    root.title("PTTS App - Home")
    root.geometry("1200x600")
    root.configure(bg="#f4f4f4")

    # --- Helper functions to open pages ---
    def open_student():
        root.destroy()
        launch_student()

    def open_tutor():
        root.destroy()
        launch_tutor()

    def open_parent():
        root.destroy()
        launch_parent()

    def open_admin():
        root.destroy()
        launch_admin()

    # --- Title ---
    title_label = tk.Label(
        root,
        text="Hello and Welcome to the PTTS App",
        font=("Helvetica", 28, "bold"),
        bg="#f4f4f4"
    )
    title_label.pack(pady=40)

    # --- Subheading ---
    subheading_label = tk.Label(
        root,
        text="Please select a category",
        font=("Helvetica", 16),
        bg="#f4f4f4",
        fg="#555"
    )
    subheading_label.pack(pady=(0, 20))

    # --- Frame for cards ---
    card_frame = tk.Frame(root, bg="#f4f4f4")
    card_frame.pack(pady=20)

    # --- Load images ---
    student_img = load_icon("student.png")
    tutor_img = load_icon("tutor.png")
    parent_img = load_icon("guardian.png")
    admin_img = load_icon("admin.png")

    # --- Helper function to create cards ---
    def create_card(parent, title, color, image, command):
        canvas_width = 220
        canvas_height = 280

        canvas = tk.Canvas(
            parent,
            width=canvas_width,
            height=canvas_height,
            bg="#f4f4f4",
            highlightthickness=0
        )
        canvas.pack(side="left", padx=25)

        card_width = 180
        card_height = 240
        radius = 20

        x_offset = (canvas_width - card_width) // 2
        y_offset = (canvas_height - card_height) // 2

        # Shadow
        canvas.create_rectangle(
            x_offset + 8, y_offset + 8,
            x_offset + card_width + 8, y_offset + card_height + 8,
            fill="#d0d0d0", outline=""
        )

        # Rounded rectangle
        x1, y1 = x_offset, y_offset
        x2, y2 = x_offset + card_width, y_offset + card_height

        canvas.create_arc(x1, y1, x1+radius*2, y1+radius*2,
                          start=90, extent=90, fill=color, outline=color)
        canvas.create_arc(x2-radius*2, y1, x2, y1+radius*2,
                          start=0, extent=90, fill=color, outline=color)
        canvas.create_arc(x1, y2-radius*2, x1+radius*2, y2,
                          start=180, extent=90, fill=color, outline=color)
        canvas.create_arc(x2-radius*2, y2-radius*2, x2, y2,
                          start=270, extent=90, fill=color, outline=color)

        canvas.create_rectangle(x1+radius, y1, x2-radius, y2,
                                fill=color, outline=color)
        canvas.create_rectangle(x1, y1+radius, x2, y2-radius,
                                fill=color, outline=color)

        # Icon
        canvas.create_image((x1+x2)//2, y1 + 70, image=image)

        # Title
        canvas.create_text(
            (x1+x2)//2, y1 + 140,
            text=title,
            fill="white",
            font=("Helvetica", 14, "bold")
        )

        # Button
        btn = tk.Button(
            parent,
            text="Open",
            command=command,
            bg="white",
            fg=color,
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2"
        )
        canvas.create_window((x1+x2)//2, y1 + 190, window=btn)

    # --- Create cards ---
    create_card(card_frame, "Student", "#4da6ff", student_img, open_student)
    create_card(card_frame, "Tutor", "#ff9933", tutor_img, open_tutor)
    create_card(card_frame, "Parent", "#33cc33", parent_img, open_parent)
    create_card(card_frame, "Admin", "#9966cc", admin_img, open_admin)

    # --- Footer ---
    footer_label = tk.Label(
        root,
        text="The Personal Tutor Tracker",
        font=("Helvetica", 12, "italic"),
        bg="#f4f4f4",
        fg="#777"
    )
    footer_label.pack(side="bottom", pady=20)

    root.mainloop()
