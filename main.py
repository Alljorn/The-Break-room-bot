import discord
from discord.ext import commands

from config.token import token
from config.bot import *

from the_break_room import *


bot = commands.Bot(prefix, intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(bot.user)


@bot.tree.command(name='presenttion', description="Qu'est ce que The Break room ?")
async def presentation(interaction: discord.Interaction):
    await interaction.response.send_message("Trop de travail ? Prenez une pause !")


@bot.tree.command(name='distributeur', description="Se rendre au distributeur")
async def distributeur(interaction: discord.Interaction):
    embed = discord.Embed(title="Le Distributeur", description="Vous êtes devant le distributeur")
    content = distributor.get_stock()
    for slot in content:
        embed.add_field(name=str(slot), value=content[slot], inline=True)
    await interaction.response.send_message(embed=embed)


bot.run(token)
