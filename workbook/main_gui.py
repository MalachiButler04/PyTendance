import tkinter as tk
from color_chooser import ColorPicker
from tkinter import messagebox

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x350")
        self.root.title("PyTendance")
        self.root.eval('tk::PlaceWindow . center') 
    
        self.label_frame = tk.Frame(self.root)
        self.label = tk.Label(self.label_frame, text="Welcome to PyTendance!")
        self.label.pack()
        self.label_frame.pack(pady=5)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        self.new_term_button = tk.Button(
            self.button_frame, text="New Term", command=lambda: messagebox.showinfo("New Term", "This feature is coming soon!")
        )
        self.new_term_button.pack(side=tk.LEFT, padx=5)

        self.edit_term_button = tk.Button(
            self.button_frame, text="Edit Term", 
            command=lambda: messagebox.showinfo("Edit Term", "This feature is coming soon!")
        )
        self.edit_term_button.pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()