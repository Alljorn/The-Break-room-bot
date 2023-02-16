import sqlite3 as sql

import discord
from discord.ext import commands

from experiments.config import MAIN_COLOUR


class Wallet(commands.Cog):

    wallet = discord.SlashCommandGroup('wallet')

    def __init__(self):
        self.con = sql.connect('game/data/data_base.db')
        self.cur = self.con.cursor()

    @wallet.command()
    async def amount(self, ctx):
        self.cur.execute(
            f"SELECT money FROM user WHERE id = {ctx.author.id}"
            )
        embed = discord.Embed(colour=MAIN_COLOUR,
                              description=self.cur.fetchone())
        await ctx.send_response(embed=embed)


def setup(bot):
    bot.add_cog(Wallet())
