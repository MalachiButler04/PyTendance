import pandas as pd
import ttkbootstrap as ttk
from tkinter import StringVar, messagebox
import json
from config.path_config import STUDENT_CONFIG, TOTAL_WEEKS, WEEK_SHEET_PREFIX, WORKBOOK_FILENAME
from workbook.util.tabloid import Tabloid
from main import main_menu

class StudentManager:

    def __init__(self, root: ttk.Window):
        self.root = root
        self.button_frame = None

        self.FRAMES, self.STUDENTS, self.REF, self.COLOR, self.DAYS = self.init_data()
        
        self.option_frame = None
        
    def add_student(self) -> ttk.Frame:
        ...

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
        if self.button_frame:
            self.button_frame.destroy()

        self.root.geometry("300x250")

        self.option_frame = ttk.Frame(self.root)
        self.option_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.build_student_dropdown(self.option_frame)

    def build_student_dropdown(self, parent_frame: ttk.Frame):
        selected = StringVar(value="Select Student")  # StringVar from tkinter

        ops = ["Select Student", *self.STUDENTS]
        option_menu = ttk.OptionMenu(parent_frame, selected, *ops)
        option_menu.pack(pady=5)

        def get_conf():
            if selected.get() != "Select Student":
                conf = messagebox.askokcancel(
                    message=f"Are you sure you would like to remove '{selected.get()}'?"
                )
                if conf:
                    self.remove_helper(selected.get())
                    self.STUDENTS = Tabloid.load_students() 
                    self.refresh_dropdown(option_menu, selected)
                    exit = messagebox.askyesno(title="Success!", message=f"'{selected.get()}' has been removed successfully! Would you like to exit?")
                    if exit:
                        self.root.destroy()

                    selected.set("Select Student")
            else:
                messagebox.showerror(
                    title="Invalid Selection",
                    message="Please select a student to continue!"
                )

        ttk.Button(parent_frame, text="Submit", bootstyle="danger", command=get_conf).pack(pady=(5, 0))
        ttk.Button(parent_frame, text="Back", bootstyle="secondary", command=lambda: self.back_to_edit(self.option_frame)).pack(pady=(5, 0))
        
    def back_to_edit(self, prev: ttk.Frame):
        prev.destroy()
        self.root.geometry("300x200")
        self.button_frame = ttk.Frame(self.root)
                    
        self.button_frame.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Button(self.button_frame, text="Add Student", bootstyle="secondary", command=self.add_student).grid(row=0, column=0, padx=5)
        ttk.Button(self.button_frame, text="Remove Student", bootstyle="secondary", command=self.remove_student).grid(row=0, column=1, padx=5)
        
         
    def refresh_dropdown(self, option_menu: ttk.OptionMenu, selected: StringVar):
        menu = option_menu["menu"]
        menu.delete(0, "end")
        for student in self.STUDENTS:
            menu.add_command(label=student, command=lambda s=student: selected.set(s))
    
    def remove_helper(self, student: str):
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