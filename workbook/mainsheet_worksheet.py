import json
from tkinter import Tk, filedialog
import color_chooser

class MainPage:
    def __init__(self, root):
        self.root = root

    def set_config(self):
        path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )

       # color_chooser.ColorPicker(self.root) 

        with open("config.json", "r") as js:
            data = json.load(js)

        print(path if len(path) > 0 else "Fail")
        
        data["ref"] = path
        data["term"] = "Fall"

        with open("config.json", "w") as jw:
            json.dump(data, jw, indent=4)

root = Tk()
root.withdraw()
mp = MainPage(root)
mp.set_config()
root.mainloop()