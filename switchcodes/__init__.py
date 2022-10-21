from .switchcodes import switchcodes

async def setup(bot):
    cog = switchcodes
    bot.add_cog(switchcodes(bot))
