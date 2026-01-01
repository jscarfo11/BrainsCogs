import asyncio
import sys

# import clr
import discord
from redbot.core import Config, commands

# dir = "/home/jackd/PythonProjects/BrainsCogs/pkhex-sid"
# sys.path.append(dir)
# clr.AddReference("PKHeX.Core")


class PkHex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=396492370998460420)

        default_globals = {"pkhex_dir": "", "ready": False}
        self.config.register_global(**default_globals)
        self.pkhex = None

    @commands.Cog.listener()
    async def on_ready(self):
        if await self.config.ready() is True:
            try:
                from pythonnet import load

                load("coreclr")
                src_dir = await self.config.pkhex_dir()
                sys.path.append(src_dir)
            except Exception as e:
                await self.config.ready.set(False)
                destinations = await self.bot.get_owner_notification_destinations()
                for destination in destinations:
                    is_dm = isinstance(destination, discord.User)

                    if is_dm:
                        await destination.send("Your dotnet runtime is not properly setup!")
                raise e

    @commands.is_owner()
    @commands.command()
    async def set_pkhex_location(self, ctx: commands.Context, folder_path: str):
        try:
            await self.config.pkhex_dir.set(folder_path)
            await self.config.ready.set(True)
            from pythonnet import load

            load("coreclr")
            sys.path.append(folder_path)
        except Exception as e:
            await self.config.ready.set(False)
            await ctx.send("Your dotnet runtime is not properly setup! Check logs for more info")
            raise e

    @commands.command()
    async def sid(self, ctx: commands.Context):
        """Get the SID/TID of the first file attached to the command message."""

        if len(ctx.message.attachments) == 0:
            return await ctx.send("You must attach at least one PKHeX file.")
        import clr

        clr.AddReference("PKHeX.Core")
        from PKHeX import Core
        from PKHeX.Core import Species
        from System import Array, Byte, Memory

        file = ctx.message.attachments[0]
        data = await file.read()
        net_bytes = Array[Byte](data)
        mem = Memory[Byte](net_bytes)

        try:

            p = Core.EntityFormat.GetFromBytes(mem)
            msg = await ctx.send(
                f"Info for {Species(p.Species)}\nTID: {p.DisplayTID}\nSID: {p.DisplaySID}\n React with ❌ in the next minute to delete this message."
            )
        except Exception as e:
            await ctx.send(f"Failed to parse {file.filename}")
            raise e

        await msg.add_reaction("❌")
        try:
            await self.bot.wait_for(
                "reaction_add",
                check=lambda r, u: r.message.id == msg.id
                and str(r.emoji) == "❌"
                and u.id == ctx.author.id,
                timeout=60.0,
            )
        except asyncio.TimeoutError:
            await msg.clear_reactions()
            return
        await ctx.message.add_reaction("✅")
        await msg.delete()
