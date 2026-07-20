import tkinter as tk
from tkinter import Tk, filedialog, messagebox
import json
from workbook.util.color_chooser import ColorPicker
from workbook.util.term_chooser import TermChooser
import pandas as pd 
from workbook.config.path_config import INFO_CONFIG, STUDENT_CONFIG, BASE_DIR

class Main:
    def __init__(self, root: Tk):
        self.root = root
        root.title("PyTendance")
        root.geometry("300x200")
        root.eval("tk::PlaceWindow . center")
        root.resizable(False, False)

        self.ref = None

        icon = tk.PhotoImage(file=str(BASE_DIR / "assets" / "492snake_100855.png"))
        root.iconphoto(True, icon)

        property_label = tk.Label(root, text="Malachi A. Butler and Jacob T. Imbus", font=("Aptos", 5))
        property_label.place(anchor="s", relx=.25, rely=.95)

        tk.Label(
            root,
            text="Pytendance",
            font=("Helvetica", 15, "bold"),
            border=1,
            relief="ridge",
            borderwidth=2,
        ).pack(pady=10, ipadx=5, ipady=5)

        self.button_frame: tk.Frame = tk.Frame(root)
        self.button_frame.place(anchor="center", relx=.5, rely=.5)

        create_new = tk.Button(self.button_frame, text="New Worksheet", command=lambda: self.init_workbook(), width=15)
        create_new.pack(pady=5)

        edit_existing: tk.Button = tk.Button(self.button_frame, text="Edit Worksheet", command=lambda: print("edit works"), width=15)
        edit_existing.pack(pady=5)

    def on_exit_create(self) -> None:
      
        exit_prompt = messagebox.askyesno(title="Leaving so soon?" , message="Exiting now will reset your progress. Continue?", icon="warning")

        if exit_prompt:
            self.reset_json()
            self.root.destroy()
        
    def init_workbook(self) -> None:
        warning = messagebox.askokcancel(title="Warning", message="This action will erase any previous worksheet information. Continue?", icon="warning")
        
        if warning: 
            self.reset_json()
            self.upload_roster()

            if self.has_ref():
                self.root.protocol("WM_DELETE_WINDOW", self.on_exit_create)
                self.button_frame.destroy()
                self.init_colorpicker()
            else:
                messagebox.showerror(title="Error", message="Please select your Photo Roster to continue")

    def init_colorpicker(self) -> None:
        self.cp = ColorPicker(self.root, on_complete=self.init_termpicker)
        self.cp.build_gui()

    def init_termpicker(self) -> None:
        self.tc = TermChooser(self.root, on_complete=self.success_screen)
        self.tc.build_gui()

    def success_screen(self) -> None:
        self.root.destroy()
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
                student_array = roster_df["Sortable name"].values
            except FileNotFoundError:
                messagebox.showerror(title="Error", message=f"Could not find file:\n{self.ref}")
                self.ref = None
                return
            except pd.errors.ParserError:
                messagebox.showerror(title="Error", message="The selected file could not be read as a valid CSV.")
                self.ref = None
                return
            except KeyError:
                messagebox.showerror(
                    title="Error",
                    message='The selected CSV is missing a required "Sortable name" column.'
                )
                self.ref = None
                return

            with open(STUDENT_CONFIG, "r") as frs:
                student_data = json.load(frs)

                students = student_data["students"]

                for i in student_array:
                    students.append(i)
                
                student_data["students"] = students
                
            with open(STUDENT_CONFIG, "w") as fws:
                json.dump(student_data, fws, indent=4)

    
    def reset_json(self) -> None:
        with open(INFO_CONFIG, "r") as fri , open(STUDENT_CONFIG, "r") as frs:
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
    root = Tk()
    mn = Main(root)
    root.mainloop()