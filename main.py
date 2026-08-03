import ttkbootstrap as ttk
from tkinter import filedialog, messagebox
import json
from workbook.util.color_chooser import ColorPicker
from workbook.util.term_chooser import TermChooser
import pandas as pd
from workbook.util.tabloid import Tabloid
from config.path_config import INFO_CONFIG, STUDENT_CONFIG, BASE_DIR, WORKBOOK_FILENAME
import os


def main_menu(frame: ttk.Frame | None = None, main_app: "Main" | None = None):
    if main_app is None:
        raise ValueError("main_app must be provided")
    if frame is None:
        frame = ttk.Frame(main_app.root)

    frame.place(anchor="center", relx=.5, rely=.55)

    create_new = ttk.Button(frame, text="New Worksheet", bootstyle="secondary", command=main_app.init_workbook, width=15)
    create_new.pack(pady=5)

    edit_existing: ttk.Button = ttk.Button(frame, text="Edit Worksheet", bootstyle="secondary", command=main_app.student_manager, width=15)
    edit_existing.pack(pady=5)

class Main:
    root = None
    instance = None

    def __init__(self, root: ttk.Window | None):
        self.button_frame = None

        if root:
            self.root = root
            Main.root = root
            Main.instance = self
            
            self.init_main(self.root)
            
        property_label = ttk.Label(root, text="Malachi A. Butler and Jacob T. Imbus", font=("Aptos", 5))
        property_label.place(anchor="s", relx=.25, rely=.90)
        
        self.ref = None
        self.manager_frame = None
        self.valid_csv = False

        ttk.Label(
            root,
            text="  PyTendance",
            font=("Helvetica", 15, "bold"),
            bootstyle="primary-inverse"
        ).pack(pady=(15, 10), ipadx=5, ipady=5)
   
    def init_main(self, root):
        root.title("PyTendance")
        self.button_frame = ttk.Frame(root)
        
        root.geometry("300x200")
        root.eval("tk::PlaceWindow . center")
        root.resizable(False, False)
        root.theme_use("pydata-light")
        icon = ttk.PhotoImage(file=str(BASE_DIR / "assets" / "492snake_100855.png"))
        root.iconphoto(True, icon)
                     
                
        self.button_frame.place(anchor="center", relx=.5, rely=.55)
                                
        create_new = ttk.Button(self.button_frame, text="New Worksheet", bootstyle="secondary", command=self.init_workbook, width=15)
        create_new.pack(pady=5)
                                
        edit_existing: ttk.Button = ttk.Button(self.button_frame, text="Edit Worksheet", bootstyle="secondary", command=self.init_student_manager, width=15)
        edit_existing.pack(pady=5)       
        
    def on_exit_create(self) -> None:
        exit_prompt = messagebox.askyesno(title="Leaving so soon?", message="Exiting now will reset your progress. Continue?", icon="warning")

        if exit_prompt:
            self.reset_json()
            self.root.destroy()
            self.init_student_manager()
            
    def init_student_manager(self):
        from workbook.util.student_manager import StudentManager
        exists = os.path.exists(WORKBOOK_FILENAME)
        
        if exists and all(Tabloid.load_config()):
            
            sm = StudentManager(self.root)
            self.button_frame.destroy()
                
            self.button_frame = ttk.Frame(self.root)
            
            sm.button_frame = self.button_frame
            
            self.button_frame.place(relx=0.5, rely=0.5, anchor="center")
            ttk.Button(self.button_frame, text="Add Student", bootstyle="secondary", command=sm.add_student).grid(row=0, column=0, padx=5)
            ttk.Button(self.button_frame, text="Remove Student", bootstyle="secondary", command=sm.remove_student).grid(row=0, column=1, padx=5)
                    
        else:
            messagebox.showerror(title="No Workbook Data Found", message="There was an error while loading your attendance sheet data. Please try again or press 'New Workbook'")
            
    def init_workbook(self) -> None:
        warning = messagebox.askokcancel(title="Warning", message="Any old data will be erased. Continue?", icon="warning")

        if warning:
            self.valid_csv = False
            self.reset_json()
            self.upload_roster()

            if self.has_ref() and self.valid_csv:
                self.root.protocol("WM_DELETE_WINDOW", self.on_exit_create)
                if self.button_frame is not None:
                    self.button_frame.destroy()
                self.init_colorpicker()
            else:
                if self.button_frame is not None:
                    self.button_frame.destroy()
                self.button_frame = ttk.Frame(self.root)
                main_menu(self.button_frame, self)

    def init_colorpicker(self) -> None:
        if self.valid_csv:
            self.cp = ColorPicker(self.root, on_complete=self.init_termpicker)
            self.cp.build_gui()
        else:
            if self.button_frame is not None:
                self.button_frame.destroy()
            self.button_frame = ttk.Frame(self.root)
            main_menu(self.button_frame, self)

    def init_termpicker(self) -> None:
        self.tc = TermChooser(self.root, on_complete=self.success_screen)
        self.tc.build_gui()

    def success_screen(self) -> None:
        self.root.destroy()
        Tabloid()
        messagebox.showinfo(title="Success!", message="Your workbook is under-wraps! Have an amazing semester!")

    def upload_roster(self) -> None:
        file_upload: str = filedialog.askopenfilename(
            title="Please select Photo Roster",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
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
                cleaned = roster_df[roster_df["Sortable name"] != "Lu, Lingma"]["Sortable name"]
                self.valid_csv = True
                
            except (FileNotFoundError, pd.errors.ParserError, KeyError):
                messagebox.showerror(title="Error", message="The selected file was not accepted. Please choose a valid Photo Roster.")
                self.ref = None
                
            if self.valid_csv:
                with open(STUDENT_CONFIG, "r") as frs:
                    student_data = json.load(frs)

                    students = student_data["students"]

                    for i in cleaned:
                        students.append(i)

                    student_data["students"] = students

                with open(STUDENT_CONFIG, "w") as fws:
                    json.dump(student_data, fws, indent=4)

    def reset_json(self) -> None:
        with open(INFO_CONFIG, "r") as fri, open(STUDENT_CONFIG, "r") as frs:
            data_info = json.load(fri)
            data_student = json.load(frs)

        with open(INFO_CONFIG, "w") as fwi, open(STUDENT_CONFIG, "w") as fws:
            data_info["ref"] = ""
            data_info["color"] = ""
            data_info["term"] = ""
            data_info["days"] = []

            data_student["students"] = []

            json.dump(data_info, fwi, indent=4)
            json.dump(data_student, fws, indent=4)

    @staticmethod
    def has_ref() -> bool:
        """Return True if a photo roster reference has been set in the config."""
        with open(INFO_CONFIG, "r") as fr:
            reader = json.load(fr)
            return reader["ref"] != ""

if __name__ == "__main__":
    root = ttk.Window()
    mn = Main(root)
    root.mainloop()