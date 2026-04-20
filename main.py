import tkinter as tk
import os


# from modules.gui import MISGUI

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = MISGUI(root)
#     root.mainloop()

from homepage import launch_homepage

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("assets/blank.ico")
    root.withdraw()  # Hide the root window
    launch_homepage()
    root
