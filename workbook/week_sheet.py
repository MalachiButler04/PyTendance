from xlsxwriter import Workbook
from tkinter import Tk
import tkinter as tk
from pandas import read_csv
import pandas as pd
import os
import json

class WeekSheet:
    def __init__(self, week:int, work_book:Workbook):
        self.sheet_title:str = f"Week {week}"
        self.work_book = work_book
        self.worksheet = work_book.add_worksheet(self.sheet_title)

        '''Assumes base workbook is already created'''
        self.data = self.loadConfig()

        self.pathRef = "/Users/malachibutler/Downloads/PhotoRoster_2377748_2026-05-17.csv"
   

        self.names:pd.DataFrame = self.getNames()
        
        self.create_sheet()

    def create_sheet(self):
        headers_format = self.work_book.add_format({"bold":True, "bg_color":"#cfe2f3","align":"center", "border":1})
        col_format = self.work_book.add_format({"left":1,"right":1})

        #Names
        self.worksheet.write(0,0, "Name", headers_format)
        max_name_length = len(self.names["Sortable name"].iloc[0])

        last = len(self.names)
        bottom_format = self.work_book.add_format({"left":1,"right":1,"bottom":1})
        bottom_name = self.work_book.add_format({"bottom":1})

        for row,name in enumerate(self.names["Sortable name"],1):

            fmt = bottom_format if row == last else col_format
            nm_fmt =  bottom_name if row == last else None

            self.worksheet.write(row, 0, name, nm_fmt)
            for i in range(3):
                self.worksheet.insert_checkbox(row, i+1, False, fmt)
        
            max_name_length = max(max_name_length, len(name))

        width = max_name_length * .95
        self.worksheet.set_column(0,0,width)

        #Other Categories
        headers = ["Tuesday Lecture", "Tuesday Lab", "Thursday Lecture"]
        for col, head in enumerate(headers, 1):
            self.worksheet.write(0,col, head, headers_format)
            self.worksheet.set_column(col, col, len(head) * .85)

        self.worksheet.write(0,5,"Attended Lab", headers_format)
        self.worksheet.set_column(4,5, width=len("Attended Lab"))

        for i in range(len(self.names)):
            fmt = bottom_format if i+1 == last else col_format
            self.worksheet.write_formula(i+1,5, f"=COUNTIF(C{i+2}, True)", fmt)


    def loadConfig(self) -> str | None:
        if os.path.exists("referencePath.json"):
            with open("referencePath.json", "r") as fr: 
                data = json.load(fr)

                return data
        else:
            return None

    def getNames(self) -> pd.DataFrame:
        if self.pathRef != None:
            names = read_csv(self.pathRef)

            names = names[(names["Sortable name"] != "Butler, Malachi")
            & (names["Sortable name"] != "Imbus, Jacob") &
            (names["Sortable name"] != "Lu, Lingma")]

            return names.dropna()