# main.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import messagebox

from theme import BG
from sidebar import Sidebar, Header
from pages import (login, dashboard, taxi_records, trip_records,
                   driver_profiles, analysis, visualization, parking_zones,
                   account_details, system_preferences)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogay Jogay - Bhutan Transport Authority")
        self.root.geometry("1280x780")
        self.root.minsize(1100, 650)
        self.root.configure(bg=BG)

        self.root._jogay_app = self

        self.routes = {
            "Dashboard":          dashboard.build,
            "Taxi Records":       taxi_records.build,
            "Trip Records":       trip_records.build,
            "Driver Profiles":    driver_profiles.build,
            "Analysis":           analysis.build,
            "Visualization":      visualization.build,
            "Parking Zones":      parking_zones.build,
            "Account details":    account_details.build,
            "System preferences": system_preferences.build,
        }

        self.pending_driver = None

        self.show_login()

    def show_login(self):
        login.build(self.root, on_success=self.build_main)

    def logout(self):
        answer = messagebox.askyesno(
            "Log out",
            "Are you sure you want to log out?"
        )
        if answer:
            self.show_login()

    def build_main(self):
        for w in self.root.winfo_children():
            w.destroy()

        self.sidebar = Sidebar(self.root,
                               on_navigate=self.navigate,
                               on_logout=self.logout)

        right = tk.Frame(self.root, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        self.header = Header(right,
                             initial_title="Dashboard",
                             on_logout=self.logout)

        self.content = tk.Frame(right, bg=BG)
        self.content.pack(fill="both", expand=True)

        self.navigate("Dashboard")

    def navigate(self, name, driver_name=None):
        self.pending_driver = driver_name
        for w in self.content.winfo_children():
            w.destroy()
        self.header.set_title(name)
        self.sidebar.set_active(name)

        if name == "Driver Profiles":
            self.routes[name](self.content, pending_driver=self.pending_driver)
        else:
            self.routes[name](self.content)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()