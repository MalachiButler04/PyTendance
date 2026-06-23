import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class StudentManager:
    def __init__(self, root: ttk.Window):
        self.root = root

        root.geometry("400x300")
        root.resizable(False, False)
        root.title("PyTendance: Student Manager")
        root.eval("tk::PlaceWindow . center")

        self.current_frame = None
        self.current_page(to_main=True)

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def current_page(self, frame: ttk.Frame = None, to_main: bool = False) -> None:

        if to_main:
            self.clear_frame()
            self.current_frame = self.main_frame()
            self.current_frame.pack(fill=BOTH, expand=True)
            return

        if frame:
            self.clear_frame()
            self.current_frame = frame
            frame.pack(fill=BOTH, expand=True)

    def main_frame(self) -> ttk.Frame:
        main_wrapper = ttk.Frame(self.root)

        header_label = ttk.Label(
            main_wrapper,
            text="Student Manager",
            padding=10,
            bootstyle="Inverse.primary",
            font=("Helvetica", 15)
        )
        header_label.place(relx=.5, rely=.25, anchor=CENTER)

        button_style = {
            "bootstyle": SECONDARY,
            "padding": 5,
        }

        button_frame = ttk.Frame(
            main_wrapper,
            relief=SUNKEN,
            padding=10
        )
        button_frame.place(relx=.5, rely=.6, anchor=CENTER)

        ttk.Button(
            button_frame,
            text="Add Student",
            command=self.add_student,
            **button_style
        ).pack(pady=5)

        ttk.Button(
            button_frame,
            text="Remove Student",
            command=self.remove_student,
            **button_style
        ).pack(pady=5)

        ttk.Button(
            button_frame, 
            text="Back",
            **button_style
        ).pack(pady=5)

        return main_wrapper

    def add_student(self):
        wrapper = ttk.Frame(self.root)
        self.current_page(wrapper)

        ttk.Label(
            wrapper,
            text="Add Student",
            padding=10,
            bootstyle="Inverse.primary",
            font=("Helvetica", 15)
        ).place(relx=.5, rely=.25, anchor=CENTER)

        name = ttk.StringVar()

        name_frame = ttk.Frame(wrapper, relief=SUNKEN, padding=10)
        name_frame.place(relx=.5, rely=.6, anchor=CENTER)

        name_entry = ttk.Entry(
            name_frame,
            textvariable=name,
            bootstyle=SECONDARY
        )
        name_entry.pack(pady=5)

        submit_button = ttk.Button(
            name_frame,
            text="Submit",
            bootstyle=SECONDARY,
            command=lambda: self.confirm_add(name.get())
        )
        submit_button.pack(pady=5)

        back_button = ttk.Button(
            name_frame,
            text="Back",
            bootstyle=SECONDARY,
            command=lambda: self.back()
        )
        back_button.pack(pady=5)
        
        submit_button.config(state="disabled")

        def validate(*args):
            if name.get().strip():
                submit_button.config(state="normal")
            else:
                submit_button.config(state="disabled")

        name.trace_add("write", validate)

    def back(self):
        choice = messagebox.askokcancel(
            message="Are you sure?",
            icon=messagebox.WARNING
        )
        if choice:
            messagebox.showinfo(
                message="Back to main menu...",
                icon=messagebox.INFO
            )
            self.current_page(to_main=True)

    def confirm_add(self, name: str) -> None:
        if name:
            choice = messagebox.askokcancel(
                title="Confirm",
                message=f"Would you like to confirm '{name}'?",
                icon=messagebox.QUESTION
            )
            if choice:
                messagebox.showinfo(
                    message=f"{name} confirmed! Back to main menu...",
                    icon=messagebox.INFO
                )
                self.current_page(to_main=True)

    def remove_student(self):
        wrapper = ttk.Frame(self.root)
        self.current_page(wrapper)

if __name__ == "__main__":
    pass