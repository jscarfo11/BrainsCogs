from .kickwarn import KickWarn


async def setup(bot):
    await bot.add_cog(KickWarn(bot))
