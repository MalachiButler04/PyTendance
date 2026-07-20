import tkinter as tk
from tkinter import Tk, filedialog, messagebox
import json
from pathlib import Path
from workbook.util.color_chooser import ColorPicker
from workbook.util.term_chooser import TermChooser

BASE_DIR = Path(__file__).resolve().parent
info_config = BASE_DIR / "config" / "book_config.json"

class Main:
    def __init__(self, root: Tk):
        self.root = root
        root.title("PyTendance")
        root.geometry("300x200")
        root.eval("tk::PlaceWindow . center")
        root.resizable(False, False)

        icon = tk.PhotoImage(file="assets/492snake_100855.png")
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

            if not self.check_ref():
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

        with open(info_config, "r") as fr:
            data = json.load(fr)
            data["ref"] = file_upload

        with open(info_config, "w") as fw:
            json.dump(data, fw, indent=4)
    
    def reset_json(self) -> None:
        with open(info_config, "r") as fr:
            data = json.load(fr)
        
        with open(info_config, "w") as fw:
            data["ref"] = ""
            data["color"] = ""
            data["term"] = ""
            data["days"] = []

            json.dump(data, fw, indent=4)

    @staticmethod
    def check_ref() -> bool:
        with open(info_config, "r") as fr:
            reader = json.load(fr)
            return reader["ref"] == ""
        
if __name__ == "__main__":
    root = Tk()
    mn = Main(root)
    root.mainloop()