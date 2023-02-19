from datetime import datetime

import discord
from discord import InputTextStyle
from discord.ext import commands, tasks
from discord.ui import InputText

from experiments.netdata import Netdata
from experiments.wallet import Wallet


class Network(commands.Cog):

    network = discord.SlashCommandGroup('network')

    def __init__(self, bot):
        self.bot = bot
        self.netdata = Netdata()

    @network.command()
    async def receive(self, ctx):
        data = self.netdata.get_message()
        if not data:
            embed = discord.Embed(
                colour=0x00A2A2,
                description="Soyer le premier à poster sur le net."
                )
            await ctx.send_response(embed=embed)
        else:
            embed = discord.Embed(colour=0x00A2A2)
            for i in range(len(data)):
                author = await self.bot.fetch_user(data[i]['author'])
                title = f"{i+1} — {data[i]['title']} envoyé par {author.name}"
                text = f"Ce message sera supprimé \
                    <t:{int(data[i]['timestamp']) + 86400}:R>."
                embed.add_field(name=title, value=text, inline=False)
                await ctx.send_response(embed=embed, view=MessageChoose(data))

    @network.command()
    async def send(self, ctx):
        await ctx.send_modal(PostModal(ctx.author.id))

    @tasks.loop(hours=24)
    async def refresh(self):
        self.netdata.delete_messages()


class MessageChoose(discord.ui.View):

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.wallet = Wallet()
        for i in range(len(data), 5):
            self.remove_item(self.children[-1])

    def act(self, i):
        embed = discord.Embed(
            colour=0x00A2A2,
            title=self.data[i]['title'],
            description=self.data[i]['content'],
            timestamp=datetime.fromtimestamp(self.data[i]['timestamp'])
            )
        self.wallet.insert(self.data[i]['author'], self.data[i]['value'])
        return embed

    async def on_timeout(self):
        for child in self.children:
            self.remove_item(child)
        await self.message.edit(view=self)

    @discord.ui.button(label='1')
    async def callback_1(self, button, interaction):
        button.disabled = True
        await self.message.edit(view=self)
        await interaction.response.send_message(
            embed=self.act(0), ephemeral=True, view=MessageLike()
            )

    @discord.ui.button(label='2')
    async def callback_2(self, button, interaction):
        button.disabled = True
        await self.message.edit(view=self)
        await interaction.response.send_message(
            embed=self.act(1), ephemeral=True, view=MessageLike()
            )

    @discord.ui.button(label='3')
    async def callback_3(self, button, interaction):
        button.disabled = True
        await self.message.edit(view=self)
        await interaction.response.send_message(
            embed=self.act(2), ephemeral=True, view=MessageLike()
            )

    @discord.ui.button(label='4')
    async def callback_4(self, button, interaction):
        button.disabled = True
        await self.message.edit(view=self)
        await interaction.response.send_message(
            embed=self.act(3), ephemeral=True, view=MessageLike()
            )

    @discord.ui.button(label='5')
    async def callback_5(self, button, interaction):
        button.disabled = True
        await self.message.edit(view=self)
        await interaction.response.send_message(
            embed=self.act(4), ephemeral=True, view=MessageLike()
            )


class MessageLike(discord.ui.View):

    async def on_timeout(self):
        for child in self.children:
            self.remove_item(child)
        await self.message.edit(view=self)

    @discord.ui.button(label='Like', style=discord.ButtonStyle.green)
    async def callback_like(self, button, interact):
        embed = discord.Embed(colour=0x00A2A2,
                              description="You liked the message.")
        await interact.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label='Dislike', style=discord.ButtonStyle.red)
    async def callback_dislike(self, button, interact):
        embed = discord.Embed(colour=0x00A2A2,
                              description="You liked the message.")
        await interact.response.edit_message(embed=embed, view=None)


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
