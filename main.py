import discord
from discord.ext import commands

from config.token import token
from config.bot import *


bot = commands.Bot(prefix, intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(bot.user)


bot.run(token)
