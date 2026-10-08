# pages/parking_zones.py
import tkinter as tk
from theme import *
from widgets import (card, load_image, parking_photo_path,
                     driver_photo_path, vehicle_photo_path)
from backend import get_parking_zones, get_drivers


def build(parent):
    page = tk.Frame(parent, bg=BG, padx=25, pady=22)
    page.pack(fill="both", expand=True)

    header = card(page); header.pack(fill="x")
    tk.Label(header, text="Taxi parking zones", bg=CARD, fg=TEXT,
             font=FONT_HEAD).pack(anchor="w")
    tk.Label(header,
             text="Stationed taxis reported by local authority and stand "
                  "across all 20 dzongkhags. Click a zone to see stationed drivers.",
             bg=CARD, fg=MUTED, font=FONT_SMALL).pack(anchor="w", pady=(2, 0))

    outer = tk.Frame(page, bg=BG)
    outer.pack(fill="both", expand=True, pady=(18, 0))
    canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    sb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    sb.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=sb.set)

    grid = tk.Frame(canvas, bg=BG)
    window_id = canvas.create_window((0, 0), window=grid, anchor="nw")

    def on_grid_conf(_):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfigure(window_id, width=canvas.winfo_width())
    grid.bind("<Configure>", on_grid_conf)
    canvas.bind("<Configure>", on_grid_conf)

    def _wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _wheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    for i, (name, dzong, count) in enumerate(get_parking_zones()):
        r, c = divmod(i, 3)
        _parking_card(grid, name, dzong, count, r, c, page)


def _parking_card(parent, name, dzong, count, row, col, page_ref):
    parent.grid_columnconfigure(col, weight=1, uniform="pk")
    parent.grid_rowconfigure(row, weight=1)

    wrapper = card(parent, padx=0, pady=0)
    wrapper.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

    img = tk.Frame(wrapper, bg="#2c3e50", height=160)
    img.pack(fill="x"); img.pack_propagate(False)

    photo = load_image(parking_photo_path(name), width=340, height=160)
    if photo:
        lbl = tk.Label(img, image=photo, bg="#2c3e50", bd=0, cursor="hand2")
        lbl.image = photo
        lbl.pack(expand=True, fill="both")
    else:
        lbl = tk.Label(img, text="🚕 TAKSI 🚕", bg="#2c3e50", fg=GOLD,
                       font=("Helvetica", 18, "bold"), cursor="hand2")
        lbl.pack(expand=True)

    body = tk.Frame(wrapper, bg=CARD, padx=18, pady=16, cursor="hand2")
    body.pack(fill="both", expand=True)

    title_lbl = tk.Label(body, text=name, bg=CARD, fg=TEXT,
                         font=("Helvetica", 13, "bold"), cursor="hand2")
    title_lbl.pack(anchor="w")

    dzong_lbl = tk.Label(body, text=dzong, bg=CARD, fg=MUTED,
                         font=FONT_SMALL, cursor="hand2")
    dzong_lbl.pack(anchor="w", pady=(2, 14))

    bottom = tk.Frame(body, bg=CARD, cursor="hand2"); bottom.pack(fill="x")
    stat_lbl = tk.Label(bottom, text="STATIONED TAXIS", bg=CARD, fg=MUTED,
                        font=FONT_TINY, cursor="hand2")
    stat_lbl.pack(side="left")
    count_lbl = tk.Label(bottom, text=count, bg=CARD, fg=NAVY,
                         font=("Helvetica", 20, "bold"), cursor="hand2")
    count_lbl.pack(side="right")

    def on_enter(_):
        wrapper.configure(highlightbackground=ACCENT, highlightthickness=2)
        body.configure(bg="#f0f5fa")
        for w in (title_lbl, dzong_lbl, stat_lbl, count_lbl, bottom):
            w.configure(bg="#f0f5fa")

    def on_leave(_):
        wrapper.configure(highlightbackground=BORDER, highlightthickness=1)
        body.configure(bg=CARD)
        for w in (title_lbl, dzong_lbl, stat_lbl, count_lbl, bottom):
            w.configure(bg=CARD)

    def open_zone(event=None):
        _open_zone_detail(page_ref.winfo_toplevel(), name, dzong, count)

    for w in (wrapper, img, body, bottom,
              title_lbl, dzong_lbl, stat_lbl, count_lbl):
        w.bind("<Button-1>", open_zone)
        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)


def _open_zone_detail(parent, zone_name, dzongkhag, count):
    win = tk.Toplevel(parent)
    win.title(f"{zone_name} — Drivers Stationed")
    win.geometry("820x720")
    win.configure(bg=BG)
    win.transient(parent)
    win.grab_set()

    banner = tk.Frame(win, bg=NAVY, height=140)
    banner.pack(fill="x"); banner.pack_propagate(False)

    img_box = tk.Frame(banner, bg="#2c3e50", width=200, height=140)
    img_box.pack(side="left"); img_box.pack_propagate(False)

    photo = load_image(parking_photo_path(zone_name), width=200, height=140)
    if photo:
        lbl = tk.Label(img_box, image=photo, bg="#2c3e50", bd=0)
        lbl.image = photo
        lbl.pack(expand=True, fill="both")
    else:
        tk.Label(img_box, text="🚕", bg="#2c3e50", fg=GOLD,
                 font=("Helvetica", 40)).pack(expand=True)

    tinfo = tk.Frame(banner, bg=NAVY, padx=24, pady=20)
    tinfo.pack(side="left", fill="both", expand=True)

    tk.Label(tinfo, text="PARKING ZONE", bg=NAVY, fg="#8fa7c2",
             font=FONT_TINY).pack(anchor="w")
    tk.Label(tinfo, text=zone_name, bg=NAVY, fg="white",
             font=("Helvetica", 20, "bold")).pack(anchor="w", pady=(4, 6))
    tk.Label(tinfo, text=dzongkhag, bg=NAVY, fg="#c5d3e2",
             font=FONT_NORMAL).pack(anchor="w")
    tk.Label(tinfo, text=f"{count} taxis stationed",
             bg=NAVY, fg=GOLD,
             font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(6, 0))

    body = tk.Frame(win, bg=BG, padx=24, pady=18)
    body.pack(fill="both", expand=True)

    dzong_clean = dzongkhag.replace("dzongkhag", "").strip().lower()
    all_drivers = get_drivers()
    stationed = [d for d in all_drivers
                 if d["dzongkhag"].strip().lower() == dzong_clean]

    title_row = tk.Frame(body, bg=BG); title_row.pack(fill="x")
    tk.Label(title_row, text="Drivers stationed here", bg=BG, fg=TEXT,
             font=FONT_HEAD).pack(side="left")
    tk.Label(title_row, text=f"{len(stationed)} drivers", bg=BG, fg=MUTED,
             font=FONT_SMALL).pack(side="left", padx=10, pady=(6, 0))

    list_outer = tk.Frame(body, bg=BG)
    list_outer.pack(fill="both", expand=True, pady=(12, 0))

    canvas = tk.Canvas(list_outer, bg=BG, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    sb = tk.Scrollbar(list_outer, orient="vertical", command=canvas.yview)
    sb.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=sb.set)

    inner = tk.Frame(canvas, bg=BG)
    canvas.create_window((0, 0), window=inner, anchor="nw")
    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def _wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _wheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    def go_to_driver(driver_name):
        win.destroy()
        root = parent
        app = getattr(root, "_jogay_app", None)
        if app is None:
            app = getattr(root.winfo_toplevel(), "_jogay_app", None)
        if app:
            app.navigate("Driver Profiles", driver_name=driver_name)

    if not stationed:
        empty = card(inner, padx=24, pady=40)
        empty.pack(fill="x")
        tk.Label(empty, text="No drivers currently stationed in this zone.",
                 bg=CARD, fg=MUTED, font=FONT_NORMAL).pack()
    else:
        for d in stationed:
            _driver_card(inner, d, on_click=go_to_driver)

    footer = tk.Frame(win, bg=BG, padx=24, pady=14)
    footer.pack(fill="x")
    tk.Button(footer, text="Close", bg=ACCENT, fg="white", bd=0,
              activebackground=ACCENT_DARK, activeforeground="white",
              font=("Helvetica", 10, "bold"), padx=24, pady=8,
              cursor="hand2", command=win.destroy).pack(side="right")


def _driver_card(parent, driver, on_click):
    c = card(parent, padx=0, pady=0)
    c.pack(fill="x", pady=6)

    row = tk.Frame(c, bg=CARD, padx=16, pady=12, cursor="hand2")
    row.pack(fill="x")

    av = tk.Frame(row, bg=ACCENT_LIGHT, width=56, height=56)
    av.pack(side="left"); av.pack_propagate(False)

    photo = load_image(driver_photo_path(driver), width=56, height=56)
    if photo:
        lbl = tk.Label(av, image=photo, bg=ACCENT_LIGHT, bd=0)
        lbl.image = photo
        lbl.pack(expand=True, fill="both")
    else:
        initials = "".join(p[0] for p in driver["name"].split()[:2]).upper()
        tk.Label(av, text=initials, bg=ACCENT_LIGHT, fg=NAVY,
                 font=("Helvetica", 12, "bold")).pack(expand=True)

    info = tk.Frame(row, bg=CARD); info.pack(side="left", padx=14)
    tk.Label(info, text=driver["name"], bg=CARD, fg=TEXT,
             font=("Helvetica", 12, "bold")).pack(anchor="w")
    tk.Label(info, text=f"{driver['vehicle']} · {driver['plate']}",
             bg=CARD, fg=MUTED, font=FONT_SMALL).pack(anchor="w", pady=(2, 0))
    tk.Label(info, text=f"Contact: {driver['contact']}",
             bg=CARD, fg=MUTED, font=FONT_SMALL).pack(anchor="w")

    ci = tk.Frame(row, bg="#2c3e50", width=110, height=62)
    ci.pack(side="right"); ci.pack_propagate(False)

    car = load_image(vehicle_photo_path(driver["vehicle"]),
                     width=110, height=62)
    if car:
        lbl = tk.Label(ci, image=car, bg="#2c3e50", bd=0)
        lbl.image = car
        lbl.pack(expand=True, fill="both")
    else:
        tk.Label(ci, text="🚕", bg="#2c3e50", fg=GOLD,
                 font=("Helvetica", 20)).pack(expand=True)

    status_color = GREEN if driver["status"] in ("Available", "Completed") \
        else GOLD if driver["status"] == "On Trip" else RED
    dot = tk.Frame(row, bg=status_color, width=10, height=10)
    dot.pack(side="right", padx=(0, 14))
    dot.pack_propagate(False)

    def on_enter(_):
        row.configure(bg="#f0f5fa")
        for w in (info, *info.winfo_children()):
            w.configure(bg="#f0f5fa")

    def on_leave(_):
        row.configure(bg=CARD)
        for w in (info, *info.winfo_children()):
            w.configure(bg=CARD)

    def clicked(_):
        on_click(driver["name"])

    for w in (c, row, av, info, ci,
              *info.winfo_children(), *av.winfo_children(),
              *ci.winfo_children(), dot):
        w.bind("<Button-1>", clicked)
        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)