from .minecraftrcon import MinecraftRCON


async def setup(bot):
    await bot.add_cog(MinecraftRCON(bot))
