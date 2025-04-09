import contextlib

import discord
from redbot.core import commands


class KickWarn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    @commands.admin_or_permissions(ban_members=True)
    async def kickwarn(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        """Kick a member with a warning message."""
        if reason is None:
            reason = "No reason provided."

        loaded_cogs = self.bot.cogs

        if "Mod" not in loaded_cogs:
            return await ctx.send("The Mod cog is not loaded. Please load it to use this command.")
        elif "Warnings" not in loaded_cogs:
            return await ctx.send(
                "The Warnings cog is not loaded. Please load it to use this command."
            )

        await ctx.invoke(self.bot.get_command("warn"), user=member, points=1, reason=reason)
        with contextlib.suppress(discord.HTTPException):
            em = discord.Embed(
                title=(f"**You have been kicked from {ctx.guild.name}.**"),
                color=await self.bot.get_embed_color(member),
            )
            em.add_field(
                name=("**Return**"),
                value=(
                    "Your membership to the Continental has been—by thine own hand—revoked\nYou may return at any time you wish:\nhttps://discord.gg/V9yYzugtmr"
                ),
                inline=False,
            )
            await member.send(embed=em)
        await ctx.invoke(self.bot.get_command("kick"), member=member, reason=reason)
        await ctx.send(
            (
                f"**User**: {member.mention} kicked! | **Reason**: `{reason}` | **Your membership to the Continental has been** *—by thine own hand—* **revoked.**"
            )
        )
