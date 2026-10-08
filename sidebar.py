# sidebar.py
import tkinter as tk
from theme import *

NAV_ITEMS = [
    ("Dashboard",       "▦"),
    ("Taxi Records",    "🚗"),
    ("Trip Records",    "📋"),
    ("Driver Profiles", "👤"),
    ("Analysis",        "📊"),
    ("Visualization",   "📈"),
    ("Parking Zones",   "🅿"),
]


class Sidebar:
    def __init__(self, parent, on_navigate, on_logout):
        self.on_navigate = on_navigate
        self.buttons = {}
        self._active = None
        self.frame = tk.Frame(parent, bg=NAVY, width=240)
        self.frame.pack(side="left", fill="y")
        self.frame.pack_propagate(False)
        self._build_brand()
        self._build_nav()
        self._build_footer(on_logout)

    def _build_brand(self):
        brand = tk.Frame(self.frame, bg=NAVY)
        brand.pack(fill="x", pady=(18, 22), padx=16)
        logo = tk.Frame(brand, bg=ACCENT_LIGHT, width=42, height=42)
        logo.pack(side="left"); logo.pack_propagate(False)
        tk.Label(logo, text="🚕", bg=ACCENT_LIGHT, fg=NAVY,
                 font=("Helvetica", 18)).pack(expand=True)
        t = tk.Frame(brand, bg=NAVY); t.pack(side="left", padx=10)
        tk.Label(t, text="Jogay Jogay", bg=NAVY, fg="white",
                 font=("Helvetica", 13, "bold")).pack(anchor="w")
        tk.Label(t, text="TRANSPORT", bg=NAVY, fg="#8fa7c2",
                 font=("Helvetica", 7)).pack(anchor="w")
        tk.Label(t, text="AUTHORITY", bg=NAVY, fg="#8fa7c2",
                 font=("Helvetica", 7)).pack(anchor="w")

    def _build_nav(self):
        tk.Label(self.frame, text="MAIN MENU", bg=NAVY, fg="#7b93b3",
                 font=("Helvetica", 8, "bold")).pack(anchor="w",
                                                      padx=22, pady=(10, 8))
        for name, icon in NAV_ITEMS:
            self._nav_button(name, icon)

    def _nav_button(self, name, icon):
        btn = tk.Frame(self.frame, bg=NAVY, cursor="hand2", height=42)
        btn.pack(fill="x", padx=10, pady=1); btn.pack_propagate(False)
        accent = tk.Frame(btn, bg=NAVY, width=4); accent.pack(side="left", fill="y")
        ic = tk.Label(btn, text=icon, bg=NAVY, fg="#c5d3e2",
                      font=("Helvetica", 11), width=3); ic.pack(side="left", padx=(8, 0))
        lbl = tk.Label(btn, text=name, bg=NAVY, fg="#dbe5f0",
                       font=FONT_NORMAL, anchor="w")
        lbl.pack(side="left", fill="x", expand=True)
        self.buttons[name] = {"frame": btn, "accent": accent, "icon": ic, "label": lbl}
        for w in (btn, ic, lbl):
            w.bind("<Button-1>", lambda e, n=name: self.on_navigate(n))
            w.bind("<Enter>", lambda e, n=name: self._hover(n, True))
            w.bind("<Leave>", lambda e, n=name: self._hover(n, False))

    def _hover(self, name, entering):
        if name == self._active: return
        color = NAVY_HOVER if entering else NAVY
        r = self.buttons[name]
        for k in ("frame", "icon", "label"): r[k].configure(bg=color)

    def _build_footer(self, on_logout):
        tk.Frame(self.frame, bg=NAVY).pack(fill="both", expand=True)
        tk.Frame(self.frame, bg=NAVY_DARK, height=1).pack(fill="x", padx=16)
        lo = tk.Frame(self.frame, bg=NAVY, cursor="hand2")
        lo.pack(fill="x", padx=16, pady=10)
        tk.Label(lo, text="↪", bg=NAVY, fg="#8fa7c2",
                 font=("Helvetica", 12)).pack(side="left", padx=(6, 10))
        tk.Label(lo, text="Log out", bg=NAVY, fg="#8fa7c2",
                 font=FONT_NORMAL).pack(side="left")
        for w in (lo, *lo.winfo_children()):
            w.bind("<Button-1>", lambda e: on_logout())
        bar = tk.Frame(self.frame, bg=NAVY_DARK); bar.pack(fill="x", side="bottom")
        av = tk.Frame(bar, bg=ACCENT_LIGHT, width=36, height=36)
        av.pack(side="left", padx=16, pady=14); av.pack_propagate(False)
        tk.Label(av, text="TS", bg=ACCENT_LIGHT, fg=NAVY,
                 font=("Helvetica", 10, "bold")).pack(expand=True)
        info = tk.Frame(bar, bg=NAVY_DARK); info.pack(side="left")
        tk.Label(info, text="Tashi Sherpa", bg=NAVY_DARK, fg="white",
                 font=("Helvetica", 9, "bold")).pack(anchor="w")
        tk.Label(info, text="Administrator", bg=NAVY_DARK, fg="#8fa7c2",
                 font=("Helvetica", 8)).pack(anchor="w")

    def set_active(self, name):
        self._active = name
        for n, r in self.buttons.items():
            if n == name:
                r["frame"].configure(bg=NAVY_ACTIVE)
                r["accent"].configure(bg=GOLD)
                r["icon"].configure(bg=NAVY_ACTIVE, fg="white")
                r["label"].configure(bg=NAVY_ACTIVE, fg="white")
            else:
                r["frame"].configure(bg=NAVY)
                r["accent"].configure(bg=NAVY)
                r["icon"].configure(bg=NAVY, fg="#c5d3e2")
                r["label"].configure(bg=NAVY, fg="#dbe5f0")


class Header:
    def __init__(self, parent, initial_title="Dashboard", on_logout=None):
        self.on_logout = on_logout
        self._menu_open = False
        self._menu = None

        self.frame = tk.Frame(parent, bg="white", height=70,
                              highlightbackground=BORDER, highlightthickness=1)
        self.frame.pack(fill="x")
        self.frame.pack_propagate(False)

        left = tk.Frame(self.frame, bg="white")
        left.pack(side="left", padx=28, pady=12)
        tk.Label(left, text="BHUTAN TRANSPORT INFORMATION SYSTEM",
                 bg="white", fg=MUTED, font=FONT_SMALL).pack(anchor="w")
        self.title = tk.Label(left, text=initial_title, bg="white", fg=NAVY,
                              font=FONT_TITLE)
        self.title.pack(anchor="w")

        right = tk.Frame(self.frame, bg="white")
        right.pack(side="right", padx=28)

        d = tk.Frame(right, bg="white")
        d.pack(side="left", padx=(0, 20))
        tk.Label(d, text="Thursday, 21 March 2024", bg="white", fg=TEXT,
                 font=("Helvetica", 10, "bold")).pack(anchor="e")
        tk.Label(d, text="Last synced 08:42 AM", bg="white", fg=MUTED,
                 font=FONT_SMALL).pack(anchor="e")

        tk.Frame(right, bg=BORDER, width=1, height=36).pack(side="left", padx=10)

        self.chip = tk.Frame(right, bg="white", cursor="hand2")
        self.chip.pack(side="left")

        av = tk.Frame(self.chip, bg=ACCENT_LIGHT, width=36, height=36)
        av.pack(side="left")
        av.pack_propagate(False)
        tk.Label(av, text="TS", bg=ACCENT_LIGHT, fg=NAVY,
                 font=("Helvetica", 10, "bold")).pack(expand=True)

        self.arrow = tk.Label(self.chip, text="▾", bg="white", fg=MUTED,
                              font=("Helvetica", 10), cursor="hand2")
        self.arrow.pack(side="left", padx=6)

        for w in (self.chip, av, self.arrow, *av.winfo_children()):
            w.bind("<Button-1>", self._toggle_menu)

    def set_title(self, text):
        self.title.configure(text=text)

    def _toggle_menu(self, event=None):
        if self._menu_open:
            self._close_menu()
        else:
            self._open_menu()

    def _open_menu(self):
        self._menu = tk.Toplevel(self.chip)
        self._menu.wm_overrideredirect(True)
        self._menu.configure(bg=BORDER)

        self.chip.update_idletasks()
        x = self.chip.winfo_rootx() + self.chip.winfo_width() - 280
        y = self.chip.winfo_rooty() + self.chip.winfo_height() + 4
        width = 280
        self._menu.geometry(f"{width}x0+{x}+{y}")

        outer = tk.Frame(self._menu, bg="white",
                         highlightbackground=BORDER, highlightthickness=1)
        outer.pack(fill="both", expand=True, padx=1, pady=1)

        top = tk.Frame(outer, bg="white", padx=16, pady=14)
        top.pack(fill="x")

        av = tk.Frame(top, bg=ACCENT_LIGHT, width=42, height=42)
        av.pack(side="left")
        av.pack_propagate(False)
        tk.Label(av, text="TS", bg=ACCENT_LIGHT, fg=NAVY,
                 font=("Helvetica", 12, "bold")).pack(expand=True)

        info = tk.Frame(top, bg="white")
        info.pack(side="left", padx=12)
        tk.Label(info, text="Tashi Sherpa", bg="white", fg=TEXT,
                 font=("Helvetica", 11, "bold")).pack(anchor="w")
        tk.Label(info, text="Administrator", bg="white", fg=MUTED,
                 font=FONT_SMALL).pack(anchor="w")

        tk.Frame(outer, bg=BORDER, height=1).pack(fill="x")
        org = tk.Frame(outer, bg="white", padx=16, pady=10)
        org.pack(fill="x")
        tk.Label(org, text="Transport Authority · Thimphu",
                 bg="white", fg=MUTED, font=FONT_SMALL).pack(anchor="w")
        tk.Frame(outer, bg=BORDER, height=1).pack(fill="x")

        items_frame = tk.Frame(outer, bg="white", pady=6)
        items_frame.pack(fill="x")

        self._menu_item(items_frame, "Account details",
                        lambda: self._menu_action("Account details"))
        self._menu_item(items_frame, "System preferences",
                        lambda: self._menu_action("System preferences"))

        tk.Frame(outer, bg=BORDER, height=1).pack(fill="x")
        self._menu_item(items_frame, "Log out",
                        self._handle_logout, danger=True)

        outer.update_idletasks()
        h = outer.winfo_reqheight() + 2
        self._menu.geometry(f"{width}x{h}+{x}+{y}")

        self.arrow.configure(text="▴")
        self._menu_open = True

        self._menu.focus_set()
        self.chip.winfo_toplevel().bind("<Button-1>",
                                        self._global_click, add="+")

    def _menu_item(self, parent, label, command, danger=False):
        color = RED if danger else TEXT
        row = tk.Frame(parent, bg="white", cursor="hand2")
        row.pack(fill="x")

        lbl = tk.Label(row, text=label, bg="white", fg=color,
                       font=FONT_NORMAL, anchor="w",
                       padx=16, pady=10)
        lbl.pack(fill="x")

        def on_enter(_):
            row.configure(bg="#f0f5fa")
            lbl.configure(bg="#f0f5fa")

        def on_leave(_):
            row.configure(bg="white")
            lbl.configure(bg="white")

        for w in (row, lbl):
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", lambda e: command())

    def _menu_action(self, name):
        self._close_menu()
        root = self.chip.winfo_toplevel()
        app = getattr(root, "_jogay_app", None)
        if app and name == "Account details":
            app.navigate("Account details")
        elif app and name == "System preferences":
            app.navigate("System preferences")
        else:
            from tkinter import messagebox
            messagebox.showinfo(name, f"{name} would open here.")

    def _handle_logout(self):
        self._close_menu()
        if self.on_logout:
            self.on_logout()

    def _global_click(self, event):
        if not self._menu_open:
            return
        widget = event.widget
        if widget == self._menu or str(widget).startswith(str(self._menu)):
            return
        if widget == self.chip or str(widget).startswith(str(self.chip)):
            return
        self._close_menu()

    def _close_menu(self):
        if self._menu:
            try:
                self._menu.destroy()
            except Exception:
                pass
            self._menu = None
        self._menu_open = False
        self.arrow.configure(text="▾")
        try:
            self.chip.winfo_toplevel().unbind("<Button-1>")
        except Exception:
            pass