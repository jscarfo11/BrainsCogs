import discord
import asyncio

from redbot.core import Config, commands
from redbot.core.utils.predicates import MessagePredicate


class SwitchCodes(commands.Cog):
    """Store and retrieve Nintendo Switch friend codes."""
    
    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=296058336787300353)
        default_guild = {
            "codes": {},
        }
        self.config.register_guild(**default_guild)
        self.bot = bot
        
        return
    
    @commands.group(invoke_without_command=True, aliases = ["friendcode"])
    async def fc(self, ctx, *, user: discord.Member or int or None):
        """Search someone else's friend code"""
        if isinstance(user, int):
            user = self.bot.get_user(user)
        elif user is None:
            user = ctx.author
        code = await self.config.guild(ctx.guild).codes.get_raw(str(user.id), default=None)
        if code is None:
            await ctx.send("That user has not set their Friend Code.")
        else:
            embed = discord.Embed(colour=user.colour, title=f"{user.display_name}'s Friend Code", description=f"SW-{code}")
            await ctx.send(embed=embed)
        await ctx.tick()
        
        return
    
    @fc.command()
    async def add(self, ctx, code: str):
        """Set your friend code"""
        if len(code) > 12:
            await ctx.send("That code is too long. Expected length is `12` Please try again.")
            return
        elif len(code) < 12:
            await ctx.send("That code is too short. Expected length is `12` Please try again.")
            return
        async with self.config.guild(ctx.guild).codes() as codes:
            codes[str(ctx.author.id)] = f'{str(code)[:4]}-{str(code)[4:8]}-{str(code)[8:12]}'
            await ctx.send(f"Your Friend Code has been set to: {codes[str(ctx.author.id)]}.")
        await ctx.tick()
        
        return

    @fc.command()
    async def remove(self, ctx):
        """Remove your friend code"""
        check = MessagePredicate.yes_or_no()
        try:
            await ctx.send("Are you sure you want to remove your Friend Code? Reply with Yes or No.")
            await self.bot.wait_for("message", check=check, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return
        if not check.result:
            await ctx.send("Operation cancelled.")
            return
        try:
            async with self.config.guild(ctx.guild).codes() as codes:
                codes.pop(str(ctx.author.id))
            await ctx.send("Your Friend Code has been removed.")
        except KeyError:
            await ctx.send("You do not have a Friend Code set.")
        await ctx.tick()
        
        return
