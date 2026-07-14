import tkinter as tk
from tkinter import Tk, filedialog
import json
from pathlib import Path
from workbook.util.color_chooser import ColorPicker

BASE_DIR = Path(__file__).resolve().parent
info_config = BASE_DIR / "config" / "book_config.json"

class Main:
    def __init__(self, root:Tk):
        
        self.root = root
        root.geometry("300x200")
        root.eval("tk::PlaceWindow . center")
        root.title("PyTendance")
        root.resizable(False, False)

        icon = tk.PhotoImage(file="assets/492snake_100855.png")
        root.iconphoto(True, icon)
        
        property_label = tk.Label(root, text="Malachi A. Butler and Jacob T. Imbus", font=("Aptos", 5))
        property_label.place(anchor="s", relx=.25, rely=.95)
        
        tk.Label(root, text="Pytendance", font=("Helvetica", 15, "bold"), border=1, relief="ridge", borderwidth=2).pack(pady=10, ipadx=5, ipady=5)
        
        self.button_frame:tk.Frame = tk.Frame(root)
        self.button_frame.place(anchor="center", relx=.5, rely=.5)
        
        create_new = tk.Button(self.button_frame, text="New Worksheet", command=lambda: self.init_workbook(), width=15)
        create_new.pack(pady=5)
        edit_existing:tk.Button = tk.Button(self.button_frame, text="Edit Worksheet", command=lambda: print("edit works"), width=15)
        edit_existing.pack(pady=5)

    def init_workbook(self):
        self.button_frame.destroy()
        self.upload_roster()
        
        cp = ColorPicker(self.root)
        cp.build_ui()
        self.root.geometry("300x350")
        
    @staticmethod
    def upload_roster() -> None:  
        global info_config
        
        file_upload:str = filedialog.askopenfilename(
            title="Please select Photo Roster", 
            filetypes= [
            ("CSV Files", "*.csv"),
            ("All Files", "*.*")
            ]
        )
        
        with open(info_config, "r") as fr:
            data = json.load(fr)
            data["ref"] = file_upload
        
        with open(info_config, "w") as fw:
            json.dump(data, fw, indent=4)
        
        print(f"upload successful path: {file_upload}")

if __name__ == "__main__":
    root = Tk()
    
    mn = Main(root)
    root.mainloop()