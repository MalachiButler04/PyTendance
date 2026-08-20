# PyTendance

PyTendance is a desktop application for creating and editing attendance workbooks from a photo roster CSV. It uses a simple GUI to collect roster data, theme preferences, and term information, then generates an Excel workbook with weekly attendance sheets and summary tabs.

## Features

- Create a new attendance workbook from a photo roster CSV
- Record the TA's name (persists across new workbooks once entered)
- Choose a workbook theme color
- Select the term and class meeting days
- Choose where the generated workbook is saved
- Generate weekly worksheets with attendance checkboxes
- View summary sheets for weekly results and total labs attended
- Add or remove students from an existing workbook
- Rebuild the workbook automatically after roster changes

## Requirements

- Python 3.10 or newer
- pandas
- ttkbootstrap
- xlsxwriter
- Pillow (used to render the landing screen icon)

PyInstaller is an additional requirement only if you want to build a standalone executable (see [Building a standalone executable](#building-a-standalone-executable)).

## Installation

1. Clone or download this project.
2. Install the Python dependencies:

```bash
pip install pandas ttkbootstrap xlsxwriter openpyxl Pillow
```

`openpyxl` is included because pandas uses it when reading Excel files.

## Running the application

Start the program with:

```bash
python main.py
```

## How it works

When the app opens, you can choose one of two options:

- New Workbook: creates a fresh workbook from a CSV roster
- Edit Workbook: updates an existing workbook by adding or removing students

### New Workbook flow

1. Select a photo roster CSV file.
2. If a TA name has not already been recorded, enter your first and last name. This name must match a name already present in the uploaded roster, and it is remembered for future workbooks (it is not cleared by "New Workbook").
3. Choose a color theme.
4. Select the term and class days.
5. Choose a folder to save the workbook in (if you cancel the folder picker, it is saved to the project folder instead).
6. The app generates a uniquely named Excel workbook (for example `AttendanceTabloid20082026-2782719671219672689.xlsx`) in that folder and opens it automatically.

### Edit Workbook flow

If workbook data already exists, you can:

- Add Student by uploading an updated roster CSV
- Remove Student by selecting a student from the list

The recorded TA is hidden from the Add/Remove Student lists, so it cannot be accidentally removed, but the TA still appears as a normal student row in the generated workbook.

After changes are made, the workbook is rebuilt so the summary sheets stay synchronized.

If the generated workbook file is currently open in Excel, adding or removing a student (or starting the app's edit flow) will show an error asking you to close it first.

> **⚠️ Save your Excel file before editing students.** Adding or removing a student rebuilds the workbook from the last **saved** version of the file on disk — it does not read whatever is currently open and unsaved in Excel. If you have checked attendance boxes or made other changes in Excel and haven't saved, closing Excel to run an edit will discard those unsaved changes; the rebuilt workbook will revert to the previous saved state instead of preserving your latest edits. Always save (Ctrl+S) and close the workbook in Excel before adding or removing a student.

## Configuration files

The app stores its working data in the config folder:

- config/book_config.json: workbook settings such as roster path, theme, term, days, the recorded TA name, and the folder/filename the workbook was last saved to
- config/students_config.json: list of students used to build the workbook

## Output

The generated workbook is saved with a unique, timestamp-based filename (for example `AttendanceTabloid20082026-2782719671219672689.xlsx`) in the folder you choose during workbook creation. If no folder is chosen, it defaults to the project folder.

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

2. From the project root, run the rebuild script for your platform — [rebuild_app.bat](rebuild_app.bat) on Windows or [rebuild_app.sh](rebuild_app.sh) on macOS/Linux. Re-run the same script any time the code changes to rebuild the executable with your latest changes.

Alternatively, run PyInstaller directly:

```bash
python -m PyInstaller PyTendance.spec --noconfirm
```

The build produces a single `PyTendance.exe`, bundling the app alongside `assets/` and the default `config/` files referenced in `PyTendance.spec`. It is written straight to your Desktop (the OneDrive-redirected Desktop is used automatically if present), overwriting any previous build there.

## Notes

- The roster CSV must contain a column named Sortable name.
- The application ignores the student Lu, Lingma when importing roster data.
- The TA name you enter must exactly match a name already in the uploaded roster, or it will be rejected.
- "New Workbook" resets the roster path, theme, term, days, and saved workbook location, but does not clear the previously recorded TA name.
- Closing the app during workbook creation will reset progress.
- **Always save the workbook in Excel before adding or removing a student.** Edits are rebuilt from the last saved file on disk, so unsaved changes made in Excel will be lost, and the workbook will revert to its previous saved state.
