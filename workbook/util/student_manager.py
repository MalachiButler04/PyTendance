import pandas as pd
import ttkbootstrap as ttk
from tkinter import StringVar, messagebox
import json
from config.path_config import STUDENT_CONFIG, TOTAL_WEEKS, WEEK_SHEET_PREFIX, WORKBOOK_FILENAME
from workbook.util.tabloid import Tabloid

class StudentManager:
    def __init__(self, root: ttk.Window):
        self.root = root
        self.button_frame = None

        self.FRAMES, self.STUDENTS, self.REF, self.COLOR, self.DAYS = self.init_data()

    def build_ui(self) -> ttk.Frame:
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.place(relx=0.5, rely=0.5, anchor="center")
    
        ttk.Button(self.button_frame, text="Add Student", bootstyle="secondary", command=self.add_student).grid(row=0, column=0, padx=5)
        ttk.Button(self.button_frame, text="Remove Student", bootstyle="secondary", command=self.remove_student).grid(row=0, column=1, padx=5)
        
        return self.button_frame
        
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
        from main import Main
        self.button_frame.destroy()
        
        mn = Main(None)
        
        self.root.geometry("300x250")
        self.button_frame.destroy()
        option_frame = ttk.Frame(self.root)
        option_frame.place(relx=.5, rely=.5, anchor="center")

        selected = ttk.StringVar(value="Select Student")

        ops = ["Select Student", *self.STUDENTS]
        ttk.OptionMenu(option_frame, selected, *ops).pack()

        def get_conf():
            if selected.get() != "Select Student":
                conf = messagebox.askokcancel(message=f"Are you sure you would like to remove '{selected.get()}'?")
                if conf:
                    self.remove_helper(selected.get())
                    
                    mn.to_main(option_frame)
    
            else:
                messagebox.showerror(title="Invalid Selection", message="Please select a student to continue!")

        ttk.Button(option_frame, text="Submit", command=get_conf).pack(pady=(5, 0))

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

if __name__ == "__main__":
    root = ttk.Window()
    sm = StudentManager(root)
    root.mainloop()