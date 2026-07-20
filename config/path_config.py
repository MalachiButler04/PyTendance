from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent 
INFO_CONFIG = BASE_DIR / "config" / "book_config.json"
STUDENT_CONFIG = BASE_DIR / "config" / "students_config.json"