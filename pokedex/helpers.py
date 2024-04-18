import discord
import textwrap

from discord.ext import commands


async def construct_embed(index: dict, embed: discord.Embed):
    for element, value in index.items():
        if value and len(str(value)) <= 1024:
            embed.add_field(name=element, value="\n".join(textwrap.wrap(str(value), 25)))
        elif value and len(str(value)) > 1024:
            embed.add_field(name=element, value="Value too long to display.")
        else:
            embed.add_field(name=element, value="N/A")

