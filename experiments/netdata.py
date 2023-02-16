import sqlite3 as sql

from experiments.calculus import Calculus
from experiments.wallet import Wallet


class Netdata:

    def __init__(self):
        self.con = sql.connect('experiments/netdata.db')
        self.cur = self.con.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS message(author, title, content, value)"
            )
        self.delete_messages()
        self.wallet = Wallet()

    def insert_message(self, author, title, message):
        self.cur.execute("INSERT INTO message VALUES(?, ?, ?, ?)",
                         (author, title, message, Calculus.value(message)))
        self.con.commit()

    def delete_messages(self):
        self.cur.execute("DELETE FROM message")
        self.con.commit()

    def get_message(self):
        self.cur.execute("SELECT author, title, content, value FROM message")
        res = self.cur.fetchall()
        if not res:
            return None
        else:
            author, title, content, value = res[-1]
            self.wallet.insert(author, value)
            return author, title, content
