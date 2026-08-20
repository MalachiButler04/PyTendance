# Config Folder Documentation

## Overview

The `config` folder stores the application settings and runtime data used by PyTendance. These files are read and updated by the GUI workflow, the workbook generator, and the student management features.

This folder is important because it keeps the workbook state persistent between sessions. Without these files, the application would not know which roster was imported, which theme was selected, which term is active, or which students belong in the workbook.

## Folder Contents

| File                   | Purpose                                                                     |
| ---------------------- | --------------------------------------------------------------------------- |
| `path_config.py`       | Central location for file paths, workbook constants, and naming conventions |
| `book_config.json`     | Stores workbook metadata such as roster path, theme, term, and class days   |
| `students_config.json` | Stores the current student roster used to build and rebuild the workbook    |
| `config_docs.md`       | Documentation for the config folder                                         |

## How the Config Folder Is Used

The application uses the config folder as its source of truth for workbook state.

Typical flow:

1. The user imports a photo roster CSV.
2. The app stores the roster path in `book_config.json`.
3. If no TA name is already recorded, the user enters their first and last name; it is validated against the roster and stored in `book_config.json` as `TA`.
4. The user selects a theme color.
5. The app stores the selected hex color in `book_config.json`.
6. The user selects a term and meeting days.
7. The app stores those values in `book_config.json`.
8. The roster names are stored in `students_config.json`.
9. The user picks a save folder; the workbook generator reads both JSON files to build the Excel workbook, then writes the resulting `book-ref` and `book-name` back into `book_config.json`.

When the user later adds or removes students, the config files are updated again so the regenerated workbook stays in sync.

## `path_config.py`

`path_config.py` defines the shared constants used across the project.

### Purpose

This module prevents hard-coded paths and repeated string values from being scattered through the codebase. It gives the application one place to define where config files live and what workbook naming rules should be used.

### Constants

#### `BASE_DIR`

The absolute root directory of the project.

This is calculated from the location of `path_config.py` and is used as the base for all other paths.

#### `CONFIG_DIR`

The path to the `config` folder.

#### `INFO_CONFIG`

Path to `book_config.json`.

This file stores workbook settings such as:

- roster path
- color theme
- term
- class days

#### `STUDENT_CONFIG`

Path to `students_config.json`.

This file stores the current active student list used by the workbook.

#### `WORKBOOK_FILENAME`

The fallback name used for the generated workbook file when no save location has been recorded yet (for example, the very first workbook created in a session, before `book-ref`/`book-name` exist in `book_config.json`).

This value is generated dynamically each time the app starts, from the current date and a hash of that date string, so it is unique per run rather than a fixed constant:

```python
curr_date = datetime.now().strftime("%d%m%Y")
WORKBOOK_FILENAME = f"AttendanceTabloid{curr_date}{hash(curr_date)}.xlsx"
```

Example value:

- `AttendanceTabloid20082026-2782719671219672689.xlsx`

Once a workbook has been saved, `resolve_workbook_path()` in `workbook/util/tabloid.py` prefers the `book-ref`/`book-name` values stored in `book_config.json` over this fallback.

#### `TOTAL_WEEKS`

The number of weekly worksheets created by the workbook generator.

Current value:

- `15`

#### `WEEK_SHEET_PREFIX`

The prefix used for weekly sheet names.

Current value:

- `Week `

This produces sheet names like `Week 1`, `Week 2`, and so on.

#### `LAB_ATTENDANCE_DIVISOR`

The divisor used when calculating the attendance percentage on the total labs sheet.

Current value:

- `16`

## `book_config.json`

`book_config.json` stores the user-selected workbook settings.

### Current structure

```json
{
  "ref": "...",
  "color": "#...",
  "term": "Fall or Spring",
  "days": ["Tuesday", "Thursday"],
  "TA": "Last, First",
  "book-name": "AttendanceTabloid20082026-2782719671219672689.xlsx",
  "book-ref": "C:/path/to/save/folder"
}
```

### Field reference

#### `ref`

The path to the imported photo roster CSV.

This is used when the workbook is first created and also when the user adds students later.

Expected value:

- a valid file path to a CSV roster

If no roster has been selected yet, this value is set to an empty string.

#### `color`

The selected workbook theme color stored as a hex value.

Example values:

- `#fce5cd`
- `#d9ead3`
- `#c9daf8`

This color is used for workbook headers and other formatted cells.

#### `term`

The selected academic term.

Current supported values:

- `Fall`
- `Spring`

This value is saved for reference and displayed in the setup workflow.

#### `days`

The selected class meeting days stored as a two-item list.

Example:

```json
["Tuesday", "Thursday"]
```

These values are used to label the weekly attendance sheets.

#### `TA`

The name of the teaching assistant using the app, stored in `Last, First` title-cased form, the same format used for student names.

This value is:

- collected once, the first time a workbook is created without a stored `TA` value
- validated against the current student roster before being saved (the entered name must match an existing student)
- read by `Tabloid` and `StudentManager` alongside the other `book_config.json` fields
- used by `StudentManager` to hide the TA from the Add/Remove Student lists, even though the TA remains a normal row in the generated workbook

If no roster has been selected yet, or before a TA has ever been entered, this value is an empty string.

#### `book-name`

The filename of the most recently generated workbook (for example `AttendanceTabloid20082026-2782719671219672689.xlsx`).

This is written by `Main.success_screen()` in `main.py` right after a new workbook is generated, and is read by `resolve_workbook_path()` in `workbook/util/tabloid.py` (and duplicated in `workbook/util/student_manager.py`) to locate the workbook for rebuilds and the `wb_closed()` file-lock check.

If empty, `resolve_workbook_path()` falls back to the dynamically generated `WORKBOOK_FILENAME` constant from `path_config.py`.

#### `book-ref`

The folder path the user chose to save the workbook in, selected via a folder picker shown after term/day confirmation. Used together with `book-name` to build the full workbook path.

If the user cancels the folder picker, the workbook is saved to `BASE_DIR` (the project root) instead, and `book-ref` is set accordingly.

### When this file changes

`book_config.json` is updated when:

- the user imports a roster CSV
- the user enters and confirms a TA name for the first time
- the user confirms a color theme
- the user confirms the term and meeting days
- a new workbook is generated (`book-name` and `book-ref` are written)
- students are added or removed (`ref` is rewritten to the newly uploaded roster path)
- the workbook is reset or cleared during a new workbook workflow

`TA` is the one exception: it is not cleared during a reset, so once recorded it persists across "New Workbook" runs until manually edited in the file.

## `students_config.json`

`students_config.json` stores the active student roster.

### Current structure

```json
{
  "students": ["Student Name 1", "Student Name 2"]
}
```

### Field reference

#### `students`

A list of student names used to populate workbook sheets.

The list is expected to contain title-cased names and should not include duplicates.

### How the list is built

When a roster CSV is loaded:

- the `Sortable name` column is read
- names are cleaned and title-cased
- duplicates are removed through sorting and normalization
- the student `Lu, Lingma` is intentionally excluded

When editing an existing workbook:

- new names are appended if they are not already present
- removed names are deleted from the list
- the workbook is regenerated from the updated list

### When this file changes

`students_config.json` is updated when:

- a new roster is imported
- students are added from an updated roster
- students are removed from the workbook
- the application resets stored data for a new workbook

## Data Flow Between Config Files and Workbook Generation

The config files directly support workbook creation:

- `book_config.json` tells the workbook generator what settings to use
- `students_config.json` tells the workbook generator which names to place into sheets

The workbook builder reads both files before writing the Excel output. When a student is added or removed, the updated list is saved first, then the workbook is rebuilt using the latest values.

## Validation and Assumptions

The config folder expects the following:

- `book_config.json` must be valid JSON
- `students_config.json` must be valid JSON
- the roster path stored in `ref` should point to a CSV file
- the roster CSV must contain a `Sortable name` column
- `days` must always contain exactly two entries for the workbook labels
- `book_config.json` must contain a `TA` key (even if empty), since `Tabloid.load_config()` and `StudentManager` read it unconditionally
- the `TA` value, once set, must match a name in `students_config.json`
- `book-name` and `book-ref`, once set, must together point to an existing, readable `.xlsx` file, since `StudentManager.init_data()` reads that file with `pandas.read_excel()` before any add/remove edit

If these assumptions are broken, parts of the application may fail to load workbook data correctly.

> **⚠️ Data integrity note:** Add/remove student edits are rebuilt from the workbook file at the path resolved from `book-ref`/`book-name` — that is, the last version **saved to disk**, not whatever is currently open and unsaved in Excel. The workbook must be saved (and closed, per `wb_closed()`) before an edit is made, or any unsaved attendance data in Excel will be lost when the workbook is rebuilt.

## Reset Behavior

The application can clear stored config values when starting a new workbook.

During a reset:

- `ref` is cleared
- `color` is cleared
- `term` is cleared
- `days` is reset to an empty list
- `book-ref` is cleared
- `book-name` is cleared
- `students` is reset to an empty list

`TA` is intentionally left untouched by reset, so the recorded TA name carries over into the next workbook instead of being re-entered every time.

This ensures that a new workbook starts from a clean state, aside from the persisted TA name.

## Notes for Maintenance

- Update `path_config.py` if the workbook filename changes.
- Update `TOTAL_WEEKS` if the semester length changes.
- Keep the JSON structures stable so the workbook and GUI code continue to read them correctly.
- If new settings are added later, document them here and update any code that reads or writes the config files.

## Summary

The `config` folder acts as persistent storage for PyTendance. It holds the workbook settings, the active student roster, and the shared constants needed to keep the application organized and consistent across sessions.
 