import tkinter as tk
from tkinter import messagebox

class ColorPicker:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x260")
        self.root.title("Choose your color!")
        self.root.eval('tk::PlaceWindow . center') 

        self.canvas_width = 250
        self.canvas_height = 120
        self.size = 70

        self.hex_vals = {
            "Dusty Rose": "#e6b8af",
            "Soft Pink": "#f4cccc",
            "Peach Cream": "#fce5cd",
            "Sage Green": "#d9ead3",
            "Mist Blue": "#d0e0e3",
            "Powder Blue": "#c9daf8",
            "Sky Mist": "#cfe2f3",
            "Lavender Gray": "#d9d2e9",
            "Blush Lavender": "#ead1dc"
        }

        self.build_ui()

    def build_ui(self):
        self.label_frame = tk.Frame(self.root)
        self.color_label = tk.Label(self.label_frame, text="Choose your color!")
        self.color_label.pack()
        self.label_frame.pack(pady=5)

        self.canv_frame = tk.Frame(self.root)
        self.canv_frame.pack(pady=3)

        self.canvas = tk.Canvas(
            self.canv_frame,
            width=self.canvas_width,
            height=self.canvas_height
        )
        self.canvas.pack()

        center_x = self.canvas_width / 2
        center_y = self.canvas_height / 2
        half = self.size / 2

        x1 = center_x - half
        y1 = center_y - half
        x2 = center_x + half
        y2 = center_y + half

        self.square = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill="#FFFFFF"
        )

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        self.selected_color = tk.StringVar(self.root, value=list(self.hex_vals.keys())[0])

        self.ops = tk.OptionMenu(
            self.button_frame,
            self.selected_color,
            *self.hex_vals,
            command=self.change_color
        )
        self.ops.pack()

        self.conf_button = tk.Button(self.root, text="Submit", command=self.get_conf)
        self.conf_button.pack(pady=1)

        first_color = list(self.hex_vals.keys())[0]
        self.change_color(first_color)

    def change_color(self, c):
        self.canvas.itemconfig(self.square, fill=self.hex_vals[c])
        self.color_label.config(text=self.hex_vals[c])
        self.color_name = c

    def get_conf(self):
        if self.color_name is not None:
            self.option = messagebox.askyesno(
                "Confirm Color?",
                message=f"Would you like to confirm your theme as '{self.color_name}'?",
                icon=messagebox.INFO
            )

            if self.option:
                import json

                try:
                    with open("config.json", "r") as file:
                        data = json.load(file)
                        data["color"] = self.hex_vals[self.color_name]

                except FileNotFoundError, json.JSONDecodeError:
                    data = {}
                
                with open("config.json", "w") as file:
                    json.dump(data, file, indent=4)

                messagebox.showinfo(
                    "Confirmed",
                    f"Theme confirmed: {self.color_name} ({self.hex_vals[self.color_name]})",
                    icon=messagebox.INFO
                )

                self.root.destroy()

root =  tk.Tk()
ColorPicker(root)
root.mainloop()