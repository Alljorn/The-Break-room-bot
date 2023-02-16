import discord
from discord import InputTextStyle
from discord.ext import commands, tasks
from discord.ui import InputText

from experiments.netdata import Netdata


class Network(commands.Cog):

    network = discord.SlashCommandGroup('réseau')

    def __init__(self, bot):
        self.bot = bot
        self.netdata = Netdata()

    @network.command(name='envoyer')
    async def post(self, ctx):
        await ctx.send_modal(PostModal(ctx.author.id))

    @network.command(name='recevoir')
    async def read(self, ctx):
        data = self.netdata.get_message()
        if not data:
            embed = discord.Embed(
                colour=0x00A2A2,
                description="Soyer le premier à poster sur le net."
                )
        else:
            author = await self.bot.fetch_user(data[0])
            embed = discord.Embed(colour=0x00A2A2, title=data[1],
                                  description=data[2])
            embed.set_author(name=author.name, icon_url=author.avatar.url)
        await ctx.send_response(embed=embed)

    @tasks.loop(hours=24)
    async def refresh(self):
        self.netdata.delete_messages()


class PostModal(discord.ui.Modal):

    def __init__(self, author_id):
        super().__init__(title="Post")
        self.author_id = author_id
        self.add_item(InputText(label="Titre", max_length=256, required=False))
        self.add_item(InputText(label="Contenu", style=InputTextStyle.long))

    async def callback(self, interaction):
        netdata = Netdata()
        netdata.insert_message(self.author_id, self.children[0].value,
                               self.children[1].value)
        await interaction.response.send_message("Votre message a été envoyé.")


def setup(bot):
    bot.add_cog(Network(bot))
