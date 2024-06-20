import discord
from redbot.core import commands


class TouchableMember(commands.MemberConverter):
    def __init__(self, response: bool = True):
        self.response = response
        super().__init__()


class Legacy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role = ""

    @commands.has_any_role()
    @commands.command()
    async def legacy(self, ctx, user: TouchableMember):
        """This is a legacy command."""
        await user.add_roles(self.role)
        await ctx.send(f"Added role to {user.display_name}.")
