# pages/system_preferences.py
import tkinter as tk
from tkinter import messagebox
from theme import *
from widgets import card, scrollable_page, Dropdown


PREFS = {
    "theme":               "Light",
    "language":            "English",
    "date_format":         "DD/MM/YYYY",
    "rows_per_page":       "25",
    "email_notifications": True,
    "push_notifications":  True,
    "weekly_reports":      False,
    "auto_refresh":        True,
    "compact_mode":        False,
}


def build(parent):
    inner = scrollable_page(parent)
    page = tk.Frame(inner, bg=BG, padx=25, pady=22)
    page.pack(fill="both", expand=True)

    title_card = card(page, padx=28, pady=24)
    title_card.pack(fill="x")
    tk.Label(title_card, text="System preferences", bg=CARD, fg=TEXT,
             font=("Helvetica", 18, "bold")).pack(anchor="w")
    tk.Label(title_card, text="Customize how Jogay Jogay looks and behaves.",
             bg=CARD, fg=MUTED, font=FONT_SMALL).pack(anchor="w", pady=(4, 0))

    appearance = card(page, padx=28, pady=24)
    appearance.pack(fill="x", pady=(18, 0))
    tk.Label(appearance, text="APPEARANCE", bg=CARD, fg=MUTED,
             font=FONT_TINY).pack(anchor="w", pady=(0, 14))

    _dropdown_row(appearance, "Theme", ["Light", "Dark", "System"], "theme")
    _dropdown_row(appearance, "Language", ["English", "Dzongkha"], "language")
    _toggle_row(appearance, "Compact mode",
                "Show more rows by reducing padding.", "compact_mode")

    display = card(page, padx=28, pady=24)
    display.pack(fill="x", pady=(18, 0))
    tk.Label(display, text="DISPLAY", bg=CARD, fg=MUTED,
             font=FONT_TINY).pack(anchor="w", pady=(0, 14))

    _dropdown_row(display, "Date format",
                  ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"], "date_format")
    _dropdown_row(display, "Rows per page", ["10", "25", "50", "100"],
                  "rows_per_page")
    _toggle_row(display, "Auto-refresh data",
                "Pull latest records every 5 minutes.", "auto_refresh")

    notifications = card(page, padx=28, pady=24)
    notifications.pack(fill="x", pady=(18, 0))
    tk.Label(notifications, text="NOTIFICATIONS", bg=CARD, fg=MUTED,
             font=FONT_TINY).pack(anchor="w", pady=(0, 14))

    _toggle_row(notifications, "Email notifications",
                "Receive email alerts for system events.", "email_notifications")
    _toggle_row(notifications, "Push notifications",
                "Get in-app alerts for new records.", "push_notifications")
    _toggle_row(notifications, "Weekly reports",
                "Receive a summary every Monday morning.", "weekly_reports")

    actions = card(page, padx=28, pady=24)
    actions.pack(fill="x", pady=(18, 0))

    row = tk.Frame(actions, bg=CARD)
    row.pack(anchor="w")
    tk.Button(row, text="Save preferences", bg=ACCENT, fg="white", bd=0,
              activebackground=ACCENT_DARK, activeforeground="white",
              font=("Helvetica", 10, "bold"), padx=20, pady=9,
              cursor="hand2", command=_save).pack(side="left", padx=(0, 8))
    tk.Button(row, text="Reset to defaults", bg="white", fg=TEXT, bd=1,
              relief="solid", font=FONT_NORMAL, padx=20, pady=9,
              cursor="hand2", command=_reset).pack(side="left")


def _dropdown_row(parent, label, options, key):
    row = tk.Frame(parent, bg=CARD)
    row.pack(fill="x", pady=8)

    left = tk.Frame(row, bg=CARD)
    left.pack(side="left")
    tk.Label(left, text=label, bg=CARD, fg=TEXT,
             font=FONT_BOLD).pack(anchor="w")
    tk.Label(left, text="Choose from the list.", bg=CARD, fg=MUTED,
             font=FONT_SMALL).pack(anchor="w", pady=(2, 0))

    dd = Dropdown(row, options, default=PREFS[key], width=18,
                  on_change=lambda val, k=key: PREFS.update({k: val}))
    dd.pack(side="right")


def _toggle_row(parent, label, description, key):
    row = tk.Frame(parent, bg=CARD)
    row.pack(fill="x", pady=8)

    left = tk.Frame(row, bg=CARD)
    left.pack(side="left")
    tk.Label(left, text=label, bg=CARD, fg=TEXT,
             font=FONT_BOLD).pack(anchor="w")
    tk.Label(left, text=description, bg=CARD, fg=MUTED,
             font=FONT_SMALL).pack(anchor="w", pady=(2, 0))

    _ToggleSwitch(row, initial=PREFS[key],
                  on_change=lambda val, k=key: PREFS.update({k: val})).pack(side="right")


class _ToggleSwitch(tk.Frame):
    def __init__(self, parent, initial=False, on_change=None):
        super().__init__(parent, bg=CARD)
        self.state = bool(initial)
        self.on_change = on_change
        self.width, self.height = 48, 26

        self.canvas = tk.Canvas(self, width=self.width, height=self.height,
                                bg=CARD, highlightthickness=0, cursor="hand2")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._click)
        self._draw()

    def _draw(self):
        self.canvas.delete("all")
        track_color = ACCENT if self.state else "#cbd5e0"
        self.canvas.create_oval(1, 1, self.height - 1, self.height - 1,
                                fill=track_color, outline=track_color)
        self.canvas.create_oval(self.width - self.height + 1, 1,
                                self.width - 1, self.height - 1,
                                fill=track_color, outline=track_color)
        self.canvas.create_rectangle(self.height // 2, 1,
                                     self.width - self.height // 2,
                                     self.height - 1,
                                     fill=track_color, outline=track_color)
        knob_x = self.width - self.height // 2 if self.state else self.height // 2
        self.canvas.create_oval(knob_x - 10, 3, knob_x + 10, self.height - 3,
                                fill="white", outline="white")

    def _click(self, _):
        self.state = not self.state
        self._draw()
        if self.on_change:
            self.on_change(self.state)

    def get(self):
        return self.state


def _save():
    summary = "\n".join(f"• {k}: {v}" for k, v in PREFS.items())
    messagebox.showinfo("Preferences saved",
                        f"Your preferences have been saved:\n\n{summary}")


def _reset():
    defaults = {
        "theme":               "Light",
        "language":            "English",
        "date_format":         "DD/MM/YYYY",
        "rows_per_page":       "25",
        "email_notifications": True,
        "push_notifications":  True,
        "weekly_reports":      False,
        "auto_refresh":        True,
        "compact_mode":        False,
    }
    PREFS.update(defaults)
    messagebox.showinfo("Reset", "Preferences reset to defaults. "
                                 "Reopen the page to see the changes.")