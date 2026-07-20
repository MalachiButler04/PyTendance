import xlsxwriter as xl
from xlsxwriter import Workbook
import json
import pandas as pd
from config.path_config import STUDENT_CONFIG, INFO_CONFIG


class Results:
    def __init__(self):
        self.weeks = [f"Week {i}" for i in range(1,16)] 
        self.students = self.load_students()
        wb = Workbook("Attendance Tabloid")

        self.ref, self.color, self.term, self.days = self.load_config()

    def init_workbook(self):
        ...
    
    def week_sheet(self, workbook: Workbook):
        ...
        
    @staticmethod
    def load_students() -> list[str]:
        with open(STUDENT_CONFIG, "r") as fr:
            return json.load(fr)["students"]
    
    @staticmethod
    def load_config():
        with open(INFO_CONFIG, "r") as fr:
            data = json.load(fr)
            return data["ref"], data["color"], data["term"], data["days"]


r = Results()


