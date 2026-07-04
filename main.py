import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("AI Gesture Dashboard")
root.geometry("900x550")
root.configure(bg="#0f172a")
root.resizable(False, False)

# ---------------- TITLE ----------------
title = tk.Label(
    root,
    text="AI MULTI-FUNCTION GESTURE SYSTEM",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="#0f172a"
)
title.pack(pady=25)

subtitle = tk.Label(
    root,
    text="Choose Any Module",
    font=("Arial", 13),
    fg="#94a3b8",
    bg="#0f172a"
)
subtitle.pack()

# ---------------- RUN FUNCTION ----------------
def run_file(filename):

    try:
        path = os.path.join(os.getcwd(), filename)

        subprocess.Popen([sys.executable, path])

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )

# ---------------- MAIN FRAME ----------------
main_frame = tk.Frame(root, bg="#0f172a")
main_frame.pack(pady=50)

# ---------------- CARD FUNCTION ----------------
def create_card(parent, title_text, desc_text, filename, color):

    card = tk.Frame(
        parent,
        bg="#1e293b",
        width=220,
        height=260,
        highlightbackground=color,
        highlightthickness=3
    )

    card.pack(side="left", padx=25)
    card.pack_propagate(False)

    title = tk.Label(
        card,
        text=title_text,
        font=("Arial", 18, "bold"),
        fg="white",
        bg="#1e293b"
    )
    title.pack(pady=20)

    desc = tk.Label(
        card,
        text=desc_text,
        font=("Arial", 11),
        fg="#cbd5e1",
        bg="#1e293b",
        wraplength=180,
        justify="center"
    )
    desc.pack(pady=10)

    button = tk.Button(
        card,
        text="OPEN",
        font=("Arial", 13, "bold"),
        bg=color,
        fg="white",
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
        command=lambda: run_file(filename)
    )

    button.pack(side="bottom", pady=25)

# ---------------- CARDS ----------------
create_card(
    main_frame,
    "Cursor Control",
    "Control mouse movement using hand gestures.",
    "cursor.py",
    "#2563eb"
)

create_card(
    main_frame,
    "Advanced Cursor",
    "Perform click, drag and gesture actions.",
    "cursor1.py",
    "#7c3aed"
)

create_card(
    main_frame,
    "Gesture Game",
    "Play games using hand tracking controls.",
    "game.py",
    "#16a34a"
)

# ---------------- START ----------------
root.mainloop()