import json
import pandas as pd
import ttkbootstrap as ttk

from tkinter import StringVar, messagebox, filedialog
from pathlib import Path

from main import wb_closed

from config.path_config import (
    STUDENT_CONFIG,
    TOTAL_WEEKS,
    WEEK_SHEET_PREFIX,
    INFO_CONFIG
)

from workbook.util.tabloid import (
    Tabloid,
    load_config,
    load_students,
)

def resolve_workbook_path() -> str:
    _, _, _, _, _, book_name, book_ref = load_config()

    if book_ref and book_name:
        return str(Path(book_ref) / book_name)
    
class StudentManager:

    FRAMES = None
    STUDENTS = None
    REF = None
    COLOR = None
    DAYS = None
    TA = None

    def __init__(self, root: ttk.Window):
        self.root = root

        self.button_frame = None
        self.option_frame = None

        self._data_frames = []
        self._lecture0 = None
        self._lab0 = None
        self._lecture1 = None

        self.ref, self.color, _, self.days, self.TA, _, _ = load_config()

        self.students = self._load_students()
        (
            self.FRAMES,
            self.STUDENTS,
            self.REF,
            self.COLOR,
            self.DAYS,
        ) = self.init_data()

        self._sync_class_state()

    def _sync_class_state(self):
        """Keep class-level state synchronized with this instance."""
        StudentManager.FRAMES = self.FRAMES
        StudentManager.STUDENTS = self.STUDENTS
        StudentManager.REF = self.REF
        StudentManager.COLOR = self.COLOR
        StudentManager.DAYS = self.DAYS
        StudentManager.TA = self.TA

    def _load_students(self):
      
        loaded_students = load_students()

        students = list(loaded_students)

        if self.TA in students:
            students.remove(self.TA)

        return students

    def _save_students(self):
        with open(STUDENT_CONFIG, "r", encoding="utf-8") as sr:
            data = json.load(sr)

        stored = data.get("students", [])
        updated = list(self.students)

        if self.TA and self.TA in stored and self.TA not in updated:
            updated = sorted([*updated, self.TA])

        data["students"] = updated

        with open(STUDENT_CONFIG, "w", encoding="utf-8") as sw:
            json.dump(data, sw, indent=4)

    def _save_roster_reference(self, roster_path):
        with open(INFO_CONFIG, "r", encoding="utf-8") as fr:
            data = json.load(fr)

        data["ref"] = roster_path

        with open(INFO_CONFIG, "w", encoding="utf-8") as fw:
            json.dump(data, fw, indent=4)

    def _clear_frame(self, frame: ttk.Frame | None):
        if frame is None:
            return

        for widget in frame.winfo_children():
            widget.destroy()


    def _reload_state(self):

        (
            self.ref,
            self.color,
            _,
            self.days,
            self.TA,
            _,
            _
        ) = load_config()

        self.students = self._load_students()

        (
            self.FRAMES,
            self.STUDENTS,
            self.REF,
            self.COLOR,
            self.DAYS,
        ) = self.init_data()

        self._sync_class_state()

    def add_student(self):
        if not wb_closed():
            return

        new_ref = filedialog.askopenfilename(
            title="Upload New Photo Roster",
            filetypes=[("CSV Files", "*.csv")],
        )

        if not new_ref:
            return

        try:
            temp_df = pd.read_csv(new_ref)

            if "Sortable name" not in temp_df.columns:
                messagebox.showerror(
                    title="Processing Error",
                    message=(
                        "The selected file does not contain a "
                        "'Sortable name' column."
                    ),
                )
                return

            temp_students = (
                temp_df["Sortable name"]
                .dropna()
                .astype(str)
                .str.strip()
            )

            normalized_new = [
                student.title()
                for student in temp_students
                if student
            ]

            normalized_existing = {
                student.title()
                for student in self.students
            }

            excluded_students = {
                "Lu, Lingma",
                self.TA,
            }

            unique_new_students = [
                student
                for student in normalized_new
                if student not in normalized_existing
                and student not in excluded_students
            ]

            if not unique_new_students:
                messagebox.showerror(
                    title="Processing Error",
                    message=(
                        "It appears the uploaded Photo Roster contains "
                        "no new students! Please reupload and try again!"
                    ),
                )
                return

            merged_students = sorted(
                set(self.students).union(unique_new_students)
            )

            self.students = merged_students
            self.STUDENTS = list(merged_students)

            self._sync_class_state()

            self._save_students()

            self._save_roster_reference(new_ref)

            try:
                tab = Tabloid(skip_init=True)
                tab.rebuild_workbook()

            except Exception as exc:
                messagebox.showerror(
                    title="Processing Error",
                    message=(
                        f"The roster was saved, but the workbook could "
                        f"not be rebuilt:\n{exc}"
                    ),
                )
                return

            self._reload_state()

            messagebox.showinfo(
                title="Success!",
                message="Student roster updated successfully.",
            )

        except pd.errors.EmptyDataError:
            messagebox.showerror(
                title="Processing Error",
                message="The selected CSV file is empty.",
            )

        except pd.errors.ParserError as exc:
            messagebox.showerror(
                title="Processing Error",
                message=f"Could not read the CSV file:\n{exc}",
            )

    def init_data(self):

        if not self.students:
            return None, None, None, None, None

        if not self.ref or not self.color or not self.days:
            return None, None, None, None, None

        if len(self.days) < 2:
            return None, None, None, None, None

        data_frames = []

        for week_number in range(1, TOTAL_WEEKS + 1):
            sheet_name = (
                f"{WEEK_SHEET_PREFIX}{week_number}"
            )

            frame = pd.read_excel(
                resolve_workbook_path(),
                sheet_name=sheet_name,
            )

            data_frames.append(frame)

        lecture0 = f"{self.days[0]} Lecture"
        lab0 = f"{self.days[0]} Lab"
        lecture1 = f"{self.days[1]} Lecture"

        required_columns = [
            "Names",
            lecture0,
            lab0,
            lecture1,
        ]

        for index, frame in enumerate(data_frames, start=1):
            missing_columns = [
                column
                for column in required_columns
                if column not in frame.columns
            ]

            if missing_columns:
                raise KeyError(
                    f"Week {index} is missing required columns: "
                    f"{missing_columns}"
                )

        self._data_frames = data_frames
        self._lecture0 = lecture0
        self._lab0 = lab0
        self._lecture1 = lecture1

        frames = {
            f"{WEEK_SHEET_PREFIX}{index}": frame[required_columns].copy()
            for index, frame in enumerate(data_frames, start=1)
        }

        return (
            frames,
            list(self.students),
            self.ref,
            self.color,
            self.days,
        )

    def remove_student(self):
        if not wb_closed():
            return

        self.root.geometry("300x250")

        if self.button_frame:
            self._clear_frame(self.button_frame)

        if self.option_frame:
            self.option_frame.destroy()
            self.option_frame = None

        self.option_frame = ttk.Frame(self.button_frame.master)
        self.option_frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

        self.build_student_dropdown(self.option_frame)

    def build_student_dropdown(self, parent_frame: ttk.Frame):
        selected = StringVar(value="Select Student")

        ops = [
            "Select Student",
            *self.STUDENTS,
        ]

        option_menu = ttk.OptionMenu(
            parent_frame,
            selected,
            ops[0],
            *ops[1:],
        )

        option_menu.pack(pady=5)

        def get_conf():
            current = selected.get()

            if current == "Select Student":
                messagebox.showerror(
                    title="Invalid Selection",
                    message="Please select a student to continue!",
                )
                return

            conf = messagebox.askokcancel(
                title="Confirm Removal",
                message=(
                    f"Are you sure you would like to remove "
                    f"'{current}'?"
                ),
            )

            if not conf:
                return

            if current not in self.STUDENTS:
                messagebox.showerror(
                    title="Processing Error",
                    message=(
                        f"'{current}' could not be found in the "
                        "current student roster."
                    ),
                )
                return

            if self.option_frame:
                self.option_frame.destroy()
                self.option_frame = None

            try:
                self.remove_helper(current)

            except Exception as exc:
                messagebox.showerror(
                    title="Processing Error",
                    message=(
                        f"Could not remove '{current}':\n{exc}"
                    ),
                )
                return

            messagebox.showinfo(
                title="Success!",
                message=(
                    f"'{current}' has been removed successfully!"
                ),
            )

            exit_prompt = messagebox.askyesno(
                title="Success!",
                message="Would you like to exit?",
            )

            if exit_prompt:
                self.root.destroy()
            else:
                self.back_to_edit()

        ttk.Button(
            parent_frame,
            text="Submit",
            bootstyle="danger",
            command=get_conf,
        ).pack(pady=(5, 0))

        ttk.Button(
            parent_frame,
            text="Back",
            bootstyle="secondary",
            command=self.back_to_edit,
        ).pack(pady=(5, 0))

    def back_to_edit(self):
        if self.option_frame:
            self.option_frame.destroy()
            self.option_frame = None

        if self.button_frame:
            self._clear_frame(self.button_frame)
        else:
            self.button_frame = ttk.Frame(self.root)
            self.button_frame.place(
                relx=0.5,
                rely=0.5,
                anchor="center",
            )
            
        ttk.Button(
            self.button_frame,
            text="Add Student",
            bootstyle="secondary",
            command=self.add_student,
        ).pack(pady=10)

        ttk.Button(
            self.button_frame,
            text="Remove Student",
            bootstyle="secondary",
            command=self.remove_student,
        ).pack(pady=10)


    def refresh_dropdown(
        self,
        option_menu: ttk.OptionMenu,
        selected: StringVar,
    ):
        menu = option_menu["menu"]

        menu.delete(0, "end")

        for student in self.STUDENTS:
            menu.add_command(
                label=student,
                command=lambda s=student: selected.set(s),
            )


    def remove_helper(self, student: str):
        if student not in self.STUDENTS:
            raise ValueError(
                f"Student '{student}' is not in the roster."
            )

        updated_students = [
            existing
            for existing in self.STUDENTS
            if existing != student
        ]

        self.students = updated_students
        self.STUDENTS = updated_students

        for frame in self._data_frames:
            matching_rows = frame.index[
                frame["Names"] == student
            ]

            if len(matching_rows) > 0:
                frame.drop(
                    matching_rows,
                    inplace=True,
                )

        required_columns = [
            "Names",
            self._lecture0,
            self._lab0,
            self._lecture1,
        ]

        self.FRAMES = {
            f"{WEEK_SHEET_PREFIX}{index}": frame[
                required_columns
            ].copy()
            for index, frame in enumerate(
                self._data_frames,
                start=1,
            )
        }

        self._sync_class_state()

        self._save_students()

        tab = Tabloid(skip_init=True)
        tab.rebuild_workbook()

        self._reload_state()