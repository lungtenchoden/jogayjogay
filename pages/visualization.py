# pages/visualization.py
import tkinter as tk
from theme import *
from widgets import card
from data import REGISTRATION_BARS, MONTHLY_TRIPS, FLEET_SHARE


# =========================================================
#  PAGE BUILDER
# =========================================================
def build(parent):
    page = tk.Frame(parent, bg=BG, padx=25, pady=22)
    page.pack(fill="both", expand=True)

    # ---- Top row: bar chart + donut ----
    top = tk.Frame(page, bg=BG)
    top.pack(fill="x")

    # LEFT — Taxi registrations
    left = card(top)
    left.pack(side="left", fill="both", expand=True, padx=(0, 10))
    tk.Label(left, text="Taxi registrations", bg=CARD, fg=TEXT,
             font=FONT_HEAD).pack(anchor="w")
    tk.Label(left, text="Current registration records by dzongkhag",
             bg=CARD, fg=MUTED, font=FONT_SMALL).pack(anchor="w", pady=(0, 12))

    _draw_horizontal_bars(left, REGISTRATION_BARS,
                          width=520, height=260,
                          x_label="Registered taxis")

    tk.Label(left, text="Source: Taxi registration database · Updated monthly",
             bg=CARD, fg=MUTED, font=FONT_SMALL).pack(anchor="w", pady=(10, 0))

    # RIGHT — Fleet share donut
    right = card(top)
    right.pack(side="left", fill="both", padx=(10, 0))
    right.configure(width=420)
    right.pack_propagate(False)
    tk.Label(right, text="Fleet share by vehicle type", bg=CARD, fg=TEXT,
             font=FONT_HEAD).pack(anchor="w")
    tk.Label(right, text="Distribution across the fleet", bg=CARD, fg=MUTED,
             font=FONT_SMALL).pack(anchor="w", pady=(0, 12))

    _draw_donut_chart(right, FLEET_SHARE, size=240)

    # ---- Bottom: Trips by month ----
    bottom = card(page)
    bottom.pack(fill="both", expand=True, pady=(18, 0))
    tk.Label(bottom, text="Trips recorded by month", bg=CARD, fg=TEXT,
             font=FONT_HEAD).pack(anchor="w")
    tk.Label(bottom, text="Total trips per month (Oct 2023 – Mar 2024)",
             bg=CARD, fg=MUTED, font=FONT_SMALL).pack(anchor="w", pady=(0, 12))

    _draw_vertical_bars(bottom, MONTHLY_TRIPS,
                        height=280,
                        y_label="Trips")


# =========================================================
#  HORIZONTAL BAR CHART  (registrations by dzongkhag)
# =========================================================
def _draw_horizontal_bars(parent, data, width=520, height=260,
                          x_label="Count"):
    cv = tk.Canvas(parent, width=width, height=height,
                   bg=CARD, highlightthickness=0)
    cv.pack(anchor="w")

    pad_left = 140
    pad_right = 60
    pad_top = 20
    pad_bottom = 40
    plot_w = width - pad_left - pad_right
    plot_h = height - pad_top - pad_bottom

    max_val = _nice_max(max(v for _, v in data))
    n = len(data)
    bar_gap = 10
    bar_h = (plot_h - (n - 1) * bar_gap) / n

    ticks = 5
    for i in range(ticks + 1):
        x = pad_left + (plot_w * i / ticks)
        cv.create_line(x, pad_top, x, pad_top + plot_h,
                       fill="#eef2f7")
        val = int(max_val * i / ticks)
        cv.create_text(x, pad_top + plot_h + 12,
                       text=str(val), fill=MUTED,
                       font=("Helvetica", 8))

    for i, (label, val) in enumerate(data):
        y0 = pad_top + i * (bar_h + bar_gap)
        y1 = y0 + bar_h
        bar_w = plot_w * val / max_val

        cv.create_rectangle(pad_left, y0, pad_left + plot_w, y1,
                            fill="#f2f5f9", outline="")
        cv.create_rectangle(pad_left, y0, pad_left + bar_w, y1,
                            fill=ACCENT, outline="")
        cv.create_text(pad_left - 10, (y0 + y1) / 2,
                       text=label, anchor="e",
                       fill=TEXT, font=("Helvetica", 9))
        cv.create_text(pad_left + bar_w + 8, (y0 + y1) / 2,
                       text=str(val), anchor="w",
                       fill=TEXT, font=("Helvetica", 9, "bold"))

    cv.create_text(width - 15, height - 8, text=x_label,
                   anchor="e", fill=MUTED, font=("Helvetica", 8))
    cv.create_text(6, 8, text="Dzongkhag", anchor="nw",
                   fill=MUTED, font=("Helvetica", 8))


# =========================================================
#  VERTICAL BAR CHART  (trips per month) — responsive
# =========================================================
def _draw_vertical_bars(parent, data, height=280, y_label="Count"):
    wrapper = tk.Frame(parent, bg=CARD)
    wrapper.pack(fill="x", expand=True, pady=(4, 0))

    cv = tk.Canvas(wrapper, height=height, bg=CARD,
                   highlightthickness=0)
    cv.pack(fill="x", expand=True)

    def redraw(event=None):
        cv.delete("all")

        w = cv.winfo_width()
        h = cv.winfo_height()
        if w < 50 or h < 50:
            return

        pad_left   = 55
        pad_right  = 25
        pad_top    = 30
        pad_bottom = 45

        plot_w = w - pad_left - pad_right
        plot_h = h - pad_top - pad_bottom

        max_val = _nice_max(max(v for _, v in data))

        ticks = 5
        for i in range(ticks + 1):
            y = pad_top + plot_h - (plot_h * i / ticks)
            cv.create_line(pad_left, y, pad_left + plot_w, y,
                           fill="#eef2f7")
            cv.create_text(pad_left - 10, y,
                           text=str(int(max_val * i / ticks)),
                           anchor="e", fill=MUTED,
                           font=("Helvetica", 8))

        n = len(data)
        gap = 24
        slot_w = (plot_w - gap * (n - 1)) / n
        bar_w = min(slot_w, 90)

        max_in_data = max(v for _, v in data)
        best_index = [v for _, v in data].index(max_in_data)

        for i, (label, val) in enumerate(data):
            cx = pad_left + i * (slot_w + gap) + slot_w / 2
            x0 = cx - bar_w / 2
            x1 = cx + bar_w / 2

            bar_h = plot_h * val / max_val
            y0 = pad_top + plot_h - bar_h
            y1 = pad_top + plot_h

            color = GOLD if i == best_index else ACCENT

            cv.create_rectangle(x0, y0, x1, y1,
                                fill=color, outline="")
            cv.create_line(x0, y0, x1, y0,
                           fill="#ffffff", width=1)
            cv.create_text(cx, y0 - 12, text=str(val),
                           fill=TEXT,
                           font=("Helvetica", 10, "bold"))
            cv.create_text(cx, y1 + 16, text=label,
                           fill=MUTED,
                           font=("Helvetica", 10))

        cv.create_line(pad_left, pad_top + plot_h,
                       pad_left + plot_w, pad_top + plot_h,
                       fill=BORDER)

        cv.create_text(10, 10, text=y_label, anchor="nw",
                       fill=MUTED, font=("Helvetica", 8))

    cv.bind("<Configure>", redraw)
    cv.after(50, redraw)


# =========================================================
#  DONUT CHART  (fleet share)
# =========================================================
def _draw_donut_chart(parent, segments, size=240):
    wrapper = tk.Frame(parent, bg=CARD)
    wrapper.pack(anchor="w", pady=(4, 0))

    cv = tk.Canvas(wrapper, width=size + 20, height=size + 20,
                   bg=CARD, highlightthickness=0)
    cv.pack(side="left")

    x0 = 10
    y0 = 10
    x1 = x0 + size
    y1 = y0 + size

    start = 90
    for _, pct, color in segments:
        extent = -pct * 3.6
        cv.create_arc(x0, y0, x1, y1, start=start, extent=extent,
                      fill=color, outline=CARD, width=2)
        start += extent

    hole = size * 0.55
    hx0 = x0 + (size - hole) / 2
    hy0 = y0 + (size - hole) / 2
    cv.create_oval(hx0, hy0, hx0 + hole, hy0 + hole,
                   fill=CARD, outline=CARD)

    cv.create_text(x0 + size / 2, y0 + size / 2 - 8,
                   text="100%", fill=NAVY,
                   font=("Helvetica", 16, "bold"))
    cv.create_text(x0 + size / 2, y0 + size / 2 + 12,
                   text="fleet", fill=MUTED,
                   font=("Helvetica", 9))

    legend = tk.Frame(wrapper, bg=CARD)
    legend.pack(side="left", padx=(20, 0), anchor="n", pady=(40, 0))

    for label, pct, color in segments:
        row = tk.Frame(legend, bg=CARD)
        row.pack(anchor="w", pady=6)
        swatch = tk.Frame(row, bg=color, width=12, height=12)
        swatch.pack(side="left", padx=(0, 8))
        swatch.pack_propagate(False)
        tk.Label(row, text=label, bg=CARD, fg=TEXT,
                 font=FONT_NORMAL, width=10,
                 anchor="w").pack(side="left")
        tk.Label(row, text=f"{pct}%", bg=CARD, fg=TEXT,
                 font=("Helvetica", 10, "bold")).pack(side="left")


# =========================================================
#  HELPERS
# =========================================================
def _nice_max(value):
    if value <= 0:
        return 10
    for step in (10, 20, 25, 50, 100, 200, 250, 500, 1000):
        top = ((value // step) + 1) * step
        if top <= value * 1.3:
            return top
    return ((value // 100) + 1) * 100
