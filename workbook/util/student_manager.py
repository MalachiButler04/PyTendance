import json
import pandas as pd
import ttkbootstrap as ttk

from tkinter import StringVar, messagebox, filedialog

from config.path_config import (
    STUDENT_CONFIG,
    TOTAL_WEEKS,
    WEEK_SHEET_PREFIX,
    WORKBOOK_FILENAME,
    INFO_CONFIG
)
from workbook.util.tabloid import Tabloid


class StudentManager:
    
    FRAMES = None
    STUDENTS = None
    REF = None
    COLOR = None 
    DAYS = None
    
    def __init__(self, root: ttk.Window):
        self.root = root
        self.button_frame = None
        self.option_frame = None

        self.ref, self.color, _, self.days = Tabloid.load_config()
        self.students = Tabloid.load_students()

        self.FRAMES, self.STUDENTS, self.REF, self.COLOR, self.DAYS = self.init_data()

        StudentManager.FRAMES = self.FRAMES
        StudentManager.STUDENTS = self.STUDENTS
        StudentManager.REF = self.REF
        StudentManager.COLOR = self.COLOR
        StudentManager.DAYS = self.DAYS

    def _clear_frame(self, frame: ttk.Frame | None):
        if frame:
            for widget in frame.winfo_children():
                widget.destroy()

    def _reload_state(self):
        self.ref, self.color, _, self.days = Tabloid.load_config()
        self.students = Tabloid.load_students()
        self.FRAMES, self.STUDENTS, self.REF, self.COLOR, self.DAYS = self.init_data()
        
        tab = Tabloid(skip_init=True)
        tab.rebuild_workbook()


    def add_student(self):
        self.root.geometry("300x200")

        new_ref: str = filedialog.askopenfilename(
            title="Upload New Photo Roster",
            filetypes=[("CSV Files", "*.csv")]
        )

        if not new_ref:
            return

        try:
            temp_df = pd.read_csv(new_ref)

            if "Sortable name" not in temp_df.columns:
                messagebox.showerror(
                    title="Processing Error",
                    message="The selected file does not contain a 'Sortable name' column."
                )
                return

            temp_students = temp_df["Sortable name"].dropna().astype(str)
            normalized_existing = {stud.title() for stud in self.students}
            normalized_new = [stud.title() for stud in temp_students]

            unique_new_students = [
                stud for stud in normalized_new
                if stud not in normalized_existing and stud != "Lu, Lingma"
            ]

            if not unique_new_students:
                messagebox.showerror(
                    title="Processing Error",
                    message=(
                        "It appears the uploaded Photo Roster contains no new students! "
                        "Please reupload and try again!"
                    )
                )
                return

            merged_students = sorted({*self.students, *unique_new_students})
            self.students = merged_students
            self.STUDENTS = merged_students

            with open(STUDENT_CONFIG, "r") as fr:
                data = json.load(fr)

            data["students"] = merged_students

            with open(STUDENT_CONFIG, "w") as fw:
                json.dump(data, fw, indent=4)

            self._reload_state()

            messagebox.showinfo(
                title="Success!",
                message="Student roster updated successfully."
            )
            
            with open(INFO_CONFIG, "r") as fr:
                data = json.load(fr)
                data["ref"] = new_ref
            
            with open(INFO_CONFIG, "w") as fw:
                json.dump(data, fw, indent=4)

        except KeyError as e:
            print(e)
            
        except Exception as e:
            messagebox.showerror(
                title="Processing Error",
                message=f"Could not process the uploaded CSV:\n{e}"
            )

    def init_data(self):
        if self.students and all((self.ref, self.color, self.days)):
            data_frames = [
                pd.read_excel(WORKBOOK_FILENAME, sheet_name=f"{WEEK_SHEET_PREFIX}{i}")
                for i in range(1, TOTAL_WEEKS + 1)
            ]

            lecture0 = f"{self.days[0]} Lecture"
            lab0 = f"{self.days[0]} Lab"
            lecture1 = f"{self.days[1]} Lecture"

            self._data_frames = data_frames
            self._lecture0 = lecture0
            self._lab0 = lab0
            self._lecture1 = lecture1

            frames = {}
            for index, frame in enumerate(data_frames, start=1):
                frames[f"{WEEK_SHEET_PREFIX}{index}"] = frame[["Names", lecture0, lab0, lecture1]]

            return frames, self.students, self.ref, self.color, self.days

        return None, None, None, None, None

    def remove_student(self):
        self.root.geometry("300x250")

        if self.button_frame:
            self._clear_frame(self.button_frame)

        if self.option_frame:
            self.option_frame.destroy()
            self.option_frame = None

        self.option_frame = ttk.Frame(self.root)
        self.option_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.build_student_dropdown(self.option_frame)


    def build_student_dropdown(self, parent_frame: ttk.Frame):
        selected = StringVar(value="Select Student")

        ops = ["Select Student", *self.STUDENTS]
        option_menu = ttk.OptionMenu(parent_frame, selected, ops[0], *ops[1:])
        option_menu.pack(pady=5)

        def get_conf():
            current = selected.get()

            if current == "Select Student":
                messagebox.showerror(
                    title="Invalid Selection",
                    message="Please select a student to continue!"
                )
                return

            conf = messagebox.askokcancel(
                message=f"Are you sure you would like to remove '{current}'?"
            )
            if not conf:
                return

            student_to_remove = current

            if self.option_frame:
                self.option_frame.destroy()
                self.option_frame = None

            self.remove_helper(student_to_remove)

            messagebox.showinfo(
                title="Success!",
                message=f"'{student_to_remove}' has been removed successfully!"
            )

            exit_prompt = messagebox.askyesno(
                title="Success!",
                message="Would you like to exit?"
            )

            if exit_prompt:
                self.root.destroy()
            else:
                self.back_to_edit()

        ttk.Button(
            parent_frame,
            text="Submit",
            bootstyle="danger",
            command=get_conf
        ).pack(pady=(5, 0))

        ttk.Button(
            parent_frame,
            text="Back",
            bootstyle="secondary",
            command=lambda: self.back_to_edit()
        ).pack(pady=(5, 0))


    def back_to_edit(self):
        if self.option_frame:
            self.option_frame.destroy()
            self.option_frame = None

        if self.button_frame:
            self._clear_frame(self.button_frame)
        else:
            self.button_frame = ttk.Frame(self.root)
            self.button_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.root.geometry("300x200")

        ttk.Button(
            self.button_frame,
            text="Add Student",
            bootstyle="secondary",
            command=self.add_student
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            self.button_frame,
            text="Remove Student",
            bootstyle="secondary",
            command=self.remove_student
        ).grid(row=0, column=1, padx=5)


    def refresh_dropdown(self, option_menu: ttk.OptionMenu, selected: StringVar):
        menu = option_menu["menu"]
        menu.delete(0, "end")
        for student in self.STUDENTS:
            menu.add_command(label=student, command=lambda s=student: selected.set(s))


    def remove_helper(self, student: str):
        if student in self.STUDENTS:
            self.STUDENTS.remove(student)

        self.students = list(self.STUDENTS)

        for frame in self._data_frames:
            frame.drop(frame[frame["Names"] == student].index, inplace=True)

        self.FRAMES = StudentManager.FRAMES = {
            f"{WEEK_SHEET_PREFIX}{i}": df[["Names", self._lecture0, self._lab0, self._lecture1]]
            for i, df in enumerate(self._data_frames, start=1)
        }

        with open(STUDENT_CONFIG, "r") as sr:
            data = json.load(sr)
            data["students"] = self.STUDENTS

        with open(STUDENT_CONFIG, "w") as sw:
            json.dump(data, sw, indent=4)

        tab = Tabloid(skip_init=True)
        tab.rebuild_workbook()

        self._reload_state()