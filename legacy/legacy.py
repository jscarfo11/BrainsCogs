import discord
from redbot.cogs.mod.utils import is_allowed_by_hierarchy
from redbot.core import commands


class TouchableMember(commands.MemberConverter):
    def __init__(self, response: bool = True):
        self.response = response
        super().__init__()


class Legacy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role = 1169638210205388920

    @commands.has_any_role(1188264672370098207, 878727109143580683, 810013892670521364)
    @commands.command()
    async def legacy(self, ctx, user: discord.Member):
        """This is a legacy command."""
        await self.bot.add_roles(user, self.role)
        await ctx.send(f"Added the role to {user.mention}.")
