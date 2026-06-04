from tkinter import Tk
import tkinter as tk
from tkinter import filedialog
from pandas import read_csv
import pandas as pd

data = None

def upload(): 
    fp = filedialog.askopenfilename(
        title="Select Csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    return fp

def fileUpload() -> pd.DataFrame: 
    global data
    result = upload()
    
    data = read_csv(result)

    #Cleaned from TA/Prof
    data = data[(data["Sortable name"] != "Butler, Malachi")
            & (data["Sortable name"] != "Imbus, Jacob") &
            (data["Sortable name"] != "Lu, Lingma")]
    
    root.destroy()

root = Tk()
root.geometry("300x150")
root.anchor("center")
root.resizable(False, False)
root.eval("tk::PlaceWindow . Center")

frm = tk.Frame(root, height=100, width= 100, relief=tk.RIDGE)

root.title("Attendance Tabloid Generator Upload")
frm.pack(expand=True, fill='both')
tk.Label(frm, text="Upload Photo Roster Here").place(relx=.5, rely=.3, anchor="center")
tk.Button(frm, text="Upload", command=(fileUpload)).place(relx=.5, rely=.6, anchor="center")

root.mainloop()

print(data)