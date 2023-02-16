import discord
from discord.ext import commands

from experiments.config import MAIN_COLOUR
from experiments.netdata import Netdata


class Network(commands.Cog):

    network = discord.SlashCommandGroup('network')

    def __init__(self, bot):
        self.bot = bot
        self.netdata = Netdata()

    @network.command()
    async def delete(self, ctx):
        self.netdata.delete_messages()
        embed = discord.Embed(colour=MAIN_COLOUR,
                              description="All the messages have been deleted.")
        await ctx.send_response(embed=embed)

    @network.command()
    async def post(self, ctx, msg):
        self.netdata.add_message(ctx.author.id, msg)
        embed = discord.Embed(
            colour=MAIN_COLOUR,
            description=f"You have posted the message: `{msg}`"
            )
        await ctx.send_response(embed=embed)

    @network.command()
    async def read(self, ctx):
        author, content = self.netdata.get_message()
        author = await self.bot.fetch_user(author)
        embed = discord.Embed(colour=MAIN_COLOUR, description=content)
        embed.set_author(name=author.name, icon_url=author.avatar.url)
        await ctx.send_response(embed=embed)

    @network.command()
    async def colour(self, ctx, colour):
        embed = discord.Embed(colour=int(colour, 16), description="_ _")
        await ctx.send_response(embed=embed)


def setup(bot):
    bot.add_cog(Network(bot))
