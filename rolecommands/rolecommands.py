import discord
from redbot.core import commands


class RoleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_legacy = 1169638210205388920
        self.role_cd = 1302064412689174528

    @commands.has_any_role(1188264672370098207, 878727109143580683, 810013892670521364)
    @commands.command()
    async def legacy(self, ctx, user: discord.Member):
        """This is a legacy command."""
        role = discord.utils.get(ctx.guild.roles, id=self.role_legacy)
        if role in user.roles:
            return await ctx.send(f"{user.name} already has the role.")
        await user.add_roles(role)
        text = "> With said role you no longer have to pay in order to access the premium bots\n> No other perks are included\n> So basically free premium after being a premium member for 1 year\n> You can cancel your current sub if you want."
        await ctx.send(text + f"\nAdded **{role.name}** to **{user.name}**.")

    @commands.has_any_role(1188264672370098207, 878727109143580683, 810013892670521364)
    @commands.command()
    async def cd(self, ctx, user: discord.Member):
        """This adds the cd role."""
        role = discord.utils.get(ctx.guild.roles, id=self.role_cd)
        if role in user.roles:
            return await ctx.send(f"{user.name} already has the role.")

        await user.add_roles(role)
        await ctx.send(f"Added **{role.name}** to **{user.name}**.")

    @commands.has_any_role(1188264672370098207, 878727109143580683, 810013892670521364)
    @commands.command(aliases=["free", "mc"])
    async def merrychristmas(self, ctx, user: discord.Member):
        """This adds the cd role."""
        role = discord.utils.get(ctx.guild.roles, id=self.role_cd)
        if role in user.roles:
            return await ctx.send(f"{user.name} already has the role.")

        await user.add_roles(role)
        await ctx.send(f"Added **{role.name}** to **{user.name}**.")
