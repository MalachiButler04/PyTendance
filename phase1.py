from xlsxwriter import Workbook
from tkinter import Tk
import tkinter as tk
from tkinter import filedialog
from pandas import read_csv
import pandas as pd

wb = Workbook("resize.xlsx")
ws = wb.add_worksheet()

names = None

def upload() -> str: 
    fp = filedialog.askopenfilename(
        title="Select Csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    print(fp)
    return fp

def fileUpload() -> pd.DataFrame: 
    global names
    result = upload()
    
    names = read_csv(result)

    #Cleaned from TA/Prof
    names = names[(names["Sortable name"] != "Butler, Malachi")
            & (names["Sortable name"] != "Imbus, Jacob") &
            (names["Sortable name"] != "Lu, Lingma")]
    
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

headers = ["Monday Lecture", "Monday Lab", "Attend Help Session?"] 

max_width = len(headers[0])
for i in range(len(headers) - 1): 
    max_width = max(max_width, len(headers[i + 1]))

center = wb.add_format({"align":"center"})

name_len_max = len(names["Sortable name"][0])

ws.write(0,0,"Name", center)
for row, name in enumerate(names["Sortable name"], 1):
    ws.write(row, 0, name)

    for i in range(3):
        ws.insert_checkbox(row, i+1, False)

    name_len_max = max(name_len_max, len(name))

    width = name_len_max * .8
    ws.set_column(0,0, width=width )


print(name_len_max)
for col, head in enumerate(headers, 1):
    ws.write(0, col, head, center)

    width = max_width * .9

    ws.set_column(col, col, width)

wb.close()