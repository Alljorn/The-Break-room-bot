import discord
from discord.ext import commands

from experiments.config import MAIN_COLOUR


class Network(commands.Cog):

    network = discord.SlashCommandGroup("network")

    def __init__(self, bot):
        self.bot = bot

    @network.command()
    async def post(self, ctx, message: str):
        netdata.append(message)

    @network.command()
    async def read(self, ctx):
        embed = discord.Embed(colour=MAIN_COLOUR, description=netdata[-1])
        await ctx.send_response(embed=embed)

    @network.command()
    async def colour(self, ctx, colour):
        embed = discord.Embed(colour=int(colour, 16), description="_ _")
        await ctx.send_response(embed=embed)


def setup(bot):
    bot.add_cog(Network(bot))


netdata = []
