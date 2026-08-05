# PyTendance

PyTendance is a desktop application for creating and editing attendance workbooks from a photo roster CSV. It uses a simple GUI to collect roster data, theme preferences, and term information, then generates an Excel workbook with weekly attendance sheets and summary tabs.

## Features

- Create a new attendance workbook from a photo roster CSV
- Choose a workbook theme color
- Select the term and class meeting days
- Generate weekly worksheets with attendance checkboxes
- View summary sheets for weekly results and total labs attended
- Add or remove students from an existing workbook
- Rebuild the workbook automatically after roster changes

## Requirements

- Python 3.10 or newer
- pandas
- ttkbootstrap
- xlsxwriter

## Installation

1. Clone or download this project.
2. Install the Python dependencies:

```bash
pip install pandas ttkbootstrap xlsxwriter openpyxl
```

`openpyxl` is included because pandas uses it when reading Excel files.

## Running the application

Start the program with:

```bash
python main.py
```

## How it works

When the app opens, you can choose one of two options:

- New Worksheet: creates a fresh workbook from a CSV roster
- Edit Worksheet: updates an existing workbook by adding or removing students

### New Worksheet flow

1. Select a photo roster CSV file.
2. Choose a color theme.
3. Select the term and class days.
4. The app generates an Excel workbook named Attendance Tabloid.xlsx.

### Edit Worksheet flow

If workbook data already exists, you can:

- Add Student by uploading an updated roster CSV
- Remove Student by selecting a student from the list

After changes are made, the workbook is rebuilt so the summary sheets stay synchronized.

## Configuration files

The app stores its working data in the config folder:

- config/book_config.json: workbook settings such as roster path, theme, term, and days
- config/students_config.json: list of students used to build the workbook

## Output

The generated workbook is saved as:

```text
Attendance Tabloid.xlsx
```

It includes:

- Results
- Weekly attendance sheets
- Total Labs Attended

## Project structure

```text
main.py
config/
workbook/
assets/
```

## Notes

- The roster CSV must contain a column named Sortable name.
- The application ignores the student Lu, Lingma when importing roster data.
- Closing the app during workbook creation will reset progress.
