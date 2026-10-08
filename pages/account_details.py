# pages/account_details.py
import tkinter as tk
from theme import *
from widgets import card, scrollable_page


def build(parent):
    inner = scrollable_page(parent)
    page = tk.Frame(inner, bg=BG, padx=25, pady=22)
    page.pack(fill="both", expand=True)

    title_card = card(page, padx=28, pady=24)
    title_card.pack(fill="x")
    tk.Label(title_card, text="Account details", bg=CARD, fg=TEXT,
             font=("Helvetica", 18, "bold")).pack(anchor="w")
    tk.Label(title_card, text="Your profile and account information.",
             bg=CARD, fg=MUTED, font=FONT_SMALL).pack(anchor="w", pady=(4, 0))

    prof = card(page, padx=28, pady=24)
    prof.pack(fill="x", pady=(18, 0))

    head = tk.Frame(prof, bg=CARD)
    head.pack(fill="x")

    av = tk.Frame(head, bg=ACCENT_LIGHT, width=100, height=100)
    av.pack(side="left")
    av.pack_propagate(False)
    tk.Label(av, text="TS", bg=ACCENT_LIGHT, fg=NAVY,
             font=("Helvetica", 32, "bold")).pack(expand=True)

    info = tk.Frame(head, bg=CARD)
    info.pack(side="left", padx=24, anchor="n")
    tk.Label(info, text="USER", bg=CARD, fg=MUTED,
             font=FONT_TINY).pack(anchor="w")
    tk.Label(info, text="Tashi Sherpa", bg=CARD, fg=NAVY,
             font=("Helvetica", 22, "bold")).pack(anchor="w", pady=(2, 6))
    tk.Label(info, text="Administrator · Bhutan Transport Authority",
             bg=CARD, fg=MUTED, font=FONT_NORMAL).pack(anchor="w")

    badge = tk.Frame(info, bg="#d4ecd8")
    badge.pack(anchor="w", pady=(10, 0))
    tk.Label(badge, text="●  Active", bg="#d4ecd8", fg=GREEN,
             font=("Helvetica", 9, "bold"), padx=10, pady=3).pack()

    details = card(page, padx=28, pady=24)
    details.pack(fill="x", pady=(18, 0))
    tk.Label(details, text="PROFILE INFORMATION", bg=CARD, fg=MUTED,
             font=FONT_TINY).pack(anchor="w", pady=(0, 14))

    rows = [
        ("Full name",    "Tashi Sherpa"),
        ("Username",     "tashi.sherpa"),
        ("Email",        "tashi.sherpa@rsta.gov.bt"),
        ("Phone",        "+975 17 12 34 56"),
        ("Role",         "Administrator"),
        ("Department",   "Bhutan Transport Authority"),
        ("Dzongkhag",    "Thimphu"),
        ("Member since", "12 January 2022"),
        ("Last login",   "Thursday, 21 March 2024 · 08:42 AM"),
    ]
    for label, value in rows:
        _detail_row(details, label, value)

    actions = card(page, padx=28, pady=24)
    actions.pack(fill="x", pady=(18, 0))
    tk.Label(actions, text="ACCOUNT ACTIONS", bg=CARD, fg=MUTED,
             font=FONT_TINY).pack(anchor="w", pady=(0, 14))

    btn_row = tk.Frame(actions, bg=CARD)
    btn_row.pack(anchor="w")
    tk.Button(btn_row, text="Change password", bg=ACCENT, fg="white", bd=0,
              activebackground=ACCENT_DARK, activeforeground="white",
              font=("Helvetica", 10, "bold"), padx=18, pady=8,
              cursor="hand2",
              command=lambda: _show_placeholder("Change password")).pack(side="left", padx=(0, 8))
    tk.Button(btn_row, text="Edit profile", bg="white", fg=TEXT, bd=1,
              relief="solid", font=FONT_NORMAL, padx=18, pady=8,
              cursor="hand2",
              command=lambda: _show_placeholder("Edit profile")).pack(side="left", padx=(0, 8))
    tk.Button(btn_row, text="Download my data", bg="white", fg=TEXT, bd=1,
              relief="solid", font=FONT_NORMAL, padx=18, pady=8,
              cursor="hand2",
              command=lambda: _show_placeholder("Download data")).pack(side="left")


def _detail_row(parent, label, value):
    row = tk.Frame(parent, bg=CARD)
    row.pack(fill="x", pady=6)
    tk.Label(row, text=label, bg=CARD, fg=MUTED,
             font=FONT_NORMAL, width=18, anchor="w").pack(side="left")
    tk.Label(row, text=value, bg=CARD, fg=TEXT,
             font=FONT_BOLD, anchor="w").pack(side="left")
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x")


def _show_placeholder(name):
    from tkinter import messagebox
    messagebox.showinfo(name, f"{name} would open here.")