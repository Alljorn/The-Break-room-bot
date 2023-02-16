import sqlite3 as sql

import discord
from discord.ext import commands


class Wallet(commands.Cog):

    wallet = discord.SlashCommandGroup('portefeuille')

    def __init__(self):
        self.con = sql.connect('game/data/data_base.db')
        self.cur = self.con.cursor()

    def insert(self, author_id, value):
        self.cur.execute(f"""UPDATE user SET money = money + {value}
                         WHERE id = {author_id}""")
        self.con.commit()

    @wallet.command(name='solde')
    async def amount(self, ctx):
        self.cur.execute(
            f"SELECT money FROM user WHERE id = {ctx.author.id}"
            )
        user = self.cur.fetchone()
        if not user:
            self.cur.execute(f"""INSERT INTO user(id, money)
                             VALUES({ctx.author.id}, 0)""")
            self.con.commit()
            embed = discord.Embed(colour=0xA2A200,
                                  description="0 €")
        else:
            money = f"{user[0]:_.2f} €".replace('_', ' ')
            embed = discord.Embed(colour=0xA2A200,
                                  description=money.replace('.', ','))
        await ctx.send_response(embed=embed)


def setup(bot):
    bot.add_cog(Wallet())
