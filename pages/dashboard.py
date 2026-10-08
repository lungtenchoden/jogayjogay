# pages/dashboard.py
import tkinter as tk
from theme import *
from widgets import card, stat_card, bar_row, scrollable_page
from data import REGISTRATION_BARS


def build(parent):
    inner = scrollable_page(parent)
    page = tk.Frame(inner, bg=BG, padx=25, pady=22)
    page.pack(fill="both", expand=True)

    row = tk.Frame(page, bg=BG); row.pack(fill="x")
    stat_card(row, "TOTAL REGISTERED TAXIS", "248", "↑ 6.2% from last month", ACCENT)
    stat_card(row, "TOTAL TRIPS RECORDED",   "1,540", "↑ 11.8% from last month", ACCENT)
    stat_card(row, "MOST ACTIVE DZONGKHAG",  "Thimphu", "82 active taxis", GOLD, big=False)

    mid = tk.Frame(page, bg=BG); mid.pack(fill="x", pady=(18, 0))

    chart = card(mid); chart.pack(side="left", fill="both", expand=True, padx=(0, 10))
    tk.Label(chart, text="Registered taxis by dzongkhag", bg=CARD, fg=TEXT,
             font=FONT_HEAD).pack(anchor="w")
    tk.Label(chart, text="Current registration records", bg=CARD, fg=MUTED,
             font=FONT_SMALL).pack(anchor="w", pady=(0, 16))
    for name, val in REGISTRATION_BARS:
        bar_row(chart, name, val, max_value=80, bar_width=380)
    tk.Label(chart, text="Source: Taxi registration database · Updated monthly",
             bg=CARD, fg=MUTED, font=FONT_SMALL).pack(anchor="w", pady=(18, 0))

    news = card(mid); news.pack(side="left", fill="both", padx=(10, 0))
    news.configure(width=380); news.pack_propagate(False)

    img = tk.Frame(news, bg="#2c3e50", height=130)
    img.pack(fill="x"); img.pack_propagate(False)
    tk.Label(img, text="🚕  TAKSI  🚕", bg="#2c3e50", fg=GOLD,
             font=("Helvetica", 20, "bold")).pack(expand=True)

    tk.Label(news, text="FIELD UPDATE", bg=CARD, fg=MUTED,
             font=FONT_TINY).pack(anchor="w", pady=(14, 4))
    tk.Label(news, text="Parking zones reporting steady activity",
             bg=CARD, fg=TEXT, font=FONT_HEAD, wraplength=320,
             justify="left").pack(anchor="w")
    tk.Label(news, text="Thimphu and Paro parking zones have reported complete "
                        "daily submissions for the past 14 days.",
             bg=CARD, fg=MUTED, font=FONT_SMALL, wraplength=320,
             justify="left").pack(anchor="w", pady=(8, 12))
    tk.Label(news, text="View parking zones", bg=CARD, fg=ACCENT,
             font=("Helvetica", 9, "underline"),
             cursor="hand2").pack(anchor="w")

    ins = card(page); ins.pack(fill="x", pady=(18, 0))
    tk.Label(ins, text="SYSTEM INSIGHTS", bg=CARD, fg=TEXT,
             font=FONT_TINY).pack(anchor="w")
    for line in ["Thimphu has the highest number of registered taxis this month.",
                 "Phuentsholing to Thimphu is the most frequent travel route."]:
        r = tk.Frame(ins, bg=CARD); r.pack(anchor="w", fill="x", pady=3)
        tk.Frame(r, bg=GOLD, width=4, height=16).pack(side="left", padx=(0, 10))
        tk.Label(r, text=line, bg=CARD, fg=TEXT, font=FONT_NORMAL).pack(side="left")