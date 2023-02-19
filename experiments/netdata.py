import sqlite3 as sqlite

from datetime import datetime, timezone

from experiments.calculus import Calculus


class Netdata:

    def __init__(self):
        self.con = sqlite.connect('experiments/netdata.db')
        self.con.row_factory = sqlite.Row
        self.cur = self.con.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS
            message(author, title, content, value, timestamp)"""
            )
        # self.delete_messages()

    def insert_message(self, author, title, message):
        self.cur.execute(
            "INSERT INTO message VALUES(?, ?, ?, ?, ?)",
            (author, title, message, Calculus.value(message),
             datetime.now(timezone.utc).timestamp())
            )
        self.con.commit()

    def delete_messages(self):
        self.cur.execute("DELETE FROM message")
        self.con.commit()

    def get_message(self):
        self.cur.execute(
            "SELECT author, title, content, value, timestamp FROM message"
            )
        return self.cur.fetchall()[-5:None]
