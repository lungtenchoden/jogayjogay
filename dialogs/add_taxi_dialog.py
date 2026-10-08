# dialogs/add_taxi_dialog.py
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import date, datetime

from theme import *
from widgets import Dropdown
from data import DZONGKHAGS, VEHICLE_TYPES, STATUSES


class AddTaxiDialog(tk.Toplevel):
    def __init__(self, parent, on_save):
        super().__init__(parent)
        self.on_save = on_save
        self.photo_path = None
        self._preview_img = None   # keep reference so Tk doesn't GC it

        self.title("Add Taxi Record")
        self.geometry("620x740")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # -------- header --------
        header = tk.Frame(self, bg=NAVY, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="Add Taxi Record", bg=NAVY, fg="white",
                 font=("Helvetica", 16, "bold")).pack(side="left", padx=24)
        tk.Label(header, text="Register a new vehicle with the authority",
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

        # -------- section: identity --------
        _section_title(body, "VEHICLE IDENTITY")

        self.plate = _text_field(body, "Plate Number *",
                                 placeholder="e.g. BP-1-A1234",
                                 helper="Bhutanese plate format: BP-N-XXXXX")

        # -------- section: registration --------
        _section_title(body, "REGISTRATION DETAILS")

        self.dzongkhag = _dropdown_field(
            body, "Dzongkhag *",
            options=DZONGKHAGS, default="Thimphu",
            helper="Where the taxi is registered")

        self.vehicle = _dropdown_field(
            body, "Vehicle Type *",
            options=VEHICLE_TYPES, default="Maruti Alto",
            helper="Make and model of the vehicle")

        self.date_entry = _text_field(body, "Registration Date *",
                                      placeholder="YYYY-MM-DD",
                                      helper="When the vehicle was first registered")
        self.date_entry.insert(0, str(date.today()))

        self.status = _dropdown_field(
            body, "Status *",
            options=STATUSES, default="Active",
            helper="Active = fully registered · Review = pending approval")

        # -------- section: photo --------
        _section_title(body, "VEHICLE PHOTO (OPTIONAL)")

        photo_row = tk.Frame(body, bg=CARD)
        photo_row.pack(fill="x", pady=(4, 6))

        tk.Button(photo_row, text="📁  Choose photo", bg="white", fg=TEXT,
                  bd=1, relief="solid", font=FONT_NORMAL, padx=14, pady=8,
                  cursor="hand2",
                  command=self._choose_photo).pack(side="left")

        self.photo_label = tk.Label(photo_row, text="No file selected",
                                    bg=CARD, fg=MUTED, font=FONT_SMALL)
        self.photo_label.pack(side="left", padx=12)

        # Preview
        self.preview = tk.Frame(body, bg="#f0f4f8", width=280, height=160,
                                highlightbackground=BORDER, highlightthickness=1)
        self.preview.pack(anchor="w", pady=(6, 0))
        self.preview.pack_propagate(False)
        self.preview_img = tk.Label(self.preview, text="(preview)",
                                    bg="#f0f4f8", fg=MUTED, font=FONT_SMALL)
        self.preview_img.pack(expand=True, fill="both")

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

        # Focus first field
        self.plate.focus_set()

    # ---------- photo ----------
    def _choose_photo(self):
        path = filedialog.askopenfilename(
            title="Choose vehicle photo",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.gif"),
                       ("All files", "*.*")])
        if not path:
            return
        self.photo_path = path
        name = path.split("/")[-1].split("\\")[-1]
        self.photo_label.configure(text=name)
        self._show_preview(path)

    def _show_preview(self, path):
        try:
            from PIL import Image, ImageTk
            img = Image.open(path)
            img.thumbnail((270, 150), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            self.preview_img.configure(image=tk_img, text="")
            self.preview_img.image = tk_img
            self._preview_img = tk_img
        except ImportError:
            self.preview_img.configure(text="(Pillow not installed)", image="")
        except Exception:
            self.preview_img.configure(text="(can't preview)", image="")

    # ---------- save ----------
    def _save(self):
        plate = self.plate.get().strip()
        dzongkhag = self.dzongkhag.get()
        vehicle = self.vehicle.get()
        reg_date = self.date_entry.get().strip()
        status = self.status.get()

        # Validation
        if not plate:
            messagebox.showwarning("Missing info",
                                   "Please enter the plate number.")
            self.plate.focus_set()
            return

        if not reg_date:
            messagebox.showwarning("Missing info",
                                   "Please enter the registration date.")
            self.date_entry.focus_set()
            return

        try:
            datetime.strptime(reg_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Invalid date",
                                   "Registration date must be in YYYY-MM-DD format.")
            self.date_entry.focus_set()
            return

        # Auto-generate Taxi ID
        from storage import get_added
        from data import TAXI_RECORDS
        existing = len(TAXI_RECORDS) + len(get_added("taxi_records"))
        taxi_id = f"TX{existing + 1:03d}"

        record = (taxi_id, plate, dzongkhag, vehicle, reg_date, status)
        self.on_save(record, self.photo_path)
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