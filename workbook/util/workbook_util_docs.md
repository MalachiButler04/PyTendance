# Workbook Folder Documentation

## Overview

The `workbook` folder contains the code that builds, edits, and regenerates the attendance workbook used by PyTendance. It is responsible for turning roster data and user selections into a formatted Excel file with weekly attendance sheets, summary results, and total lab counts.

The folder is split into two main parts:

- `workbook/__init__.py`: package marker
- `workbook/util/`: user-facing workbook tools and workbook generation logic

This folder is the core of the application because it contains the classes that create the Excel workbook and manage student changes after the workbook already exists.

## Folder Structure

### `workbook/util/`

| File                    | Purpose                                                                                                    |
| ----------------------- | ---------------------------------------------------------------------------------------------------------- |
| `tabloid.py`            | Builds the Excel workbook, creates sheets, writes formulas, and rebuilds the workbook after roster changes |
| `student_manager.py`    | Adds and removes students from an existing workbook and triggers regeneration                              |
| `color_chooser.py`      | Provides the GUI for selecting the workbook theme color                                                    |
| `term_chooser.py`       | Provides the GUI for selecting the term and class meeting days                                             |
| `workbook_util_docs.md` | Documentation for the workbook folder                                                                      |

## High-Level Workflow

The workbook workflow follows this general sequence:

1. The user starts a new workbook from the main application.
2. A roster CSV is imported and student names are stored in the config files.
3. The user selects a theme color.
4. The user selects a term and the class meeting days.
5. The user picks a save folder, and `Tabloid` generates a uniquely named `.xlsx` file there. The chosen folder/filename are saved to `book_config.json` as `book-ref`/`book-name`.
6. If the workbook already exists, `StudentManager` can add or remove students.
7. After edits, the workbook is rebuilt (at the path resolved by `resolve_workbook_path()`) so all summary sheets stay in sync — provided the workbook was saved in Excel beforehand.

## Module Documentation

## `tabloid.py`

`tabloid.py` is the main workbook engine. It creates the output workbook, formats sheets, writes formulas, and handles rebuilds when the roster changes.

### Class: `Tabloid`

#### Purpose

`Tabloid` creates and manages the Excel workbook. It reads student and configuration data from the JSON files in `config/`, then uses `xlsxwriter` to generate the workbook.

#### Important attributes

- `self.weeks`: list of workbook sheet names such as `Week 1`, `Week 2`, and so on
- `self.students`: current student list loaded from config
- `self.output_path`: the path the workbook is written to — either the explicit `output_path` passed to the constructor, or the fallback `WORKBOOK_FILENAME`
- `self.wb`: active `xlsxwriter.Workbook` instance
- `self.ref`, `self.color`, `self.term`, `self.days`, `self.ta`, `self.bn`, `self.br`: workbook settings loaded from configuration, including the recorded TA name (`self.ta`) and the last saved workbook filename/folder (`self.bn`/`self.br`)
- `self.header_format`: formatted header style used across sheets
- `self.centered_vals`: centered cell format without borders
- `self.centeredwborder`: centered cell format with borders

#### Constructor

`Tabloid(skip_init: bool = False, output_path: str | None = None)`

When `skip_init` is `False`, the workbook is created immediately at `output_path` (or the fallback `WORKBOOK_FILENAME` if `output_path` is not given). When `True`, the instance is prepared for regeneration without writing a new workbook right away — this is the mode `StudentManager` uses before calling `rebuild_workbook()`, which writes to the path resolved by `resolve_workbook_path()` instead.

#### Methods

##### `init_workbook()`

Creates the workbook in this order:

1. `results_page()`
2. One weekly sheet for each value in `TOTAL_WEEKS`
3. `attended_labs_page()`
4. Close the workbook file

##### `results_page()`

Creates the `Results` sheet.

This sheet contains:

- Student names in the first column
- One column per week
- A `Total Attended` column at the end

Each weekly cell uses a formula that points back to the matching weekly sheet. The total attended value is calculated by summing the weekly values.

Conditional formatting is also applied so attendance totals are color-coded by value.

##### `week_sheet(week: int)`

Creates a weekly attendance sheet for a given week number.

Each sheet includes:

- `Names`
- Lecture and lab columns for the selected meeting days
- `Attended Help Session?`
- `EOW Summary`
- `Attended Lab`

The sheet inserts checkboxes for attendance fields and writes formulas that count checked boxes.

##### `week_sheet_with_data(week: int, WEEK_FRAME)`

Creates a weekly sheet using existing workbook data.

This method is used when the workbook is being rebuilt after a student is added or removed. It reads the saved weekly data, matches rows by student name, and restores checkbox values where available.

##### `attended_labs_page()`

Creates the `Total Labs Attended` sheet.

This sheet shows:

- Student names
- Total labs attended
- Attendance percentage

The formulas sum attendance across all weekly sheets.

##### `rebuild_workbook()`

Deletes the old workbook file and regenerates it using the latest student data.

This method is used after roster edits to keep the workbook consistent.

##### `load_students()`

Reads the student list from `config/students_config.json`.

##### `load_config()`

Reads the workbook configuration from `config/book_config.json` and returns `(ref, color, term, days, TA, book_name, book_ref)`.

##### `resolve_workbook_path()` (module-level function)

Calls `load_config()` and, if both `book_ref` and `book_name` are set, returns the joined path (`Path(book_ref) / book_name`) as a string. Otherwise falls back to `WORKBOOK_FILENAME`.

This is the single source of truth for "where is the current workbook file," used by `rebuild_workbook()`, `wb_closed()` in `main.py`, and `StudentManager.init_data()`. A near-identical copy of this function is also defined in `workbook/util/student_manager.py` — keep both in sync if the resolution logic changes.

### Workbook sheet output

The generated workbook contains three main areas:

#### `Results`

- One row per student
- One column per week
- One total column
- Conditional formatting for attendance totals

#### Weekly sheets

Each weekly sheet contains attendance checkboxes and summary formulas.

#### `Total Labs Attended`

This sheet summarizes total labs and percentage attendance across all weeks.

### Key workbook constants

`tabloid.py` depends on these values from `config/path_config.py`:

- `WORKBOOK_FILENAME`: output file name
- `TOTAL_WEEKS`: number of weekly sheets to generate
- `WEEK_SHEET_PREFIX`: prefix used to name weekly sheets
- `LAB_ATTENDANCE_DIVISOR`: divisor used when calculating attendance percentage

---

## `student_manager.py`

`student_manager.py` handles editing an existing workbook after it has already been created.

### Class: `StudentManager`

#### Purpose

This class provides the add and remove student workflows for the edit mode of the application.

#### Important attributes

- `self.students`: current roster list, with the TA filtered out
- `self.ref`: source CSV path stored in config
- `self.color`: theme color stored in config
- `self.days`: class meeting days stored in config
- `self.TA`: the recorded TA name loaded from `book_config.json`
- `self.FRAMES`: in-memory copy of week sheet data
- `self.STUDENTS`: shared student list used during edit actions, also excluding the TA
- Class-level mirrors `StudentManager.FRAMES`, `StudentManager.STUDENTS`, `StudentManager.REF`, `StudentManager.COLOR`, `StudentManager.DAYS`, `StudentManager.TA`: synchronized from the instance via `_sync_class_state()` after every state change, since `Tabloid.rebuild_workbook()` reads `StudentManager.FRAMES` directly as a class attribute

#### Methods

##### `_load_students()`

Loads the student list from `config/students_config.json` and removes the recorded TA name, if present, so the TA never appears in the Add/Remove Student screens.

##### `_save_students()`

Writes `self.students` back to `students_config.json`, re-adding the TA to the saved list if it was already present (since `self.students` never includes the TA).

##### `_save_roster_reference(roster_path)`

Updates `ref` in `book_config.json` to the newly uploaded roster path after `add_student()` succeeds.

##### `_reload_state()`

Reloads the stored configuration (including `TA`, `ref`, `color`, `days`) and re-derives `self.students` and the cached week-sheet frames via `init_data()`, then syncs the class-level mirrors.

##### `add_student()`

First checks `wb_closed()` (defined in `main.py`, checking the path from `resolve_workbook_path()`); if the workbook file is open elsewhere, the operation is aborted with an error message.

Imports a new roster CSV, validates that it contains a `Sortable name` column, and adds only students that are not already present.

Important behavior:

- Ignores duplicate names
- Ignores `Lu, Lingma`
- Ignores the recorded TA name (`self.TA`), so the TA is never added as a duplicate student row
- Updates `students_config.json` and `ref` in `book_config.json`
- Calls `Tabloid(skip_init=True).rebuild_workbook()` to refresh the workbook, then reloads state via `_reload_state()`

##### `remove_student()`

Shows the remove-student interface and lets the user select a student to delete. Like `add_student()`, it first checks `wb_closed()` and aborts with an error if the workbook file is currently open elsewhere. Because the roster shown here comes from `self.STUDENTS`, the TA never appears as a removable option.

##### `build_student_dropdown(parent_frame)`

Creates the dropdown menu and confirmation buttons used for removal.

##### `remove_helper(student: str)`

Removes a student from all cached week data, updates the student list, rewrites the config file, and regenerates the workbook.

##### `back_to_edit()`

Returns the interface to the add/remove student menu.

##### `refresh_dropdown(option_menu, selected)`

Rebuilds the dropdown options for the current student list.

##### `init_data()`

Loads existing week sheets from the workbook (via `pandas.read_excel(resolve_workbook_path(), ...)`) and extracts the columns needed for rebuilds.

Because this reads the workbook file **from disk**, it only sees data that has been saved in Excel. Any attendance checkboxes ticked in an open, unsaved Excel session are invisible to this method — `wb_closed()` prevents editing while the file is *open*, but does not guarantee it was *saved* before being closed. If the file was closed without saving, `init_data()` will load the older saved state, and that older state is what the rebuilt workbook will contain.

### Edit-mode workflow

The edit workflow is intended to preserve the workbook structure while keeping data synchronized:

1. Load current workbook and config values
2. Add or remove students
3. Update `students_config.json`
4. Rebuild the workbook so all formulas and sheets stay aligned

---

## `color_chooser.py`

`color_chooser.py` provides the color selection screen for new workbook creation.

### Class: `ColorPicker`

#### Purpose

Lets the user choose a theme color before the workbook is created.

#### Behavior

- Displays a preview square with the selected color
- Shows the corresponding hex value
- Stores the selected theme in `book_config.json`
- Invokes the completion callback after confirmation

#### Color palette

The available theme names include:

- Dusty Rose
- Soft Pink
- Peach Cream
- Sage Green
- Mist Blue
- Powder Blue
- Sky Mist
- Lavender Gray
- Blush Lavender

#### Methods

##### `build_gui()`

Builds the selection interface.

##### `change_color(c)`

Updates the preview square and hex display when the selection changes.

##### `get_conf()`

Confirms the chosen color and writes it to `book_config.json`.

---

## `term_chooser.py`

`term_chooser.py` provides the final setup screen for choosing term and class meeting days.

### Constants

- `DEFAULT_TERM_VALUE`: placeholder value for term selection
- `DEFAULT_DAYS_VALUE`: placeholder value for day selection
- `TERM_OPTIONS`: available term values
- `DAY_OPTIONS`: available day pairs

### Class: `TermChooser`

#### Purpose

Lets the user choose the academic term and the two class meeting days used by the workbook.

#### Methods

##### `build_gui()`

Creates the term and days dropdowns and a submit button.

##### `config_info()`

Validates the selected values, confirms them with the user, and stores the result in `book_config.json`.

The chosen day pair is saved as a list, such as:

- `Monday, Wednesday`
- `Tuesday, Thursday`

---

## Configuration Files Used by the Workbook Folder

The workbook code reads and writes these files in `config/`:

### `book_config.json`

Stores workbook metadata:

- `ref`: path to the imported roster CSV
- `color`: selected theme hex value
- `term`: selected term
- `days`: selected class days
- `TA`: the recorded TA name; persists across new-workbook resets and is used to hide the TA from `StudentManager`'s Add/Remove screens
- `book-ref`, `book-name`: the folder and filename the workbook was last saved to; used by `resolve_workbook_path()` to locate the file for `wb_closed()` checks and rebuilds

### `students_config.json`

Stores the active student list used to build workbook sheets.

These files are critical because the workbook folder depends on them to rebuild the workbook after edits.

## Data Validation Rules

The workbook folder relies on several important assumptions:

- The roster CSV must contain a column named `Sortable name`
- Student names are normalized and title-cased before being stored
- `Lu, Lingma` is intentionally excluded when importing roster data
- The recorded TA name is excluded from `StudentManager`'s add/remove screens, but not from the roster used to build the workbook itself
- The workbook expects a valid existing config state when editing students

## Error Handling

The workbook code includes basic protection against invalid input:

- CSV parsing failures
- Missing required columns
- Empty selections in the color and term screens
- Removing a student without selecting one first
- Attempting to edit workbook data when no workbook exists
- Attempting to add or remove a student while the workbook file is open in another program (`wb_closed()` in `main.py`, checked against `resolve_workbook_path()`)

Most errors are reported through message boxes so the user can correct the issue in the GUI.

What is **not** currently detected or reported: an Excel workbook that was closed without saving. `wb_closed()` only checks whether the file can be opened for writing (i.e., is it currently locked by another program); it cannot tell whether the last close discarded unsaved edits. Users must save the workbook themselves before triggering an add/remove student action, or their unsaved attendance data will be silently lost on the next rebuild.

## Notes for Future Maintenance

- If the number of class weeks changes, update `TOTAL_WEEKS` in `config/path_config.py`.
- If the workbook filename changes, update `WORKBOOK_FILENAME` everywhere it is referenced.
- If new attendance fields are added, update both the weekly sheet writer and the rebuild logic.
- If you change the roster format, update the CSV validation in `main.py` and `student_manager.py`.

## Summary

The `workbook` folder is the engine of PyTendance. It turns configuration data and roster information into a structured Excel workbook, and it also keeps that workbook synchronized when students are added or removed later.
