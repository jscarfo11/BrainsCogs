from .speak import Speak


async def setup(bot):
    await bot.add_cog(Speak(bot))
