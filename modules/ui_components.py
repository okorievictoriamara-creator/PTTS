import tkinter as tk
from PIL import Image, ImageTk
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def go_home(current_window):
    current_window.destroy()
    from homepage import launch_homepage
    launch_homepage()

def load_logo():
    img = Image.open(os.path.join(ASSETS_DIR, "ptts_logo.png"))
    img = img.resize((90, 90))
    return ImageTk.PhotoImage(img)

def rounded_card(parent, width=400, height=260, radius=25, bg="white"):
    canvas = tk.Canvas(parent, width=width+20, height=height+20,
                       bg=parent["bg"], highlightthickness=0)
    canvas.pack()

    x1, y1 = 10, 10
    x2, y2 = x1 + width, y1 + height

    # Shadow
    canvas.create_rectangle(x1+5, y1+5, x2+5, y2+5,
                            fill="#d0d0d0", outline="")

    # Rounded corners
    canvas.create_arc(x1, y1, x1+radius*2, y1+radius*2,
                      start=90, extent=90, fill=bg, outline=bg)
    canvas.create_arc(x2-radius*2, y1, x2, y1+radius*2,
                      start=0, extent=90, fill=bg, outline=bg)
    canvas.create_arc(x1, y2-radius*2, x1+radius*2, y2,
                      start=180, extent=90, fill=bg, outline=bg)
    canvas.create_arc(x2-radius*2, y2-radius*2, x2, y2,
                      start=270, extent=90, fill=bg, outline=bg)

    canvas.create_rectangle(x1+radius, y1, x2-radius, y2,
                            fill=bg, outline=bg)
    canvas.create_rectangle(x1, y1+radius, x2, y2-radius,
                            fill=bg, outline=bg)

    frame = tk.Frame(canvas, bg=bg)
    canvas.create_window((width+20)//2, (height+20)//2, window=frame)

    return frame
