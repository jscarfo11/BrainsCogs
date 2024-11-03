from .rolecommands import RoleCommands


async def setup(bot):
    await bot.add_cog(RoleCommands(bot))
