import discord
from discord.ext import commands

from config.token import token
from config.bot import *


bot = commands.Bot(prefix, intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(bot.user)


@bot.tree.command(name='presenttion', description="Qu'est ce que The Break room ?")
async def presentation(interaction: discord.Interaction):
    await interaction.response.send_message("Trop de travail ? Prenez une pause !")


bot.run(token)
