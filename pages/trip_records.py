# pages/trip_records.py
import tkinter as tk
from tkinter import messagebox
from theme import *
from widgets import (card, primary_button, secondary_button,
                     data_table, search_bar, Dropdown, scrollable_table)
from backend import get_trip_records, add_trip_record
from dialogs.add_trip_dialog import AddTripDialog
from data import DZONGKHAGS


def build(parent):
    page = tk.Frame(parent, bg=BG, padx=25, pady=22)
    page.pack(fill="both", expand=True)

    c = card(page)
    c.pack(fill="both", expand=True)

    # ---------- header row ----------
    top = tk.Frame(c, bg=CARD)
    top.pack(fill="x")

    left = tk.Frame(top, bg=CARD)
    left.pack(side="left")
    tk.Label(left, text="Trip records", bg=CARD, fg=TEXT,
             font=FONT_HEAD).pack(anchor="w")
    tk.Label(left, text="Review travel activity between Bhutanese dzongkhags.",
             bg=CARD, fg=MUTED, font=FONT_SMALL).pack(anchor="w")

    right = tk.Frame(top, bg=CARD)
    right.pack(side="right")

    primary_button(right, "+ Add record",
                   command=lambda: _open_add(page)).pack(side="left", padx=4)
    secondary_button(right, "Export CSV",
                     command=lambda: messagebox.showinfo("Export",
                                                         "Records exported to CSV.")
                     ).pack(side="left", padx=4)

    # ---------- search + filter ----------
    search_row = tk.Frame(c, bg=CARD)
    search_row.pack(fill="x")

    search_entry = search_bar(search_row, "Search by dzongkhag or date")

    filter_dd = Dropdown(search_row, ["All dzongkhags"] + DZONGKHAGS,
                         default="All dzongkhags", width=20)
    filter_dd.pack(side="right", padx=(10, 0))

    # ---------- table (scrollable) ----------
    table_holder = scrollable_table(c)

    def refresh(*_):
        for w in table_holder.winfo_children():
            w.destroy()

        rows = get_trip_records()

        dz = filter_dd.get()
        if dz != "All dzongkhags":
            rows = [r for r in rows if r[0] == dz or r[1] == dz]

        q = search_entry.get().strip().lower()
        if q and q != search_entry._placeholder.lower():
            rows = [r for r in rows
                    if q in r[0].lower() or q in r[1].lower() or q in r[2].lower()]

        cols = ("Origin Dzongkhag", "Destination Dzongkhag",
                "Trip Date", "Number of Trips")
        widths = [200, 220, 180, 140]

        if not rows:
            tk.Label(table_holder, text="No records match your filters.",
                     bg=CARD, fg=MUTED, font=FONT_NORMAL).pack(pady=40)
        else:
            data_table(table_holder, cols, widths, rows, status_col=None)

    filter_dd.on_change = lambda _val: refresh()
    search_entry.bind("<KeyRelease>", refresh)

    def _open_add(parent_page):
        def on_save(record):
            add_trip_record(record)
            messagebox.showinfo("Saved", "Trip record was added.")
            refresh()

        AddTripDialog(parent_page.winfo_toplevel(), on_save=on_save)

    refresh()