import os
import json
import pandas as pd
import ttkbootstrap as ttk

from pathlib import Path
from tkinter import filedialog, messagebox
from workbook.util.color_chooser import ColorPicker
from workbook.util.term_chooser import TermChooser
from workbook.util.tabloid import Tabloid, load_students, load_config, resolve_workbook_path
from config.path_config import INFO_CONFIG, STUDENT_CONFIG, BASE_DIR, WORKBOOK_FILENAME

def get_name(): 
    with open(INFO_CONFIG, "r") as fr:
        reader = json.load(fr)

        return str(reader["TA"])
    
class Main:
    root = None
    instance = None

    def __init__(self, root: ttk.Window | None):
        self.root = root
        self.button_frame = None
        self.manager_frame = None
        self.ref = None
        self.valid_csv = False
        self.cp = None
        self.tc = None
        self.old_workbook_path = None

        if root:
            Main.root = root
            Main.instance = self
            self.init_main(self.root)

            self.property_label = ttk.Label(
                    self.root,
                    text="Malachi A. Butler and Jacob T. Imbus",
                    font=("Aptos", 5),
                )

            self.ta = get_name()

            self.property_label.place(anchor="s", relx=.5, rely=.97)

            ttk.Label(
                root,
                text="  PyTendance",
                font=("Helvetica", 15, "bold"),
                bootstyle="primary-inverse",
                ).pack(pady=(15, 10), ipadx=5, ipady=5)

    def _clear_button_frame(self):
        if self.button_frame is not None:
            self.button_frame.destroy()
            self.button_frame = None

    def init_main(self, root):
        root.title("PyTendance")
        root.geometry("300x200")
        root.eval("tk::PlaceWindow . center")
        root.resizable(False, False)

        icon = ttk.PhotoImage(file=str(BASE_DIR / "assets" / "492snake_100855.png"))
        root.iconphoto(True, icon)

        self._clear_button_frame()
        self.button_frame = ttk.Frame(root)
        self.button_frame.place(anchor="center", relx=.5, rely=.55)

        ttk.Button(
            self.button_frame,
            text="New Worksheet",
            bootstyle="secondary",
            command=self.init_workbook,
            width=15,
        ).pack(pady=5)

        ttk.Button(
            self.button_frame,
            text="Edit Worksheet",
            bootstyle="secondary",
            command=self.init_student_manager,
            width=15,
        ).pack(pady=5)

    def init_student_manager(self):
        from workbook.util.student_manager import StudentManager

        exists = os.path.exists(resolve_workbook_path())

        if not wb_closed():
            return
            
        if exists and all(load_config()) and load_students():
            sm = StudentManager(self.root)

            self._clear_button_frame()
            self.button_frame = ttk.Frame(self.root)
            sm.button_frame = self.button_frame
            self.button_frame.place(relx=0.5, rely=0.5, anchor="center")

            ttk.Button(
                self.button_frame,
                text="Add Student",
                bootstyle="secondary",
                command=sm.add_student,
            ).grid(row=0, column=0, padx=5)

            ttk.Button(
                self.button_frame,
                text="Remove Student",
                bootstyle="secondary",
                command=sm.remove_student,
            ).grid(row=0, column=1, padx=5)

        else:
            messagebox.showerror(
                title="No Workbook Data Found",
                message=(
                    "There was an error while loading your attendance sheet data. "
                    "Please try again or press 'New Workbook'"
                ),
            )

    def refresh_student_manager(self):
        self.init_student_manager()

    def init_workbook(self) -> None:
        
        warning = messagebox.askokcancel(
            title="Warning",
            message="Any old data will be erased. Continue?",
            icon="warning",
        )
            
        if warning:
            self.valid_csv = False

            _, _, _, _, _, old_book_name, old_book_ref = load_config()
            self.old_workbook_path = (
                str(Path(old_book_ref) / old_book_name)
                if old_book_ref and old_book_name
                else None
            )

            self.reset_json()

            has_uploaded = self.upload_roster()

            if self.has_ref() and self.valid_csv and has_uploaded:
                self.root.protocol("WM_DELETE_WINDOW", self.on_exit_create)
                self._clear_button_frame()
                
                if self.has_name():
                    self.init_colorpicker()
                else:
                    self.init_get_name(self.init_colorpicker)
                    

    def init_colorpicker(self) -> None:
        if self.valid_csv:
            self.cp = ColorPicker(self.root, on_complete=self.init_termpicker)
            self.cp.build_gui()
        else:
            self._clear_button_frame()
            self.button_frame = ttk.Frame(self.root)

    def init_termpicker(self) -> None:
        self.tc = TermChooser(self.root, on_complete=self.success_screen)
        self.tc.build_gui()

    def success_screen(self) -> None:
        self.root.destroy()

        dict_loc = filedialog.askdirectory(title="Choose Location")
        if not dict_loc:
            dict_loc = str(BASE_DIR)

        dest = Path(dict_loc) / WORKBOOK_FILENAME

        Tabloid(output_path=str(dest))

        if self.old_workbook_path:
            old_path = Path(self.old_workbook_path)
            if old_path.exists() and old_path.resolve() != dest.resolve():
                os.remove(old_path)

        with open(INFO_CONFIG, "r") as fr:
            data = json.load(fr)

        data["book-ref"] = dict_loc
        data["book-name"] = WORKBOOK_FILENAME

        with open(INFO_CONFIG, "w") as fw:
            json.dump(data, fw, indent=4)
        
        messagebox.showinfo(
            title="Success!",
            message="Your workbook is under-wraps! Have an amazing semester!",
        )

        

    def upload_roster(self) -> None:
        file_upload: str = filedialog.askopenfilename(
            title="Please select Photo Roster",
            filetypes=[("CSV Files", "*.csv")],
        )

        with open(INFO_CONFIG, "r") as fr:
            data = json.load(fr)

        self.ref = file_upload if file_upload != "" else None
        data["ref"] = file_upload

        with open(INFO_CONFIG, "w") as fw:
            json.dump(data, fw, indent=4)

        if self.ref:
            try:
                roster_df: pd.DataFrame = pd.read_csv(self.ref)
                cleaned = roster_df[~roster_df["Sortable name"].isin(("Lu, Lingma", self.ta))]["Sortable name"]
                self.valid_csv = True
            except (FileNotFoundError, pd.errors.ParserError, KeyError):
                messagebox.showerror(
                    title="Error",
                    message="The selected file was not accepted. Please choose a valid Photo Roster.",
                )
                self.ref = None
                self.valid_csv = False

            if self.valid_csv:
                with open(STUDENT_CONFIG, "r") as frs:
                    student_data = json.load(frs)

                students = student_data["students"]
                for i in cleaned:
                    students.append(i)

                sorted_students = sorted([stud.title() for stud in students])
                student_data["students"] = sorted_students

                with open(STUDENT_CONFIG, "w") as fws:
                    json.dump(student_data, fws, indent=4)

            return True

    def on_exit_create(self) -> None:
        exit_prompt = messagebox.askyesno(
            title="Leaving so soon?",
            message="Exiting now will reset your progress. Continue?",
            icon="warning",
        )

        if exit_prompt:
            self.reset_json()
            self.root.destroy()

    def reset_json(self) -> None:
        with open(INFO_CONFIG, "r") as fri, open(STUDENT_CONFIG, "r") as frs:
            data_info = json.load(fri)
            data_student = json.load(frs)

        with open(INFO_CONFIG, "w") as fwi, open(STUDENT_CONFIG, "w") as fws:
            data_info["ref"] = ""
            data_info["color"] = ""
            data_info["term"] = ""
            data_info["days"] = []
            data_info["book-ref"] = ""
            data_info["book-name"] = ""

            data_student["students"] = []

            json.dump(data_info, fwi, indent=4)
            json.dump(data_student, fws, indent=4)

    def init_get_name(self, on_complete=None):
        self._clear_button_frame()
        self.root.geometry("300x250")
        
        master_frame = ttk.Frame(self.root)
        master_frame.pack(fill="both", expand=True)
        
        lbl_frame = ttk.Frame(master_frame)
        lbl_frame.pack(padx=5, pady=5)
        ttk.Label(lbl_frame, text=" Enter your name", font=("Helvetica", 10, "bold")).pack(padx=5, pady=5)
        
        entry_frame = ttk.Frame(master_frame)
        entry_frame.pack(padx=5, pady=5)
        ttk.Label(entry_frame, text="First Name: ").grid(row=0, column=1, pady=(0,5))
        ttk.Label(entry_frame, text="Last Name: ").grid(row=1, column=1)
        
        firstname = ttk.Entry(entry_frame)
        firstname.grid(row=0, column=2, pady=(0,5)),
        
        lastname = ttk.Entry(entry_frame)
        lastname.grid(row=1, column=2)
        
        button_frame = ttk.Frame(master_frame)
        button_frame.pack(padx=5, pady=(5, 0))
        
        self.property_label.lift()
        
        def add_ta():
            students = load_students()
            full_name = ", ".join((lastname.get().strip(), firstname.get().strip())).title()
            
            if full_name in students:
                with open(INFO_CONFIG, "r") as fr:
                    data = json.load(fr)
                data["TA"] = full_name
                    
                with open(INFO_CONFIG, "w") as fw:
                    json.dump(data, fw, indent=4)

                if on_complete:
                    master_frame.destroy()
                    on_complete()
            else:
                messagebox.showerror(message="TA does not exist inside of your uploaded roster. Please reupload and try again!")
        ttk.Button(button_frame, text="Submit", bootstyle="secondary", command=add_ta).pack()
            
    @staticmethod
    def has_ref() -> bool:
        with open(INFO_CONFIG, "r") as fr:
            reader = json.load(fr)
            return reader["ref"] != ""
        
    @staticmethod
    def has_name() -> bool:
        with open(INFO_CONFIG, "r") as fr:
            reader = json.load(fr)            
            return reader["TA"] != ""
    
def wb_closed() -> bool:
        try:
            with open(resolve_workbook_path(), "r+b") as fr:
                ...

            return True

        except PermissionError:
            messagebox.showerror(title="Excel Sheet Open",
                                 message="It appears you are still working in your attendance sheet. "
                                            "Please save it, close it, and try again.")
            return False

        except FileNotFoundError:
            return True
            
if __name__ == "__main__":
    try:
        root = ttk.Window(themename="minty")
        mn = Main(root)
        root.mainloop()
    except KeyboardInterrupt as e:
        messagebox.showerror(title="PyTendance stopped responding", message="PyTendance has stopped responding, please reload the app and try again")