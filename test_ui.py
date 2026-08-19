import ttkbootstrap as ttk
from PIL import Image, ImageTk
from tkinter import font

root = ttk.Window(themename="minty")
root.geometry("300x200")
root.configure(bg="grey")
root.eval("tk::PlaceWindow . center")

menu_bar = ttk.Menu(root)
root.configure(menu=menu_bar)

file_menu = ttk.Menu(menu_bar, tearoff=0)

file_menu.add_command(
    label="Move Worksheet",
    command=lambda: print("works")
)

menu_bar.add_cascade(
    label="Worksheet",
    menu=file_menu
)

edit_font = font.Font(
    family="Helvetica",
    size=8,
    weight="bold"
)

style = ttk.Style()

style.configure(
    "primary.TButton",
    borderwidth=0,
    focusthickness=0,
    padding=3
)

# Get the same colors used by the Minty primary theme
primary_color = style.colors.primary
primary_hover = style.colors.primary

# Custom Edit button
style.configure(
    "Edit.TButton",
    background=primary_color,
    foreground="white",
    borderwidth=0,
    focusthickness=0,
    padding=3,
    font=edit_font
)

style.map(
    "Edit.TButton",
    background=[
        ("active", primary_hover),
        ("pressed", primary_color)
    ],
    foreground=[
        ("active", "white"),
        ("pressed", "white")
    ]
)
master = ttk.Frame(
    root,
    bootstyle="primary",
    width=75
)

master.pack(
    side="left",
    fill="y"
)

button_frame = ttk.Frame(
    master,
    bootstyle="primary"
)

button_frame.place(
    rely=.5,
    anchor="w"
)

# New Worksheet
new_button = ttk.Button(
    button_frame,
    text="      New\nWorksheet",
    bootstyle="primary.TButton",
    style="Edit.TButton"
)

new_button.pack(
    fill="x",
    pady=(0, 5),
    padx=(5,0)
)

# Edit Worksheet
edit_button = ttk.Button(
    button_frame,
    text="       Edit\nWorksheet",
    style="Edit.TButton"
)

edit_button.pack(
    fill="x",
    pady=5,
    padx=(5,0)
)

content = ttk.Frame(root)

content.pack(
    side="left",
    fill="both",
    expand=True
)

ttk.Label(
    content,
    text="PyTendance",
    font=("Helvetica", 20, "bold")
).pack(
    pady=(20, 0)
)

pil = Image.open(
    "assets/492snake_100855.png"
)

pil.thumbnail((100, 100))

photo = ImageTk.PhotoImage(pil)

label = ttk.Label(
    content,
    image=photo
)

label.image = photo

label.pack(
    expand=True
)

root.mainloop()