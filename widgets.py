# widgets.py
import tkinter as tk
from theme import *


def card(parent, padx=20, pady=20):
    return tk.Frame(parent, bg=CARD, padx=padx, pady=pady,
                    highlightbackground=BORDER, highlightthickness=1)


def primary_button(parent, text, command=None):
    return tk.Button(parent, text=text, bg=ACCENT, fg="white", bd=0,
                     activebackground=ACCENT_DARK, activeforeground="white",
                     font=("Helvetica", 10, "bold"), padx=16, pady=8,
                     cursor="hand2", command=command)


def secondary_button(parent, text, command=None):
    return tk.Button(parent, text=text, bg="white", fg=TEXT, bd=1,
                     relief="solid", font=FONT_NORMAL,
                     padx=16, pady=8, cursor="hand2", command=command)


def stat_card(parent, title, value, sub, accent=ACCENT, big=True):
    wrapper = tk.Frame(parent, bg=CARD, highlightbackground=BORDER,
                       highlightthickness=1)
    wrapper.pack(side="left", fill="both", expand=True, padx=6)
    tk.Frame(wrapper, bg=accent, width=4).pack(side="left", fill="y")
    inner = tk.Frame(wrapper, bg=CARD, padx=18, pady=18)
    inner.pack(side="left", fill="both", expand=True)
    tk.Label(inner, text=title, bg=CARD, fg=MUTED,
             font=FONT_TINY).pack(anchor="w")
    size = 26 if big else 20
    tk.Label(inner, text=value, bg=CARD, fg=NAVY,
             font=("Helvetica", size, "bold")).pack(anchor="w", pady=(4, 4))
    tk.Label(inner, text=sub, bg=CARD, fg=MUTED,
             font=FONT_SMALL).pack(anchor="w")


def data_table(parent, columns, widths, rows, status_col=None):
    header = tk.Frame(parent, bg=TABLE_HEAD)
    header.pack(fill="x", pady=(10, 0))
    for col, w in zip(columns, widths):
        tk.Label(header, text=col, bg=TABLE_HEAD, fg=MUTED,
                 font=FONT_TINY, width=w // 8,
                 anchor="w").pack(side="left", padx=10, pady=8)

    for i, row in enumerate(rows):
        bg = CARD if i % 2 == 0 else TABLE_ALT
        r = tk.Frame(parent, bg=bg)
        r.pack(fill="x")
        for j, (val, w) in enumerate(zip(row, widths)):
            color, weight = TEXT, "normal"
            if status_col is not None and j == status_col:
                weight = "bold"
                if val in ("Active", "Completed", "High", "Available"):
                    color = GREEN
                elif val in ("Review", "On Trip", "Medium"):
                    color = GOLD
                elif val in ("Low", "Inactive"):
                    color = RED
            tk.Label(r, text=val, bg=bg, fg=color,
                     font=("Helvetica", 10, weight),
                     width=w // 8, anchor="w").pack(side="left",
                                                     padx=10, pady=10)
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x")


def bar_row(parent, label, value, max_value, bar_width=420, width_chars=14):
    row = tk.Frame(parent, bg=CARD)
    row.pack(fill="x", pady=4)
    tk.Label(row, text=label, bg=CARD, fg=MUTED,
             font=FONT_NORMAL, width=width_chars,
             anchor="w").pack(side="left")
    track = tk.Frame(row, bg="#eef2f7", height=14, width=bar_width)
    track.pack(side="left", padx=8)
    track.pack_propagate(False)
    fill_w = max(4, int(bar_width * value / max_value))
    tk.Frame(track, bg=ACCENT, height=14, width=fill_w).place(x=0, y=0)
    tk.Label(row, text=str(value), bg=CARD, fg=TEXT,
             font=("Helvetica", 10, "bold")).pack(side="left", padx=8)


def search_bar(parent, placeholder):
    s = tk.Frame(parent, bg="white",
                 highlightbackground=BORDER, highlightthickness=1)
    s.pack(side="left", fill="x", expand=True, padx=(0, 10))
    tk.Label(s, text="🔍", bg="white", fg=MUTED,
             font=("Helvetica", 11)).pack(side="left", padx=10)
    entry = tk.Entry(s, bd=0, bg="white", fg=TEXT, font=FONT_NORMAL,
                     insertbackground=TEXT)
    entry.pack(side="left", fill="x", expand=True, ipady=8)
    entry.insert(0, placeholder)
    entry.configure(fg="#b0bcc9")

    def on_focus_in(_):
        if entry.get() == placeholder:
            entry.delete(0, "end"); entry.configure(fg=TEXT)

    def on_focus_out(_):
        if not entry.get():
            entry.insert(0, placeholder); entry.configure(fg="#b0bcc9")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    entry._placeholder = placeholder
    return entry


class Dropdown(tk.Frame):
    def __init__(self, parent, options, default=None, width=22, on_change=None):
        super().__init__(parent, bg="white",
                         highlightbackground=BORDER, highlightthickness=1)
        self.options = list(options)
        self.value = default if default is not None else self.options[0]
        self.on_change = on_change
        self._menu_open = False
        self._menu = None

        self.label = tk.Label(self, text=f"{self.value} ▾", bg="white",
                              fg=TEXT, font=FONT_NORMAL, anchor="w",
                              width=width, padx=10, pady=8, cursor="hand2")
        self.label.pack(fill="x")
        self.label.bind("<Button-1>", self._toggle)

    def _toggle(self, event=None):
        if self._menu_open: self._close()
        else: self._open()

    def _open(self):
        self._menu = tk.Toplevel(self)
        self._menu.wm_overrideredirect(True)
        self._menu.configure(bg=BORDER)
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self._menu.geometry(f"{self.winfo_width()}x0+{x}+{y}")

        list_frame = tk.Frame(self._menu, bg="white")
        list_frame.pack(fill="both", expand=True, padx=1, pady=1)
        canvas = tk.Canvas(list_frame, bg="white", highlightthickness=0,
                           height=min(280, 26 * len(self.options)))
        canvas.pack(side="left", fill="both", expand=True)
        sb = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        sb.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=sb.set)

        inner = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=inner, anchor="nw")
        for opt in self.options:
            bg = "#eaf2fb" if opt == self.value else "white"
            lbl = tk.Label(inner, text=opt, bg=bg, fg=TEXT,
                           font=FONT_NORMAL, anchor="w",
                           padx=10, pady=6, cursor="hand2")
            lbl.pack(fill="x")
            lbl.bind("<Button-1>", lambda e, o=opt: self._select(o))
            lbl.bind("<Enter>", lambda e, l=lbl: l.configure(bg="#eaf2fb"))
            lbl.bind("<Leave>", lambda e, o=opt, l=lbl:
                     l.configure(bg="#eaf2fb" if o == self.value else "white"))
        inner.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        self._menu.update_idletasks()
        h = list_frame.winfo_reqheight() + 2
        self._menu.geometry(f"{self.winfo_width()}x{h}+{x}+{y}")
        self._menu.focus_set()
        self._menu_open = True
        self.winfo_toplevel().bind("<Button-1>", self._global_click, add="+")

    def _global_click(self, event):
        if not self._menu_open: return
        widget = event.widget
        if widget == self._menu or str(widget).startswith(str(self._menu)):
            return
        self._close()

    def _select(self, option):
        self.value = option
        self.label.configure(text=f"{option} ▾")
        self._close()
        if self.on_change: self.on_change(option)

    def _close(self):
        if self._menu:
            try: self._menu.destroy()
            except Exception: pass
            self._menu = None
        self._menu_open = False

    def get(self):
        return self.value


def scrollable_page(parent):
    outer = tk.Frame(parent, bg=BG)
    outer.pack(fill="both", expand=True)
    canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    sb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    sb.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=sb.set)

    inner = tk.Frame(canvas, bg=BG)
    window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>",
                lambda e: canvas.itemconfigure(window_id, width=e.width))

    def _wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _wheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    return inner


def scrollable_table(parent):
    outer = tk.Frame(parent, bg=CARD)
    outer.pack(fill="both", expand=True)
    canvas = tk.Canvas(outer, bg=CARD, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    sb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    sb.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=sb.set)

    inner = tk.Frame(canvas, bg=CARD)
    window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>",
                lambda e: canvas.itemconfigure(window_id, width=e.width))

    def _wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _wheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    return inner


# =========================================================
#  Image loading helpers
# =========================================================
_image_cache = {}


def load_image(path, width=None, height=None):
    """
    Load an image from disk (png/jpg/jpeg/gif), optionally resized to fit
    within (width, height) while preserving aspect ratio.
    """
    import os
    if not path or not os.path.exists(path):
        return None

    key = (path, width, height)
    if key in _image_cache:
        return _image_cache[key]

    try:
        from PIL import Image, ImageTk
        img = Image.open(path)
        img.load()
        if width and height:
            img.thumbnail((width, height), Image.LANCZOS)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA")
        photo = ImageTk.PhotoImage(img)
        _image_cache[key] = photo
        return photo
    except ImportError:
        try:
            photo = tk.PhotoImage(file=path)
            _image_cache[key] = photo
            return photo
        except Exception:
            return None
    except Exception:
        return None


def driver_photo_path(driver):
    import os
    first = driver["name"].split()[0].lower()
    last  = driver["name"].split()[-1].lower()
    candidates = [
        f"driver_{first}{last}.jpg",
        f"driver_{first}{last}.jpeg",
        f"driver_{first}{last}.png",
        f"driver_{first}{last}.jpg.jpg",
        f"driver_{first}.jpg",
        f"driver_{first}.jpeg",
        f"driver_{first}.png",
        f"driver_{first}.jpg.jpg",
    ]
    for name in candidates:
        path = os.path.join("images", name)
        if os.path.exists(path):
            return path
    return os.path.join("images", f"driver_{first}.jpg")


def vehicle_photo_path(vehicle):
    import os
    if not vehicle:
        return os.path.join("images", "car_photo.jpg")

    name = vehicle.lower()
    name = name.replace("(", "").replace(")", "")
    name = name.replace("-", " ")
    name = "_".join(name.split())

    candidates = [
        f"car_{name}.jpg",
        f"car_{name}.jpeg",
        f"car_{name}.png",
        f"car_{name}.jpg.jpg",
    ]
    for cand in candidates:
        path = os.path.join("images", cand)
        if os.path.exists(path):
            return path
    return os.path.join("images", "car_photo.jpg")


def parking_photo_path(zone_name):
    """
    Build the image path for a parking zone.
    e.g. "Thimphu Taxi Stand" -> images/parking_thimphu.jpg
    Falls back to images/parking_default.jpg.
    """
    import os
    if not zone_name:
        return os.path.join("images", "parking_default.jpg")

    name = zone_name.lower()
    name = name.replace("taxi stand", "").replace("stand", "")
    name = name.replace("(", "").replace(")", "")
    name = name.replace("-", " ")
    name = "_".join(name.split())

    candidates = [
        f"parking_{name}.jpg",
        f"parking_{name}.jpeg",
        f"parking_{name}.png",
        f"parking_{name}.jpg.jpg",
    ]
    for cand in candidates:
        path = os.path.join("images", cand)
        if os.path.exists(path):
            return path
    return os.path.join("images", "parking_default.jpg")