from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
INFO_CONFIG = CONFIG_DIR / "book_config.json"
STUDENT_CONFIG = CONFIG_DIR / "students_config.json"

curr_date = datetime.now().strftime("%d%m%Y")
WORKBOOK_FILENAME = f"AttendanceTabloid{curr_date}{hash(curr_date)}.xlsx"
TOTAL_WEEKS = 15
WEEK_SHEET_PREFIX = "Week "
LAB_ATTENDANCE_DIVISOR = 16