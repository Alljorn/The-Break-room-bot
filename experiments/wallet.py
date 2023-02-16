import sqlite3 as sql

import discord
from discord.ext import commands

from experiments.config import MAIN_COLOUR, ERROR_COLOUR


class Wallet(commands.Cog):

    wallet = discord.SlashCommandGroup('wallet')

    def __init__(self):
        self.con = sql.connect('game/data/data_base.db')
        self.cur = self.con.cursor()

    def insert(self, author, value):
        self.cur.execute(f"""UPDATE user SET money = money + {value}
                         WHERE id = {author}""")
        self.con.commit()

    @wallet.command()
    async def amount(self, ctx):
        self.cur.execute(
            f"SELECT money FROM user WHERE id = {ctx.author.id}"
            )
        user = self.cur.fetchone()
        if not user:
            embed = discord.Embed(
                colour=ERROR_COLOUR,
                description="Vous devez d'abord vous enregistrer."
                )
            await ctx.send_response(emebed=embed)
            return
        embed = discord.Embed(colour=MAIN_COLOUR,
                              description=f"{user[0]} €")
        await ctx.send_response(embed=embed)


def setup(bot):
    bot.add_cog(Wallet())
