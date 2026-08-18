import ttkbootstrap as ttk
from PIL import Image, ImageTk

root = ttk.Window(themename="minty")
root.geometry("300x200")

button_style = ttk.Style()
button_style.configure(
    "custom.TButton",
    borderwidth=0,
    background="#609b8a",
    foreground="white",
    relief="flat"
)

button_style.map(
    "custom.TButton",
    background=[
    ("active", "#6ea092"),
    ("pressed", "#6ea092")
    ]
)

# Left button section
button_master = ttk.Frame(
    root,
    bootstyle="primary",
    borderwidth=1,
    relief="sunken"
)
button_master.pack(side="left", fill="y", expand=False)

button_frame = ttk.Frame(button_master, bootstyle="primary")
button_frame.pack(padx=5, pady=(35,0))

# Buttons
ttk.Button(
    button_frame,
    text="      New\nWorkbook",
    width=10,
    style="custom.TButton"
).pack(pady=5)

ttk.Button(
    button_frame,
    text="      Edit\nWorkbook",
    width=10,
    style="custom.TButton"
).pack(pady=5)

# Title
title_frame = ttk.Frame(root)
title_frame.pack(fill="y", expand=True)

# Photo section
ico_ref = Image.open("assets/492snake_100855.png")
ico_ref = ico_ref.resize((100, 100))

photo = ImageTk.PhotoImage(ico_ref)

label = ttk.Label(title_frame, image=photo)
label.image = photo
label.place(anchor="center", relx=0.5, rely=0.5)

root.mainloop()