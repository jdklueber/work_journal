import os
from .db import DBManager

DATA_DIR = r"c:\data"

DIALECT = "sqlite"
HOST = ""
PATH = DATA_DIR + r"\work_journal.db"

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

db = DBManager(f"{DIALECT}://{HOST}/{PATH}")
