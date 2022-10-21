import discord
from redbot.core import Config, commands


class switchcodes(commands.Cog):
    """Store and retrieve Nintendo Switch friend codes."""
    
    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=296058336787300353)
        default_guild = {
            "codes": {},
        }
        self.config.register_guild(**default_guild)
        self.bot = bot
        
        return
    
    @commands.group(invoke_without_command=True)
    async def fc(self, ctx, *, user: discord.Member or int or None):
        """Search someone else's switch code"""
        if isinstance(user, int):
            user = self.bot.get_user(user)
        elif user is None:
            user = ctx.author
        code = await self.config.guild(ctx.guild).codes.get_raw(str(user.id), default=None)
        if code is None:
            await ctx.send("That user has not set their Switch Code.")
        else:
            embed = discord.Embed(title=f"{user.display_name}'s Switch Code", description=code)
            await ctx.send(embed=embed)
        await ctx.tick()
        
        return
    
    @fc.command()
    async def add(self, ctx, code: str):
        """Set your switch code"""
        if len(code) > 30:
            await ctx.send("That code is too long. Please try again.")
            await ctx.tick()
            return
        async with self.config.guild(ctx.guild).codes() as codes:
            codes[str(ctx.author.id)] = str(code)
        await ctx.send(f"Your Switch Code has been set to {code}.")
        await ctx.tick()
        
        return

    @fc.command()
    async def remove(self, ctx):
        """Remove your switch code"""
        async with self.config.guild(ctx.guild).codes() as codes:
            codes.pop(str(ctx.author.id))
        await ctx.send("Your Switch Code has been removed.")
        await ctx.tick()
        
        return
        