from .db import DBManager

DIALECT = "sqlite"
HOST = ""
PATH = r"c:\data\work_journal.db"

db = DBManager(f"{DIALECT}://{HOST}/{PATH}")
