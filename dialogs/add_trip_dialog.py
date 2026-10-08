# dialogs/add_trip_dialog.py
import tkinter as tk
from tkinter import messagebox
from datetime import date, datetime

from theme import *
from widgets import Dropdown
from data import DZONGKHAGS


class AddTripDialog(tk.Toplevel):
    def __init__(self, parent, on_save):
        super().__init__(parent)
        self.on_save = on_save

        self.title("Add Trip Record")
        self.geometry("620x640")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # -------- header --------
        header = tk.Frame(self, bg=NAVY, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Add Trip Record", bg=NAVY, fg="white",
                 font=("Helvetica", 16, "bold")).pack(side="left", padx=24)
        tk.Label(header, text="Record a trip between two dzongkhags",
                 bg=NAVY, fg="#8fa7c2",
                 font=FONT_SMALL).pack(side="left", padx=4, pady=(6, 0))

        # -------- scrollable body --------
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        sb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        sb.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=sb.set)

        body = tk.Frame(canvas, bg=CARD, padx=30, pady=24,
                        highlightbackground=BORDER, highlightthickness=1)
        window_id = canvas.create_window((0, 0), window=body, anchor="nw")

        def _on_body_conf(_):
            canvas.configure(scrollregion=canvas.bbox("all"))
        body.bind("<Configure>", _on_body_conf)

        def _on_canvas_conf(event):
            canvas.itemconfigure(window_id, width=event.width)
        canvas.bind("<Configure>", _on_canvas_conf)

        def _wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _wheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # -------- section: route --------
        _section_title(body, "ROUTE")

        self.origin = _dropdown_field(
            body, "Origin Dzongkhag *",
            options=DZONGKHAGS, default="Thimphu",
            helper="Where the trip started")

        self.destination = _dropdown_field(
            body, "Destination Dzongkhag *",
            options=DZONGKHAGS, default="Paro",
            helper="Where the trip ended")

        # -------- section: details --------
        _section_title(body, "TRIP DETAILS")

        self.date_entry = _text_field(
            body, "Trip Date *",
            placeholder="YYYY-MM-DD",
            helper="Date the trip took place")
        self.date_entry.insert(0, str(date.today()))

        self.num = _text_field(
            body, "Number of Trips *",
            placeholder="e.g. 12",
            helper="How many trips were recorded on this route")

        # -------- footer buttons --------
        footer = tk.Frame(self, bg=CARD, padx=24, pady=18,
                          highlightbackground=BORDER, highlightthickness=1)
        footer.pack(fill="x", side="bottom")

        tk.Button(footer, text="Cancel", bg="white", fg=TEXT, bd=1,
                  relief="solid", font=FONT_NORMAL, padx=24, pady=10,
                  cursor="hand2",
                  command=self.destroy).pack(side="right", padx=(8, 0))

        tk.Button(footer, text="Save Record", bg=ACCENT, fg="white", bd=0,
                  activebackground=ACCENT_DARK, activeforeground="white",
                  font=("Helvetica", 11, "bold"), padx=28, pady=10,
                  cursor="hand2",
                  command=self._save).pack(side="right")

        self.origin.label.focus_set() if hasattr(self.origin, "label") else None

    def _save(self):
        origin = self.origin.get()
        destination = self.destination.get()
        trip_date = self.date_entry.get().strip()
        num_trips = self.num.get().strip()

        if origin == destination:
            messagebox.showwarning("Invalid",
                                   "Origin and destination can't be the same.")
            return

        if not trip_date:
            messagebox.showwarning("Missing info",
                                   "Please enter a trip date.")
            self.date_entry.focus_set()
            return

        try:
            datetime.strptime(trip_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Invalid date",
                                   "Trip date must be in YYYY-MM-DD format.")
            self.date_entry.focus_set()
            return

        if not num_trips.isdigit() or int(num_trips) <= 0:
            messagebox.showwarning("Invalid",
                                   "Number of trips must be a positive number.")
            self.num.focus_set()
            return

        record = (origin, destination, trip_date, num_trips)
        self.on_save(record)
        self.destroy()


# =========================================================
#  helpers
# =========================================================
def _section_title(parent, text):
    row = tk.Frame(parent, bg=CARD)
    row.pack(fill="x", pady=(18, 8))
    tk.Label(row, text=text, bg=CARD, fg=MUTED,
             font=FONT_TINY).pack(side="left")
    tk.Frame(row, bg=BORDER, height=1).pack(side="left", fill="x",
                                              expand=True, padx=(10, 0))


def _text_field(parent, label, placeholder="", helper=""):
    tk.Label(parent, text=label, bg=CARD, fg=TEXT,
             font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(4, 2))
    if helper:
        tk.Label(parent, text=helper, bg=CARD, fg=MUTED,
                 font=FONT_SMALL).pack(anchor="w", pady=(0, 4))

    entry = tk.Entry(parent, font=("Helvetica", 11), bd=1, relief="solid")
    entry.pack(fill="x", ipady=8)

    if placeholder and not helper:
        entry.insert(0, placeholder)
        entry.configure(fg="#b0bcc9")

        def on_in(_):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.configure(fg=TEXT)

        def on_out(_):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.configure(fg="#b0bcc9")

        entry.bind("<FocusIn>", on_in)
        entry.bind("<FocusOut>", on_out)

    return entry


def _dropdown_field(parent, label, options, default, helper=""):
    tk.Label(parent, text=label, bg=CARD, fg=TEXT,
             font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(4, 2))
    if helper:
        tk.Label(parent, text=helper, bg=CARD, fg=MUTED,
                 font=FONT_SMALL).pack(anchor="w", pady=(0, 4))

    dd = Dropdown(parent, options, default=default, width=48)
    dd.pack(fill="x", pady=(0, 4))
    return dd