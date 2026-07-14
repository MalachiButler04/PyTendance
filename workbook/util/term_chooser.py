import tkinter as tk
from tkinter import Tk, messagebox
import json


class TermChooser:
    def __init__(self, root: Tk, on_complete=None):
        self.root = root
        self.on_complete = on_complete
        self.root.geometry("300x225")

        self.term_entry = tk.StringVar(value=" Select Term ")
        self.days_entry = tk.StringVar(value=" Select Days ")
        self.frame = None

    def build_gui(self):
        terms = ["Fall", "Spring"]
        days = ["Monday, Wednesday", "Tuesday, Thursday"]

        self.frame = tk.Frame(self.root)
        self.frame.place(anchor="center", relx=.5, rely=.5)

        tk.OptionMenu(self.frame, self.term_entry, *terms).pack(padx=5, pady=5)
        tk.OptionMenu(self.frame, self.days_entry, *days).pack(padx=5, pady=5)

        tk.Button(self.frame, text="Submit", command=self.config_info).pack(padx=5, pady=5)

    def config_info(self):
        if self.term_entry.get() == " Select Term " or self.days_entry.get() == " Select Days ":
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
            with open("config/book_config.json", "r") as fr:
                data = json.load(fr)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data["term"] = term
        data["days"] = days

        with open("config/book_config.json", "w") as fw:
            json.dump(data, fw, indent=4)

      
        self.frame.destroy()

        if self.on_complete:
            self.on_complete()


if __name__ == "__main__":
    root = Tk()
    tc = TermChooser(root)
    tc.build_gui()
    root.mainloop()