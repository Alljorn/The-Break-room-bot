import sqlite3 as sql

from experiments.calculus import Calculus
from experiments.wallet import Wallet


class Netdata:

    def __init__(self):
        self.con = sql.connect('experiments/netdata.db')
        self.cur = self.con.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS message(author, content, value)"
            )
        self.con.commit()
        self.wallet = Wallet()

    def add_message(self, author, message):
        self.cur.execute("INSERT INTO message VALUES(?, ?, ?)",
                         (author, message, Calculus.value(message)))
        self.con.commit()

    def delete_messages(self):
        self.cur.execute("DELETE FROM message")
        self.con.commit()

    def get_message(self):
        self.cur.execute("SELECT author, content, value FROM message")
        author, content, value = self.cur.fetchall()[-1]
        self.wallet.insert(author, value)
        return author, content
