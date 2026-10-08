# pages/driver_profiles.py
import tkinter as tk
from theme import *
from widgets import (card, data_table, load_image,
                     driver_photo_path, vehicle_photo_path)
from backend import get_drivers


def build(parent, pending_driver=None):
    page = tk.Frame(parent, bg=BG, padx=25, pady=22)
    page.pack(fill="both", expand=True)

    drivers = get_drivers()

    # ---------- LEFT: list of drivers ----------
    left = card(page, padx=0, pady=0)
    left.pack(side="left", fill="y")
    left.configure(width=280); left.pack_propagate(False)

    header = tk.Frame(left, bg=CARD, padx=18, pady=16); header.pack(fill="x")
    tk.Label(header, text="Driver Profiles", bg=CARD, fg=TEXT,
             font=FONT_HEAD).pack(anchor="w")
    tk.Label(header, text=f"{len(drivers)} drivers registered",
             bg=CARD, fg=MUTED, font=FONT_SMALL).pack(anchor="w", pady=(2, 0))
    tk.Frame(left, bg=BORDER, height=1).pack(fill="x")

    list_wrap = tk.Frame(left, bg=CARD); list_wrap.pack(fill="both", expand=True)
    canvas = tk.Canvas(list_wrap, bg=CARD, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    sb = tk.Scrollbar(list_wrap, orient="vertical", command=canvas.yview)
    sb.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=sb.set)

    list_frame = tk.Frame(canvas, bg=CARD)
    canvas.create_window((0, 0), window=list_frame, anchor="nw", width=278)
    list_frame.bind("<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def _wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _wheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # ---------- RIGHT: detail panel (scrollable) ----------
    right_outer = tk.Frame(page, bg=BG)
    right_outer.pack(side="left", fill="both", expand=True, padx=(14, 0))

    right_canvas = tk.Canvas(right_outer, bg=BG, highlightthickness=0)
    right_canvas.pack(side="left", fill="both", expand=True)

    right_sb = tk.Scrollbar(right_outer, orient="vertical",
                            command=right_canvas.yview)
    right_sb.pack(side="right", fill="y")
    right_canvas.configure(yscrollcommand=right_sb.set)

    right = tk.Frame(right_canvas, bg=BG)
    right_window = right_canvas.create_window((0, 0), window=right, anchor="nw")

    def _right_configure(_):
        right_canvas.configure(scrollregion=right_canvas.bbox("all"))
    right.bind("<Configure>", _right_configure)

    def _right_canvas_configure(event):
        right_canvas.itemconfigure(right_window, width=event.width)
    right_canvas.bind("<Configure>", _right_canvas_configure)

    def _right_wheel(event):
        right_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    right_canvas.bind(
        "<Enter>",
        lambda e: right_canvas.bind_all("<MouseWheel>", _right_wheel))
    right_canvas.bind(
        "<Leave>",
        lambda e: right_canvas.unbind_all("<MouseWheel>"))

    state = {"selected": 0, "buttons": []}

    def select(index):
        state["selected"] = index
        for i, btn in enumerate(state["buttons"]):
            bg = "#eaf2fb" if i == index else CARD
            btn.configure(bg=bg)
            for child in btn.winfo_children():
                if child.cget("bg") not in (ACCENT_LIGHT, "#d0d7de", "#2c3e50",
                                            GREEN, GOLD, RED):
                    child.configure(bg=bg)
                for sub in child.winfo_children():
                    if sub.cget("bg") not in (ACCENT_LIGHT, "#d0d7de", "#2c3e50",
                                              GREEN, GOLD, RED):
                        sub.configure(bg=bg)
        for w in right.winfo_children():
            w.destroy()
        _build_detail(right, drivers[index])
        right_canvas.yview_moveto(0)

    for i, d in enumerate(drivers):
        row = _driver_row(list_frame, d, on_click=lambda i=i: select(i))
        state["buttons"].append(row)

    start_index = 0
    if pending_driver:
        for i, d in enumerate(drivers):
            if d["name"].lower() == pending_driver.lower():
                start_index = i
                break
    select(start_index)


def _driver_row(parent, driver, on_click):
    row = tk.Frame(parent, bg=CARD, cursor="hand2"); row.pack(fill="x")
    inner = tk.Frame(row, bg=CARD, padx=14, pady=12); inner.pack(fill="x")

    av = tk.Frame(inner, bg=ACCENT_LIGHT, width=44, height=44)
    av.pack(side="left"); av.pack_propagate(False)

    photo = load_image(driver_photo_path(driver), width=44, height=44)
    if photo:
        lbl = tk.Label(av, image=photo, bg=ACCENT_LIGHT, bd=0)
        lbl.image = photo
        lbl.pack(expand=True)
    else:
        initials = "".join(p[0] for p in driver["name"].split()[:2]).upper()
        tk.Label(av, text=initials, bg=ACCENT_LIGHT, fg=NAVY,
                 font=("Helvetica", 12, "bold")).pack(expand=True)

    info = tk.Frame(inner, bg=CARD); info.pack(side="left", padx=12)
    tk.Label(info, text=driver["name"], bg=CARD, fg=TEXT,
             font=FONT_BOLD).pack(anchor="w")
    tk.Label(info, text=driver["dzongkhag"], bg=CARD, fg=MUTED,
             font=FONT_SMALL).pack(anchor="w")

    status_color = GREEN if driver["status"] in ("Available", "Completed") \
        else GOLD if driver["status"] == "On Trip" else RED
    dot = tk.Frame(inner, bg=status_color, width=8, height=8)
    dot.pack(side="right", padx=6); dot.pack_propagate(False)

    for w in (row, inner, av, info, *info.winfo_children()):
        w.bind("<Button-1>", lambda e: on_click())
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x")
    return row


def _build_detail(parent, driver):
    prof = card(parent, padx=25, pady=25); prof.pack(fill="x")
    head = tk.Frame(prof, bg=CARD); head.pack(fill="x")

    av = tk.Frame(head, bg="#d0d7de", width=110, height=130)
    av.pack(side="left"); av.pack_propagate(False)

    photo = load_image(driver_photo_path(driver), width=110, height=130)
    if photo:
        lbl = tk.Label(av, image=photo, bg="#d0d7de", bd=0)
        lbl.image = photo
        lbl.pack(expand=True, fill="both")
    else:
        tk.Label(av, text="👤", bg="#d0d7de", fg="#5a6b7d",
                 font=("Helvetica", 40)).pack(expand=True)

    info = tk.Frame(head, bg=CARD); info.pack(side="left", padx=20, anchor="n")
    tk.Label(info, text="DRIVER PROFILE", bg=CARD, fg=MUTED,
             font=FONT_TINY).pack(anchor="w")
    tk.Label(info, text=driver["name"], bg=CARD, fg=NAVY,
             font=("Helvetica", 20, "bold")).pack(anchor="w", pady=(2, 8))
    tk.Label(info, text=f"License No: {driver['license']}",
             bg=CARD, fg=MUTED, font=FONT_NORMAL).pack(anchor="w")
    tk.Label(info, text=f"Contact: {driver['contact']}",
             bg=CARD, fg=MUTED, font=FONT_NORMAL).pack(anchor="w", pady=(2, 10))

    badge_bg = "#d4ecd8" if driver["status"] in ("Available", "Completed") \
        else "#fce8c4" if driver["status"] == "On Trip" else "#f5d0cc"
    badge_fg = GREEN if driver["status"] in ("Available", "Completed") \
        else GOLD if driver["status"] == "On Trip" else RED
    badge = tk.Frame(info, bg=badge_bg); badge.pack(anchor="w")
    tk.Label(badge, text=driver["status"], bg=badge_bg, fg=badge_fg,
             font=("Helvetica", 9, "bold"), padx=10, pady=3).pack()

    tk.Frame(prof, bg=BORDER, height=1).pack(fill="x", pady=25)
    tk.Label(prof, text="ASSIGNED VEHICLE", bg=CARD, fg=MUTED,
             font=FONT_TINY).pack(anchor="w")

    veh_wrap = tk.Frame(prof, bg="#f8fafc",
                        highlightbackground=BORDER, highlightthickness=1)
    veh_wrap.pack(fill="x", pady=(10, 0))

    veh = tk.Frame(veh_wrap, bg="#f8fafc", padx=14, pady=14)
    veh.pack(fill="x")

    ci = tk.Frame(veh, bg="#2c3e50", width=240, height=140)
    ci.pack(side="left")
    ci.pack_propagate(False)

    car_photo = load_image(vehicle_photo_path(driver["vehicle"]),
                           width=240, height=140)
    if car_photo:
        lbl = tk.Label(ci, image=car_photo, bg="#2c3e50", bd=0)
        lbl.image = car_photo
        lbl.pack(expand=True, fill="both")
    else:
        tk.Label(ci, text="🚕", bg="#2c3e50", fg=GOLD,
                 font=("Helvetica", 40)).pack(expand=True)

    vt = tk.Frame(veh, bg="#f8fafc")
    vt.pack(side="left", padx=20, anchor="n")

    tk.Label(vt, text=driver["vehicle"], bg="#f8fafc", fg=NAVY,
             font=("Helvetica", 16, "bold")).pack(anchor="w", pady=(4, 2))

    tk.Label(vt, text=f"Plate: {driver['plate']}",
             bg="#f8fafc", fg=TEXT, font=FONT_BOLD).pack(anchor="w", pady=(6, 0))

    tk.Label(vt, text=f"Dzongkhag: {driver['dzongkhag']}",
             bg="#f8fafc", fg=MUTED,
             font=FONT_NORMAL).pack(anchor="w", pady=(2, 0))

    tk.Label(vt, text=f"Assigned to: {driver['name']}",
             bg="#f8fafc", fg=MUTED,
             font=FONT_NORMAL).pack(anchor="w", pady=(2, 0))

    perf = card(parent); perf.pack(fill="x", pady=(14, 0))
    tk.Label(perf, text="Performance summary", bg=CARD, fg=TEXT,
             font=FONT_HEAD).pack(anchor="w", pady=(0, 14))
    stats = tk.Frame(perf, bg=CARD); stats.pack(fill="x")
    _mini_stat(stats, "TRIPS COMPLETED", driver["trips"], "This year")
    _mini_stat(stats, "RATING",          driver["rating"], "From reviews")
    _mini_stat(stats, "CANCELLATIONS",   driver["cancellations"], "Total")

    act = card(parent); act.pack(fill="both", expand=True, pady=(14, 0))
    tk.Label(act, text="RECENT ACTIVITY", bg=CARD, fg=MUTED,
             font=FONT_TINY).pack(anchor="w", pady=(0, 10))
    data_table(act, ("Date", "Route", "Status"), [120, 300, 120],
               driver["activity"], status_col=2)


def _mini_stat(parent, title, value, sub):
    w = tk.Frame(parent, bg=CARD, highlightbackground=BORDER,
                 highlightthickness=1, padx=16, pady=14)
    w.pack(side="left", fill="both", expand=True, padx=4)
    tk.Frame(w, bg=ACCENT, width=4).pack(side="left", fill="y", padx=(0, 10))
    inner = tk.Frame(w, bg=CARD); inner.pack(side="left", fill="both", expand=True)
    tk.Label(inner, text=title, bg=CARD, fg=MUTED,
             font=FONT_TINY).pack(anchor="w")
    tk.Label(inner, text=value, bg=CARD, fg=NAVY,
             font=("Helvetica", 22, "bold")).pack(anchor="w")
    tk.Label(inner, text=sub, bg=CARD, fg=MUTED,
             font=FONT_SMALL).pack(anchor="w")