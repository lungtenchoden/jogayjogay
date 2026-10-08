# pages/login.py
import tkinter as tk
from tkinter import messagebox
from theme import *
from backend import sign_in


def build(root, on_success):
    for w in root.winfo_children():
        w.destroy()
    root.configure(bg="#e8eef5")

    card = tk.Frame(root, bg="white", padx=45, pady=40,
                    highlightbackground=BORDER, highlightthickness=1)
    card.place(relx=0.5, rely=0.5, anchor="center")

    box = tk.Frame(card, bg=ACCENT_LIGHT, width=60, height=60)
    box.pack(pady=(0, 15)); box.pack_propagate(False)
    tk.Label(box, text="🚕", bg=ACCENT_LIGHT, fg=NAVY,
             font=("Helvetica", 24)).pack(expand=True)

    tk.Label(card, text="Jogay Jogay", bg="white", fg=NAVY,
             font=("Helvetica", 22, "bold")).pack()
    tk.Label(card, text="Transport Authority Information System",
             bg="white", fg=MUTED, font=FONT_NORMAL).pack(pady=(2, 25))

    tk.Label(card, text="Username", bg="white", fg=TEXT,
             font=("Helvetica", 10, "bold")).pack(anchor="w")
    user = tk.Entry(card, width=32, font=("Helvetica", 11),
                    bd=1, relief="solid")
    user.pack(pady=(4, 14), ipady=7)

    tk.Label(card, text="Password", bg="white", fg=TEXT,
             font=("Helvetica", 10, "bold")).pack(anchor="w")
    pwd = tk.Entry(card, width=32, font=("Helvetica", 11),
                   bd=1, relief="solid", show="●")
    pwd.pack(pady=(4, 20), ipady=7)

    def attempt(_=None):
        ok, msg = sign_in(user.get().strip(), pwd.get().strip())
        if ok:
            on_success()
        else:
            messagebox.showwarning("Login", msg)

    tk.Button(card, text="Log in", bg=ACCENT, fg="white", bd=0,
              activebackground=ACCENT_DARK, activeforeground="white",
              font=("Helvetica", 12, "bold"), cursor="hand2",
              command=attempt).pack(fill="x", ipady=9)

    tk.Label(card, text="Royal Government of Bhutan · Internal use only",
             bg="white", fg=MUTED, font=FONT_SMALL).pack(pady=(22, 0))
    pwd.bind("<Return>", attempt)

    try:
        top = root
        top.attributes("-alpha", 0.0)
        def tick(i=0):
            if i > 10:
                top.attributes("-alpha", 1.0)
                return
            top.attributes("-alpha", i / 10)
            top.after(20, tick, i + 1)
        tick()
    except Exception:
        pass