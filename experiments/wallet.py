import sqlite3 as sqlite

import discord
from discord.ext import commands


class Wallet(commands.Cog):

    wallet = discord.SlashCommandGroup('wallet')

    def __init__(self):
        self.con = sqlite.connect('game/data/data_base.db')
        self.cur = self.con.cursor()

    def insert(self, author_id, value):
        self.cur.execute(f"""UPDATE user SET money = money + {value}
                         WHERE id = {author_id}""")
        self.con.commit()

    @wallet.command()
    async def amount(self, ctx):
        self.cur.execute(f"SELECT money FROM user WHERE id = {ctx.author.id}")
        user = self.cur.fetchone()
        embed = discord.Embed(colour=0xA2A200, title="Votre Solde")
        if not user:
            self.cur.execute(f"""INSERT INTO user(id, money)
                             VALUES({ctx.author.id}, 0)""")
            self.con.commit()
            embed.description = "0 €"
        else:
            money = f"{user[0]:_.2f} €".replace('_', ' ')
            embed.description = money.replace('.', ',')
        await ctx.send_response(embed=embed)


def setup(bot):
    bot.add_cog(Wallet())
