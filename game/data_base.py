import sqlite3
import os



DATA_BASE = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+'/data/data_base.db')
DATA_BASE.cursor().execute("PRAGMA foreign_keys = ON;")

try:
    cursor = DATA_BASE.cursor()
    cursor.execute(
    """CREATE TABLE "user" (
        "id"	INTEGER NOT NULL,
        "role"	TEXT NOT NULL,
        PRIMARY KEY("id"),
        FOREIGN KEY("role") REFERENCES "roles_ref"("name")
    );
    """)
    DATA_BASE.commit()
    print("table \"user\" created")
except sqlite3.OperationalError as err:
    print(err)

try:
    cursor = DATA_BASE.cursor()
    cursor.execute(
    """CREATE TABLE "roles_ref" (
        "name"	TEXT NOT NULL,
        PRIMARY KEY("name")
    );
    """)
    DATA_BASE.commit()
    print("table \"roles_ref\" created")
except sqlite3.OperationalError as err:
    print(err)