# pages/analysis.py
import tkinter as tk
from theme import *
from widgets import card, stat_card, data_table, scrollable_page
from backend import get_analysis_data


def build(parent):
    inner = scrollable_page(parent)
    page = tk.Frame(inner, bg=BG, padx=25, pady=22)
    page.pack(fill="both", expand=True)

    row = tk.Frame(page, bg=BG); row.pack(fill="x")
    stat_card(row, "COMMON DESTINATION",     "Thimphu",  "412 recorded trips",  ACCENT, big=False)
    stat_card(row, "LEAST COMMON",           "Bumthang", "18 recorded trips",   ACCENT, big=False)
    stat_card(row, "HIGHEST TAXI DZONGKHAG", "Thimphu",  "82 registered taxis", ACCENT, big=False)
    stat_card(row, "LOWEST TAXI DZONGKHAG",  "Bumthang", "7 registered taxis",  GOLD,   big=False)

    c = card(page); c.pack(fill="both", expand=True, pady=(18, 0))
    tk.Label(c, text="Dzongkhag summary", bg=CARD, fg=TEXT,
             font=FONT_HEAD).pack(anchor="w")
    tk.Label(c, text="A consolidated view of taxi registrations and recorded travel activity.",
             bg=CARD, fg=MUTED, font=FONT_SMALL).pack(anchor="w", pady=(0, 10))

    cols = ("Dzongkhag", "Registered Taxis", "Trips Out",
            "Trips In", "Activity Level")
    widths = [180, 140, 110, 110, 130]
    data_table(c, cols, widths, get_analysis_data(), status_col=4)