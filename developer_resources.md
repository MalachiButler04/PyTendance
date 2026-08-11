# PyTendance Developer Resources

## Purpose

This page is the central reference for developers working on PyTendance. It summarizes the project structure, points to the more detailed documentation pages, and explains how to make changes without breaking the workbook generation flow.

Use this document as the starting point before editing application logic, configuration handling, workbook generation, or the GUI workflow.

## Project Overview

PyTendance is a desktop application for creating and editing attendance workbooks from a photo roster CSV. The application guides the user through roster selection, theme selection, term setup, and workbook generation, then builds a formatted Excel file with weekly attendance sheets and summary tabs.

The project is organized around three main areas:

- Application entry and screen flow in [README.md](README.md)
- Persistent settings and runtime state in [config/config_docs.md](config/config_docs.md)
- Workbook creation and edit workflows in [workbook/util/workbook_util_docs.md](workbook/util/workbook_util_docs.md)

## Documentation Index

### Project Overview

- [README.md](README.md) — user-facing project summary, installation, and run instructions

### Config Layer

- [config/config_docs.md](config/config_docs.md) — details about config files, constants, and runtime state
- [config/path_config.py](config/path_config.py) — shared path and workbook constants

### Workbook Layer

- [workbook/util/workbook_util_docs.md](workbook/util/workbook_util_docs.md) — detailed workbook generation and student editing documentation
- [workbook/util/tabloid.py](workbook/util/tabloid.py) — workbook engine
- [workbook/util/student_manager.py](workbook/util/student_manager.py) — add/remove student flows
- [workbook/util/color_chooser.py](workbook/util/color_chooser.py) — theme selection UI
- [workbook/util/term_chooser.py](workbook/util/term_chooser.py) — term and meeting-day selection UI

## Architecture Summary

### Runtime flow

1. The user starts the app from `main.py`.
2. The app loads or resets data in the config folder (the recorded TA name is preserved across resets).
3. The user imports a roster CSV.
4. If no TA name is recorded yet, the user enters one and it is validated against the imported roster.
5. The user chooses a color theme.
6. The user chooses the term and meeting days.
7. `Tabloid` creates the workbook.
8. If the workbook already exists, `StudentManager` can add or remove students (excluding the TA from that list) and then rebuild the workbook. Both actions first confirm the workbook file isn't open elsewhere via `wb_closed()`.

### Source of truth

- `book_config.json` stores workbook settings such as roster path, color, term, days, and the recorded TA name.
- `students_config.json` stores the active student list.
- `path_config.py` stores shared constants for file names and sheet naming.

These files must remain in sync with the workbook code, because the workbook builder depends on them to render the correct sheets and formulas.

## Code Ownership by Area

### `main.py`

Handles top-level app flow, screen transitions, roster import, reset behavior, and startup actions.

### `config/`

Stores persistent state and shared constants. Changes here affect every part of the application.

### `workbook/util/`

Contains the UI helpers and workbook engine used to generate or rebuild the Excel file.

## GUI Element Map

This section shows where the main user interface pieces live and which files should be edited when a visual or workflow change is needed.

### Main window and primary navigation

The initial application window, including the main title, size, icon, and entry buttons, is defined in [main.py](main.py).

Edit `Main.init_main()` when changing:

- the main window size or title
- the application icon
- the primary `New Worksheet` button
- the primary `Edit Worksheet` button
- the initial layout of the landing screen

Edit `Main.__init__()` when changing:

- the top banner text
- the small credit label shown on the main screen

### New workbook flow

The step-by-step workbook creation flow is split across multiple classes:

- [main.py](main.py): controls the order of screens and switches between steps
- [workbook/util/color_chooser.py](workbook/util/color_chooser.py): color selection screen
- [workbook/util/term_chooser.py](workbook/util/term_chooser.py): term and day selection screen

Edit `Main.init_workbook()` when changing the warning prompt before a new workbook is created.

Edit `Main.upload_roster()` when changing:

- the roster file picker
- the accepted file types
- roster validation behavior
- the way imported names are written into config

Edit `Main.get_name()` when changing:

- the TA name entry screen shown after roster upload
- validation that the entered TA name exists in the imported roster
- how the TA name is written to `book_config.json`

Edit `Main.has_name()` when changing whether a recorded TA name causes the TA entry screen to be skipped.

Edit `ColorPicker.build_gui()` when changing:

- the color preview box
- the dropdown placement
- the submit button for color confirmation

Edit `ColorPicker.hex_vals` when adding, removing, or renaming theme options.

Edit `TermChooser.build_gui()` when changing:

- the term dropdown
- the meeting-day dropdown
- the submit button for term confirmation

Edit `TERM_OPTIONS` or `DAY_OPTIONS` when changing the available selections.

### Edit workbook flow

The add and remove student interface lives in [workbook/util/student_manager.py](workbook/util/student_manager.py).

Edit `Main.init_student_manager()` when changing the initial edit-mode menu shown after the workbook already exists.

Edit `StudentManager.add_student()` when changing:

- the file picker for updated roster uploads
- validation for the uploaded CSV
- the success and error messages shown after import

Edit `StudentManager.remove_student()` and `StudentManager.build_student_dropdown()` when changing:

- the remove-student screen layout
- the student dropdown
- the submit and back buttons
- the confirmation flow before deletion

Edit `StudentManager.back_to_edit()` when changing the layout of the edit-mode menu after a student has been added or removed.

### Reset and exit behavior

The actions that clear state or warn the user before leaving are in [main.py](main.py).

Edit `Main.on_exit_create()` when changing the exit confirmation dialog shown during workbook creation.

Edit `Main.reset_json()` when changing how the application clears saved config values. Note that this method intentionally does not clear the `TA` field, so the recorded TA name survives a reset.

### Workbook file lock check

`wb_closed()` in [main.py](main.py) checks whether `Attendance Tabloid.xlsx` can be opened for writing, and shows an error if it's currently open in another program (such as Excel). It is called before entering the edit-mode menu and before `StudentManager.add_student()` / `StudentManager.remove_student()` run.

Edit `wb_closed()` when changing this file-lock check or its error message.

### Where to look for common UI changes

| UI element                            | File to edit                                                         | Primary function or class                                         |
| ------------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Main title and landing screen buttons | [main.py](main.py)                                                   | `Main.init_main()`                                                |
| Credit label on the main window       | [main.py](main.py)                                                   | `Main.__init__()`                                                 |
| New workbook warning dialog           | [main.py](main.py)                                                   | `Main.init_workbook()`                                            |
| Roster file picker                    | [main.py](main.py)                                                   | `Main.upload_roster()`                                            |
| TA name entry screen                  | [main.py](main.py)                                                   | `Main.get_name()`                                                  |
| Theme color screen                    | [workbook/util/color_chooser.py](workbook/util/color_chooser.py)     | `ColorPicker.build_gui()`                                         |
| Color options                         | [workbook/util/color_chooser.py](workbook/util/color_chooser.py)     | `ColorPicker.hex_vals`                                            |
| Term and day selection screen         | [workbook/util/term_chooser.py](workbook/util/term_chooser.py)       | `TermChooser.build_gui()`                                         |
| Term/day options                      | [workbook/util/term_chooser.py](workbook/util/term_chooser.py)       | `TERM_OPTIONS`, `DAY_OPTIONS`                                     |
| Add/remove student menu               | [workbook/util/student_manager.py](workbook/util/student_manager.py) | `StudentManager.add_student()`, `StudentManager.remove_student()` |
| Remove-student dropdown and buttons   | [workbook/util/student_manager.py](workbook/util/student_manager.py) | `StudentManager.build_student_dropdown()`                         |
| Exit confirmation dialog              | [main.py](main.py)                                                   | `Main.on_exit_create()`                                           |

## Generated Excel Report Impact Map

This section shows where the workbook output is created and which files should be changed when you need to alter the generated Excel report itself.

### Workbook creation and layout

The Excel report is generated in [workbook/util/tabloid.py](workbook/util/tabloid.py).

Edit `Tabloid.init_workbook()` when changing:

- the order that sheets are created
- whether the workbook includes results, weekly, or summary sheets
- the overall workbook generation flow

Edit `Tabloid.results_page()` when changing:

- the `Results` sheet layout
- column headers for weekly results
- the total-attendance column
- conditional formatting rules for attendance totals

Edit `Tabloid.week_sheet()` when changing:

- the layout of newly created weekly sheets
- weekly column headers
- checkbox placement
- weekly summary formulas

Edit `Tabloid.week_sheet_with_data()` when changing:

- how existing weekly values are restored during workbook rebuilds
- how checkbox state is mapped back into the workbook
- how edited student data is preserved in weekly sheets

Edit `Tabloid.attended_labs_page()` when changing:

- the `Total Labs Attended` sheet layout
- total calculation formulas
- attendance percentage formulas

Edit `Tabloid.rebuild_workbook()` when changing:

- how the output workbook is regenerated after roster edits
- which cached data is reused during rebuilds
- how the old workbook file is removed before writing a new one

### Report data sources

The workbook output depends on the saved config files in [config/config_docs.md](config/config_docs.md) and the shared constants in [config/path_config.py](config/path_config.py).

Edit `Tabloid.load_students()` when changing:

- how the student list is read from disk
- the structure of the student roster config file

Edit `Tabloid.load_config()` when changing:

- how workbook settings are read from config
- which saved values are required before report generation

### Report constants that affect output

The following constants in [config/path_config.py](config/path_config.py) directly affect the report:

- `WORKBOOK_FILENAME`: output file name
- `TOTAL_WEEKS`: number of weekly sheets and result columns
- `WEEK_SHEET_PREFIX`: weekly sheet naming pattern
- `LAB_ATTENDANCE_DIVISOR`: divisor used in attendance percentage calculations

If any of these values change, the workbook formulas, sheet names, and summary totals may need to be updated at the same time.

### Student changes that affect the report

The workbook output also changes when student data changes in [workbook/util/student_manager.py](workbook/util/student_manager.py).

Edit `StudentManager.add_student()` when changing:

- how new students appear in the report
- how new names are merged into the workbook roster

Edit `StudentManager.remove_helper()` when changing:

- how removed students disappear from workbook sheets
- how rebuilt sheets preserve the remaining rows

Edit `StudentManager.init_data()` when changing:

- how existing weekly sheet data is loaded before rebuilding the report
- which columns are preserved from the current workbook

### Report behavior that depends on GUI selections

The generated workbook is also shaped by the setup screens:

- [main.py](main.py) controls the flow that stores selections before workbook creation
- [workbook/util/color_chooser.py](workbook/util/color_chooser.py) sets the header color used in the report
- [workbook/util/term_chooser.py](workbook/util/term_chooser.py) sets the day labels used in weekly sheet headers

If you change those screens, verify that the workbook still receives valid values before it is generated.

### Common report changes

| Report change | File to edit | Primary function or constant |
| --- | --- | --- |
| Add or remove workbook sheets | [workbook/util/tabloid.py](workbook/util/tabloid.py) | `Tabloid.init_workbook()` |
| Change results sheet columns | [workbook/util/tabloid.py](workbook/util/tabloid.py) | `Tabloid.results_page()` |
| Change weekly report layout | [workbook/util/tabloid.py](workbook/util/tabloid.py) | `Tabloid.week_sheet()` |
| Change rebuilt weekly data behavior | [workbook/util/tabloid.py](workbook/util/tabloid.py) | `Tabloid.week_sheet_with_data()` |
| Change total labs summary layout | [workbook/util/tabloid.py](workbook/util/tabloid.py) | `Tabloid.attended_labs_page()` |
| Change workbook file name | [config/path_config.py](config/path_config.py) | `WORKBOOK_FILENAME` |
| Change number of weeks in the report | [config/path_config.py](config/path_config.py) | `TOTAL_WEEKS` |
| Change report theme color source | [workbook/util/color_chooser.py](workbook/util/color_chooser.py) | `ColorPicker.get_conf()` |
| Change report day labels | [workbook/util/term_chooser.py](workbook/util/term_chooser.py) | `TermChooser.config_info()` |

## Contribution Guidelines

### Before making changes

1. Read the relevant documentation page first.
2. Identify whether the change affects UI flow, config state, or workbook output.
3. Check the current file contents before editing if another change has already been made.
4. Prefer small, focused changes that preserve existing behavior.

### When editing config-related code

Be careful to keep the following consistent:

- JSON structure in `book_config.json` and `students_config.json`
- file paths defined in `path_config.py`
- default values used by the UI
- reset behavior when starting a new workbook

If you add a new setting, update all of the following:

- the code that writes the setting
- the code that reads the setting
- the documentation in [config/config_docs.md](config/config_docs.md)

### When editing workbook generation

Changes in `tabloid.py` can affect every workbook sheet. Keep these rules in mind:

- preserve sheet names unless there is a strong reason to change them
- keep formulas aligned with row and column positions
- maintain compatibility with the student list stored in config
- update the rebuild path if new workbook data needs to be preserved

### When editing student management

Changes in `student_manager.py` should continue to:

- prevent duplicates
- preserve workbook rebuild behavior
- update the active student list in the config file
- handle missing or invalid roster uploads safely

### When editing the GUI

The app uses a step-by-step flow. Avoid introducing screen changes that skip required setup values.

If you change one of the setup screens, make sure:

- callbacks still fire in the correct order
- confirmation dialogs still guard destructive actions
- the app does not proceed with incomplete values

## Development Workflow

### Suggested workflow for a change

1. Identify the affected module.
2. Read the corresponding documentation.
3. Make the smallest change that solves the problem.
4. Check for obvious logic or formatting regressions.
5. Update documentation if behavior or file structure changes.

### Recommended validation checks

After a change, verify:

- the app still starts cleanly
- a new workbook can still be created from a valid roster CSV
- editing an existing workbook still works
- generated workbook sheet names and formulas still match expectations

If you change workbook formulas or sheet layout, test both:

- fresh workbook creation
- workbook rebuild after adding/removing students

## File Change Guidance

### Safe-to-edit areas

- text labels and helper messages
- documentation files
- UI layout details that do not alter required inputs
- additional non-breaking configuration fields with matching read/write logic

### High-risk areas

- changing workbook sheet names
- changing config file structure
- changing student name normalization
- changing formula addresses
- changing reset behavior

These areas have ripple effects across the project and should be updated carefully.

## Data Handling Rules

The project currently expects:

- a roster CSV with a `Sortable name` column
- title-cased student names in the stored roster list
- `Lu, Lingma` to be excluded during import
- exactly two meeting days selected for each workbook setup
- a recorded `TA` name that matches an existing student, which is excluded from `StudentManager`'s add/remove lists but still appears as a normal student row in the workbook

Any change to these assumptions should be reflected in the docs and in the workbook logic.

## Known Dependencies

The application currently depends on:

- Python 3.10 or newer
- pandas
- ttkbootstrap
- xlsxwriter
- openpyxl for Excel file reading through pandas

If dependencies change, update both [README.md](README.md) and any setup instructions that mention installation.

## Documentation Maintenance

When project behavior changes, update the most relevant documentation page first:

- user-facing installation or usage changes go in [README.md](README.md)
- config storage or runtime state changes go in [config/config_docs.md](config/config_docs.md)
- workbook generation or editing changes go in [workbook/util/workbook_util_docs.md](workbook/util/workbook_util_docs.md)

If a change spans multiple areas, update all affected docs together so the project stays easy to maintain.

## Quick Reference

- Start here: [developer_resources.md](developer_resources.md)
- User instructions: [README.md](README.md)
- Config details: [config/config_docs.md](config/config_docs.md)
- Workbook details: [workbook/util/workbook_util_docs.md](workbook/util/workbook_util_docs.md)

## Summary

PyTendance is built around a small set of tightly connected modules. The config folder stores state, the workbook folder generates the Excel output, and the main application coordinates the workflow. Keep changes narrow, preserve the existing data contracts, and update documentation whenever behavior changes.
