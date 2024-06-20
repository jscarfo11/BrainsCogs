from .legacy import Legacy


async def setup(bot):
    await bot.add_cog(Legacy(bot))
