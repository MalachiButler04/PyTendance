import tkinter as tk
from color_chooser import ColorPicker
from tkinter import messagebox

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x260")
        self.root.title("PyTendance: Add Student")
        self.root.eval('tk::PlaceWindow . center') 

        self.label_frame = tk.Frame(self.root)
        self.label = tk.Label(self.label_frame, text="Add a New Student")
        self.label.pack()
        self.label_frame.pack(pady=5)
        self.entry_frame = tk.Frame(self.root)
        self.entry = tk.Entry(self.entry_frame, width=30)
        self.entry.pack(pady=5)
        self.entry_frame.pack(pady=10)
        self.button_frame = tk.Frame(self.root)
        self.add_button = tk.Button(
            self.button_frame, text="Add Student", command=self.add_student
        )
        self.add_button.pack()
        self.button_frame.pack(pady=10)

    def add_student(self):
        student_name = self.entry.get()
        if student_name:
            messagebox.showinfo("Student Added", f"Student added: {student_name}")
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a student name.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()