from .channellock import ChannelLock


async def setup(bot):
    await bot.add_cog(ChannelLock(bot))
