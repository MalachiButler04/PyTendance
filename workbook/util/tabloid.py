import xlsxwriter as xl
from xlsxwriter import Workbook
import json
import os
from os import remove
from config.path_config import STUDENT_CONFIG, INFO_CONFIG, WORKBOOK_FILENAME, TOTAL_WEEKS, WEEK_SHEET_PREFIX, LAB_ATTENDANCE_DIVISOR

class Tabloid:
    TA = None
    
    def __init__(self, skip_init: bool = False):
        self.weeks = [f"{WEEK_SHEET_PREFIX}{i}" for i in range(1, TOTAL_WEEKS + 1)]
        self.students = load_students()
        self.wb = Workbook(WORKBOOK_FILENAME)
        
        self.ref, self.color, self.term, self.days, self.ta = load_config()

        Tabloid.ta = self.ta
        
        self.header_format = self.wb.add_format({
            "align": "center",
            "bold": True,
            "bg_color": self.color,
            "border": 1
        })

        self.centered_vals = self.wb.add_format({"align": "center"})
        self.centeredwborder = self.wb.add_format({"align": "center", "border": 1})

        if not skip_init:
            self.init_workbook()

    def init_workbook(self):
        self.results_page()

        for i in range(TOTAL_WEEKS):
            self.week_sheet(i)

        self.attended_labs_page()

        self.wb.close()

    def attended_labs_page(self):
        sheet = self.wb.add_worksheet("Total Labs Attended")

        sheet.write(0, 0, "Names", self.header_format)
        sheet.write(0, 1, "Total", self.header_format)
        sheet.write(0, 2, " (%) ", self.header_format)

        percent_format = self.wb.add_format({"align": "center", "num_format": "0.00%"})

        max_width = len(self.students[0])
        for row, student in enumerate(self.students, start=1):
            sheet.write(row, 0, student)

            max_width = max(len(student), max_width)
            sheet.set_column(0, 0, max_width)

            week_range = f"{WEEK_SHEET_PREFIX}1:{WEEK_SHEET_PREFIX}{TOTAL_WEEKS}"
            sheet.write_formula(row, 1, f"=SUM('{week_range}'!H{row+1})", self.centered_vals)
            sheet.write_formula(row, 2, f"=SUM('{week_range}'!H{row+1}) / {LAB_ATTENDANCE_DIVISOR}", percent_format)

    def results_page(self):
        sheet = self.wb.add_worksheet("Results")
        headers = ["Name", *self.weeks]

        for col, header in enumerate(headers):
            sheet.write(0, col, header, self.header_format)
            sheet.set_column(0, col, width=10)

        sheet.write(0, 16, "Total Attended", self.header_format)
        sheet.set_column(16, 16, 15)

        max_width = len(self.students[0])
        for row, student in enumerate(self.students, start=1):
            sheet.write(row, 0, student, self.centeredwborder)

            max_width = max(len(student), max_width)
            sheet.set_column(0, 0, max_width)

            for i in range(1, TOTAL_WEEKS + 1):
                sheet.write_formula(row, i, f"='{WEEK_SHEET_PREFIX}{i}'!G{row+1}", self.centeredwborder)

            sheet.write_formula(row, 16, f"=SUM(B{row+1}:P{row+1})", self.centeredwborder)

        red_bg = self.wb.add_format({"bg_color": "#ea9999"})
        green_bg = self.wb.add_format({"bg_color": "#b7e1cd"})
        gold_bg = self.wb.add_format({"bg_color": "#fef2cd"})
        platinum_bg = self.wb.add_format({"bg_color": "#ffe599"})

        sheet.conditional_format(f"B2:P{len(self.students)+1}", {
            'type': 'cell',
            'criteria': "=",
            "value": 0,
            "format": red_bg
        })

        sheet.conditional_format(f"B2:P{len(self.students)+1}", {
            'type': 'cell',
            'criteria': "between",
            'minimum': 1,
            'maximum': 2,
            "format": green_bg
        })

        sheet.conditional_format(f"B2:P{len(self.students)+1}", {
            'type': 'cell',
            'criteria': "=",
            "value": 3,
            "format": gold_bg
        })

        sheet.conditional_format(f"B2:P{len(self.students)+1}", {
            'type': 'cell',
            'criteria': "=",
            "value": 4,
            "format": platinum_bg
        })

    def week_sheet(self, week: int):
        sheet = self.wb.add_worksheet(self.weeks[week])
        header = [
            "Names",
            f"{self.days[0]} Lecture",
            f"{self.days[0]} Lab",
            f"{self.days[1]} Lecture",
            "Attended Help Session?"
        ]

        sheet.write(0, 6, "EOW Summary", self.header_format)
        sheet.write(0, 7, "Attended Lab", self.header_format)

        sheet.set_column(0, 6, len("EOW Summary") * 1.5)
        sheet.set_column(0, 7, len("Attended Lab") * 1.5)

        for col, text in enumerate(header):
            sheet.write(0, col, text, self.header_format)
            width = len(text) * 1.1 if len(text) < 20 else len(text) * 1.2
            sheet.set_column(col, col, width)

        max_width = len(self.students[0])
        for row, student in enumerate(self.students, start=1):
            sheet.write(row, 0, student)
            max_width = max(len(student), max_width) * .98
            sheet.set_column(0, 0, max_width)
            sheet.write_formula(row, 6, f"=COUNTIF(B{row+1}:E{row+1}, TRUE)", self.centered_vals)
            sheet.write_formula(row, 7, f"=COUNTIF(C{row+1}, TRUE)", self.centered_vals)

            for i in range(1, 5):
                sheet.insert_checkbox(row, i, False)

    def week_sheet_with_data(self, week: int, WEEK_FRAME):
        sheet = self.wb.add_worksheet(self.weeks[week])
        header = [
            "Names",
            f"{self.days[0]} Lecture",
            f"{self.days[0]} Lab",
            f"{self.days[1]} Lecture",
            "Attended Help Session?"
        ]

        sheet.write(0, 6, "EOW Summary", self.header_format)
        sheet.write(0, 7, "Attended Lab", self.header_format)

        sheet.set_column(0, 6, len("EOW Summary") * 1.5)
        sheet.set_column(0, 7, len("Attended Lab") * 1.5)

        for col, text in enumerate(header):
            sheet.write(0, col, text, self.header_format)
            width = len(text) * 1.1 if len(text) < 20 else len(text) * 1.2
            sheet.set_column(col, col, width)

        week_key = f"{WEEK_SHEET_PREFIX}{week + 1}"
        week_df = WEEK_FRAME[week_key].copy()

        if "Names" in week_df.columns:
            week_df = week_df.set_index("Names")

        max_width = len(self.students[0]) if self.students else 0

        for row, student in enumerate(self.students, start=1):
            sheet.write(row, 0, student)
            max_width = max(len(student), max_width) * 0.98
            sheet.set_column(0, 0, max_width)

            sheet.write_formula(row, 6, f"=COUNTIF(B{row+1}:E{row+1}, TRUE)", self.centered_vals)
            sheet.write_formula(row, 7, f"=COUNTIF(C{row+1}, TRUE)", self.centered_vals)

            if student in week_df.index:
                row_data = week_df.loc[student]
                v1 = bool(row_data[f"{self.days[0]} Lecture"])
                v2 = bool(row_data[f"{self.days[0]} Lab"])
                v3 = bool(row_data[f"{self.days[1]} Lecture"])
            else:
                v1 = v2 = v3 = False

            sheet.insert_checkbox(row, 1, v1)
            sheet.insert_checkbox(row, 2, v2)
            sheet.insert_checkbox(row, 3, v3)
            sheet.insert_checkbox(row, 4, False)

    def rebuild_workbook(self):
        from workbook.util.student_manager import StudentManager

        if os.path.exists(WORKBOOK_FILENAME):
            remove(WORKBOOK_FILENAME)

        self.wb = Workbook(WORKBOOK_FILENAME)
        self.header_format = self.wb.add_format({
            "align": "center",
            "bold": True,
            "bg_color": self.color,
            "border": 1
        })
        self.centered_vals = self.wb.add_format({"align": "center"})
        self.centeredwborder = self.wb.add_format({"align": "center", "border": 1})

        self.students = load_students()

        WEEK_FRAME = StudentManager.FRAMES

        self.results_page()

        for i in range(TOTAL_WEEKS):
            self.week_sheet_with_data(i, WEEK_FRAME)

        self.attended_labs_page()
        self.wb.close()

def load_students() -> list[str]:
    with open(STUDENT_CONFIG, "r") as fr:
        students = json.load(fr)["students"]
        return students

def load_config():
    with open(INFO_CONFIG, "r") as fr:
        data = json.load(fr)
        return data["ref"], data["color"], data["term"], data["days"], data["TA"]       