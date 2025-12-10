from .pkhex import PkHex


async def setup(bot):
    await bot.add_cog(PkHex(bot))
