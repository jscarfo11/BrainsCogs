from .switchcodes import SwitchCodes


async def setup(bot):
    await bot.add_cog(SwitchCodes(bot))
