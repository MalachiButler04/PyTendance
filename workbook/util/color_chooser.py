import json
import ttkbootstrap as ttk
from tkinter import messagebox

from config.path_config import INFO_CONFIG

class ColorPicker:
    def __init__(self, root: ttk.Window, on_complete=None):
        self.root = root
        self.on_complete = on_complete

        self.canvas_width = 250
        self.canvas_height = 120
        self.size = 70

        self.is_done = False
        self.color_name = None
        self.option = False

        self.hex_vals = {
            "Dusty Rose": "#e6b8af",
            "Soft Pink": "#f4cccc",
            "Peach Cream": "#fce5cd",
            "Sage Green": "#d9ead3",
            "Mist Blue": "#d0e0e3",
            "Powder Blue": "#c9daf8",
            "Sky Mist": "#cfe2f3",
            "Lavender Gray": "#d9d2e9",
            "Blush Lavender": "#ead1dc",
        }

    def build_gui(self):
        self.frame = ttk.Frame(self.root)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.canv_frame = ttk.Frame(self.frame)
        self.canv_frame.pack(ipadx=3, pady=(5, 0))

        self.canvas = ttk.Canvas(
            self.canv_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            highlightthickness=0,
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
            x1, y1, x2, y2, fill="#FFFFFF", outline="black"
        )

        # Text item centered inside the rectangle
        self.hex_text = self.canvas.create_text(
            center_x, center_y, text="", fill="black", font=("TkDefaultFont", 9, "bold")
        )

        self.color_label = ttk.Label(self.frame, text="", borderwidth=2)
        self.color_label.place(relx=0.4154, rely=.5)
        
        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(ipady=10, pady=(5, 0))

        first_color = next(iter(self.hex_vals))
        self.selected_color = ttk.StringVar(self.root, value=first_color)

        self.ops = ttk.OptionMenu(
            self.button_frame,
            self.selected_color,
            *self.hex_vals,
            command=self.change_color,
        )
        self.ops.pack()

        self.conf_button = ttk.Button(self.frame, text="Submit", command=self.get_conf, bootstyle="secondary")
        self.conf_button.pack(pady=(5, 8))

        self.change_color(first_color)

    def change_color(self, c):
        hex_val = self.hex_vals[c]
        self.canvas.itemconfig(self.square, fill=hex_val)


        self.canvas.itemconfig(self.hex_text, text=hex_val, fill="black")

        self.color_name = c

    def get_conf(self):
        if not self.color_name:
            return

        self.option = messagebox.askyesno(
            "Confirm Color?",
            message=f"Would you like to confirm your theme as '{self.color_name}'?",
            icon=messagebox.INFO,
        )

        if not self.option:
            return

        try:
            with open(INFO_CONFIG, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data["color"] = self.hex_vals[self.color_name]

        with open(INFO_CONFIG, "w") as file:
            json.dump(data, file, indent=4)

        messagebox.showinfo(
            "Confirmed",
            f"Theme confirmed: {self.color_name} ({self.hex_vals[self.color_name]})",
            icon=messagebox.INFO,
        )
        
        self.frame.destroy()
            
        if self.on_complete:
            self.on_complete()