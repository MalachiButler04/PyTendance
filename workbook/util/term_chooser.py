import ttkbootstrap as ttk
from tkinter import messagebox
import json

from config.path_config import INFO_CONFIG

DEFAULT_TERM_VALUE = " Select Term "
DEFAULT_DAYS_VALUE = " Select Days "
TERM_OPTIONS = (DEFAULT_TERM_VALUE, "Fall", "Spring")
DAY_OPTIONS = (DEFAULT_DAYS_VALUE, "Monday, Wednesday", "Tuesday, Thursday")

class TermChooser:
    def __init__(self, root: ttk.Window, on_complete=None):
        self.root = root
        self.on_complete = on_complete

        self.term_entry = ttk.StringVar(value=DEFAULT_TERM_VALUE)
        self.days_entry = ttk.StringVar(value=DEFAULT_DAYS_VALUE)
        self.frame = None

    def build_gui(self):
        self.frame = ttk.Frame(self.root)
        self.frame.place(anchor="center", relx=.5, rely=.5)

        ttk.OptionMenu(self.frame, self.term_entry, *TERM_OPTIONS).pack(padx=10, pady=8)
        ttk.OptionMenu(self.frame, self.days_entry, *DAY_OPTIONS).pack(padx=10, pady=8)

        ttk.Button(self.frame, text="Submit", command=self.config_info, bootstyle="secondary").pack(padx=10, pady=8)

    def config_info(self):
        if self.term_entry.get() == DEFAULT_TERM_VALUE or self.days_entry.get() == DEFAULT_DAYS_VALUE:
            messagebox.showerror(title="Invalid Option", message="Please select valid days and term")
            return

        choice = messagebox.askyesno(
            title="Confirm",
            message=f"Term: '{self.term_entry.get()}' | Days: '{self.days_entry.get()}'"
        )
        if not choice:
            return

        term: str = self.term_entry.get()
        days: list = self.days_entry.get().split(", ")

        try:
            with open(INFO_CONFIG, "r") as fr:
                data = json.load(fr)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data["term"] = term
        data["days"] = days

        with open(INFO_CONFIG, "w") as fw:
            json.dump(data, fw, indent=4)

      
        self.frame.destroy()

        if self.on_complete:
            self.on_complete()