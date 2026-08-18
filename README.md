# PyTendance

PyTendance is a desktop application for creating and editing attendance workbooks from a photo roster CSV. It uses a simple GUI to collect roster data, theme preferences, and term information, then generates an Excel workbook with weekly attendance sheets and summary tabs.

## Features

- Create a new attendance workbook from a photo roster CSV
- Record the TA's name (persists across new workbooks once entered)
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

PyInstaller is an additional requirement only if you want to build a standalone executable (see [Building a standalone executable](#building-a-standalone-executable)).

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
2. If a TA name has not already been recorded, enter your first and last name. This name must match a name already present in the uploaded roster, and it is remembered for future workbooks (it is not cleared by "New Worksheet").
3. Choose a color theme.
4. Select the term and class days.
5. The app generates an Excel workbook named Attendance Tabloid.xlsx.

### Edit Worksheet flow

If workbook data already exists, you can:

- Add Student by uploading an updated roster CSV
- Remove Student by selecting a student from the list

The recorded TA is hidden from the Add/Remove Student lists, so it cannot be accidentally removed, but the TA still appears as a normal student row in the generated workbook.

After changes are made, the workbook is rebuilt so the summary sheets stay synchronized.

If the generated workbook file is currently open in Excel, adding or removing a student (or starting the app's edit flow) will show an error asking you to close it first.

## Configuration files

The app stores its working data in the config folder:

- config/book_config.json: workbook settings such as roster path, theme, term, days, and the recorded TA name
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
PyTendance.spec
```

## Building a standalone executable

PyTendance can be packaged into a standalone executable with [PyInstaller](https://pyinstaller.org/), using the included [PyTendance.spec](PyTendance.spec) file.

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. From the project root, run:

```bash
python -m PyInstaller PyTendance.spec
```

The build output is written to `dist/PyTendance/`, bundling the app alongside `assets/` and the default `config/` files referenced in `PyTendance.spec`.

## Notes

- The roster CSV must contain a column named Sortable name.
- The application ignores the student Lu, Lingma when importing roster data.
- The TA name you enter must exactly match a name already in the uploaded roster, or it will be rejected.
- "New Worksheet" resets the roster path, theme, term, and days, but does not clear the previously recorded TA name.
- Closing the app during workbook creation will reset progress.
