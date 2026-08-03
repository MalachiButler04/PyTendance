from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
INFO_CONFIG = CONFIG_DIR / "book_config.json"
STUDENT_CONFIG = CONFIG_DIR / "students_config.json"
WORKBOOK_FILENAME = "Attendance Tabloid.xlsx"
TOTAL_WEEKS = 15
WEEK_SHEET_PREFIX = "Week "
LAB_ATTENDANCE_DIVISOR = 16