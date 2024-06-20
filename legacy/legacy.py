import discord
from redbot.core import commands


class Legacy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role = 1169638210205388920

    @commands.has_any_role(1188264672370098207, 878727109143580683, 810013892670521364)
    @commands.command()
    async def legacy(self, ctx, user: discord.Member):
        """This is a legacy command."""
        role = discord.utils.get(ctx.guild.roles, id=self.role)
        await user.add_roles(role)
        await ctx.send(f"Added the role to {user.mention}.")
