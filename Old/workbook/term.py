from tkinter import Tk
import tkinter as tk
from tkinter import messagebox

class TermChooser:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x450")
        self.root.eval("tk::PlaceWindow . center")
        self.root.title("Choose Term")

        self.term = ["Fall", "Spring"]
        self.days = ["Monday, Wednesday", "Tuesday, Thursday"]

        self.getSemesterInfo()

    def getSemesterInfo(self):
        wrapper = tk.Frame(self.root, padx=5, pady=150)
        wrapper.pack()

        term_label_frame = tk.Frame(wrapper, padx=5, pady=5)
        term_label_frame.pack()

        label_term = tk.Label(term_label_frame, text="Term")
        label_term.pack()

        self.selected_term = tk.StringVar(wrapper, self.term[0])
        opt_men_term = tk.OptionMenu(term_label_frame, self.selected_term, *self.term)
        opt_men_term.pack()

        days_label_frame = tk.Frame(wrapper, padx=5, pady=5)
        days_label_frame.pack()

        label_days = tk.Label(days_label_frame, text="Days")
        label_days.pack()

        self.selected_days = tk.StringVar(wrapper, self.days[0])
        opt_men_days = tk.OptionMenu(days_label_frame, self.selected_days, *self.days)
        opt_men_days.pack()

        submit_button = tk.Button(wrapper, text="Submit", command=self.conf)
        submit_button.pack()

    def conf(self):
        choice = messagebox.askyesno(
            title="Confirm",
            message=f"Confirm | Days: {self.selected_days.get()} | Term: {self.selected_term.get()}",
            icon=messagebox.QUESTION
        )
        if choice:
            import json

            with open("config.json", "r") as jr:
                data = json.load(jr)

                data["term"] = self.selected_term.get()
                data["days"] = self.selected_days.get().split(", ")
            
            with open("config.json", "w") as jw:
                json.dump(data, jw, indent=4)

            self.root.destroy()

root = Tk()
TermChooser(root)
root.mainloop()