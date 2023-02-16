import sqlite3 as sql

from experiments.calculus import Calculus


class Netdata:

    def __init__(self):
        self.con = sql.connect('experiments/netdata.db')
        self.cur = self.con.cursor()
        self.cur.execute("SELECT name FROM sqlite_master")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS message(author, content, value)"
            )
        self.con.commit()

    def add_message(self, author, msg):
        self.cur.execute("INSERT INTO message VALUES(?, ?, ?)",
                         (author, msg, Calculus.value(msg)))
        self.con.commit()

    def delete_messages(self):
        self.cur.execute("DELETE FROM message")
        self.con.commit()

    def get_message(self):
        self.cur.execute("SELECT author, content FROM message")
        return self.cur.fetchall()[-1]
