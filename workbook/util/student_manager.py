import json

import pandas as pd
import ttkbootstrap as ttk
from tkinter import StringVar, messagebox

from config.path_config import STUDENT_CONFIG, TOTAL_WEEKS, WEEK_SHEET_PREFIX, WORKBOOK_FILENAME
from workbook.util.tabloid import Tabloid

class StudentManager:
    def __init__(self, root: ttk.Window):
        self.root = root
        self.button_frame = None
        self.current_frame = None

        self.FRAMES, self.STUDENTS, self.REF, self.COLOR, self.DAYS = self.init_data()

    def build_ui(self) -> ttk.Frame:
        self.current_page(to_main=True)
        return self.button_frame

    def clear_frame(self) -> None:
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def current_page(self, frame: ttk.Frame | None = None, to_main: bool = False) -> None:
        self.clear_frame()

        if to_main:
            self.current_frame = self.main_frame()
        elif frame is not None:
            self.current_frame = frame
        else:
            return

        self.button_frame = self.current_frame

    def main_frame(self) -> ttk.Frame:
        frame = ttk.Frame(self.root)
        ttk.Label(frame, text="Student Manager", bootstyle="primary-inverse", font=("Helvetica", 15)).pack(pady=(20, 10))

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Student", bootstyle="secondary", command=self.add_student).pack(pady=5)
        ttk.Button(button_frame, text="Remove Student", bootstyle="secondary", command=self.remove_student).pack(pady=5)

        return frame

    def to_main(self) -> None:
        self.current_page(to_main=True)

    def add_student(self) -> None:
        wrapper = ttk.Frame(self.root)
        self.current_page(wrapper)

        ttk.Label(wrapper, text="Add Student", bootstyle="primary-inverse", font=("Helvetica", 15)).pack(pady=(20, 10))

        name_var = StringVar()
        form_frame = ttk.Frame(wrapper)
        form_frame.pack(pady=10)

        ttk.Entry(form_frame, textvariable=name_var).pack(pady=5)
        ttk.Button(form_frame, text="Submit", bootstyle="secondary", command=lambda: self.confirm_add(name_var.get())).pack(pady=5)
        ttk.Button(form_frame, text="Back", bootstyle="secondary", command=self.to_main).pack(pady=5)

    def confirm_add(self, name: str) -> None:
        student_name = name.strip()
        if not student_name:
            messagebox.showwarning("Missing name", "Please enter a student name before continuing.")
            return

        messagebox.showinfo("Student added", f"{student_name} was added to the roster.")
        self.to_main()

    def init_data(self):
        ref, color, _, days = Tabloid.load_config()
        students = Tabloid.load_students()

        if students and ref and color and days:
            data_frames = [
                pd.read_excel(WORKBOOK_FILENAME, sheet_name=f"{WEEK_SHEET_PREFIX}{i}")
                for i in range(1, TOTAL_WEEKS + 1)
            ]

            lecture0 = f"{days[0]} Lecture"
            lab0 = f"{days[0]} Lab"
            lecture1 = f"{days[1]} Lecture"

            self._data_frames = data_frames
            self._lecture0 = lecture0
            self._lab0 = lab0
            self._lecture1 = lecture1

            frames = {}
            for index, frame in enumerate(data_frames, start=1):
                frames[f"{WEEK_SHEET_PREFIX}{index}"] = frame[["Names", lecture0, lab0, lecture1]]

            return frames, students, ref, color, days

        return None, None, None, None, None
    
    def remove_student(self):
        self.root.geometry("300x250")
        self.button_frame.destroy()
        option_frame = ttk.Frame(self.root)
        self.current_page(option_frame)

        selected = StringVar(value="Select Student")

        ttk.Label(option_frame, text="Remove Student", bootstyle="primary-inverse", font=("Helvetica", 15)).pack(pady=(20, 10))

        ops = ["Select Student", *self.STUDENTS]
        ttk.OptionMenu(option_frame, selected, *ops).pack(pady=10)

        def get_conf():
            conf = messagebox.askokcancel(message=f"Are you sure you would like to remove '{selected.get()}'?")
            if conf:
                self.remove_helper(selected.get())
            return

        student = selected.get()

        if student not in self.STUDENTS:
            return

        self.STUDENTS.remove(student)

        for frame in self._data_frames:
            frame.drop(frame[frame["Names"] == student].index, inplace=True)

        StudentManager.FRAMES = {
            f"{WEEK_SHEET_PREFIX}{i}": df[["Names", self._lecture0, self._lab0, self._lecture1]]
            for i, df in enumerate(self._data_frames, start=1)
        }
        self.FRAMES = StudentManager.FRAMES

        with open(STUDENT_CONFIG, "r") as sr:
            data = json.load(sr)
            data["students"] = self.STUDENTS

        with open(STUDENT_CONFIG, "w") as sw:
            json.dump(data, sw, indent=4)

        tab = Tabloid(skip_init=True)
        tab.rebuild_workbook()
        self.to_main()

if __name__ == "__main__":
    root = ttk.Window()
    sm = StudentManager(root)
    root.mainloop()