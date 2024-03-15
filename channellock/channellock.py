import discord
import asyncio

from redbot.core import commands, Config, checks
from redbot.core.utils.predicates import MessagePredicate


class ChannelLock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=246609685532964861890)
        default_guild = {
            "regular_channels": [],
            "supporter_channels": [],
            "admin_roles": [],
            "supporter_roles": [],
            "locked_channels": [],
            "access_roles": [],
        }
        self.config.register_guild(**default_guild)

    async def supporter_lock(self, channel: discord.TextChannel):
        pass

    async def regular_lock(self, channel: discord.TextChannel):
        pass

    @checks.admin_or_permissions(manage_channels=True)
    @commands.group(name="channellock", aliases=["cl"])
    async def channellock(self, ctx):
        """Lock channels to specific roles."""
        pass

    @channellock.group(name="channel")
    async def channel(self, ctx):
        """Lock channels to specific roles."""
        pass

    @channel.command(name="add")
    async def channel_add(self, ctx, channel: discord.TextChannel):
        """Add a channel to the locked channels list."""

        # Check if the channel is already in the list
        async with self.config.guild(ctx.guild).supporter_channels() as channels:
            if channel.id in channels:
                return await ctx.send("This channel is already a supporter channel.")
        async with self.config.guild(ctx.guild).regular_channels() as channels:
            if channel.id in channels:
                return await ctx.send("This channel is already a regular channel.")

        c_type = MessagePredicate.lower_contained_in(["regular", "supporter"])  # Regular or Supporter
        await ctx.send("What type of channel would you like to add this to? `regular` or `supporter`.")
        try:
            await ctx.bot.wait_for("message", check=c_type, timeout=10)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long to respond.")
        c_type = c_type.result

        if c_type == 0:  # Regular
            async with self.config.guild(ctx.guild).regular_channels() as channels:
                if channel.id in channels:
                    return await ctx.send("This channel is already a regular channel.")
                channels.append(channel.id)
            await ctx.send(f"{channel.mention} has been added to the regular channel list.")
        else:  # Supporter
            async with self.config.guild(ctx.guild).supporter_channels() as channels:
                if channel.id in channels:
                    return await ctx.send("This channel is already a supporter channel.")
                channels.append(channel.id)
            await ctx.send(f"{channel.mention} has been added to the supporter channel list.")

    @channel.command(name="remove")
    async def channel_remove(self, ctx, channel: discord.TextChannel):
        """Remove a channel from the locked channels list."""
        async with self.config.guild(ctx.guild).regular_channels() as channels:
            if channel.id in channels:
                channels.remove(channel.id)
                return await ctx.send(f"{channel.mention} has been removed from the regular channel list.")
        async with self.config.guild(ctx.guild).supporter_channels() as channels:
            if channel.id in channels:
                channels.remove(channel.id)
                return await ctx.send(f"{channel.mention} has been removed from the supporter channel list.")
        await ctx.send("This channel is not locked.")

    @channel.command(name="list")
    async def channel_list(self, ctx):
        """List the locked channels."""
        regular = await self.config.guild(ctx.guild).regular_channels()
        supporter = await self.config.guild(ctx.guild).supporter_channels()
        regular = [ctx.guild.get_channel(c).mention for c in regular]
        supporter = [ctx.guild.get_channel(c).mention for c in supporter]
        embed = discord.Embed(title=f"Configured Channels for {ctx.guild.name}")
        embed.add_field(name="Regular Channels", value="\n".join(regular))
        embed.add_field(name="Supporter Channels", value="\n".join(supporter))
        await ctx.send(embed=embed)

    @channellock.group(name="role")
    async def role(self, ctx):
        """Lock channels to specific roles."""
        pass

    @role.command(name="add")
    async def role_add(self, ctx, *roles: discord.Role):
        """Add a role to the locked roles list."""

        for role in roles:
            async with self.config.guild(ctx.guild).admin_roles() as r:
                if role.id in r:
                    return await ctx.send(f"{role.mention} is already an admin role.")
            async with self.config.guild(ctx.guild).supporter_roles() as r:
                if role.id in r:
                    return await ctx.send(f"{role.mention} is already a supporter role.")
            async with self.config.guild(ctx.guild).access_roles() as r:
                if role.id in r:
                    return await ctx.send(f"{role.mention} is already an access role.")

        for role in roles:
            r_type = MessagePredicate.lower_contained_in(["admin", "supporter", "access"])
            await ctx.send(
                f"What type of role would you like to add {role.name} to? `admin`, `supporter`, or `access`.")
            try:
                await ctx.bot.wait_for("message", check=r_type, timeout=10)
            except asyncio.TimeoutError:
                return await ctx.send("You took too long to respond.")
            r_type = r_type.result
            if r_type == 0:  # Admin
                async with self.config.guild(ctx.guild).admin_roles() as r:
                    r.append(role.id)
                await ctx.send(f"{role.name} has been added to the admin role list.")
            elif r_type == 1:  # Supporter
                async with self.config.guild(ctx.guild).supporter_roles() as r:
                    r.append(role.id)
                await ctx.send(f"{role.name} has been added to the supporter role list.")
            else:  # Access
                async with self.config.guild(ctx.guild).access_roles() as r:
                    r.append(role.id)
                await ctx.send(f"{role.name} has been added to the access role list.")

        if len(roles) > 1:
            await ctx.send("Roles added.")

    @role.command(name="remove")
    async def role_remove(self, ctx, *roles: discord.Role):
        """Remove a role from the locked roles list."""
        for role in roles:
            async with self.config.guild(ctx.guild).admin_roles() as r:
                if role.id in r:
                    r.remove(role.id)
                    await ctx.send(f"{role.name} has been removed from the admin role list.")
                    continue
            async with self.config.guild(ctx.guild).supporter_roles() as r:
                if role.id in r:
                    r.remove(role.id)
                    await ctx.send(f"{role.name} has been removed from the supporter role list.")
                    continue
            async with self.config.guild(ctx.guild).access_roles() as r:
                if role.id in r:
                    r.remove(role.id)
                    await ctx.send(f"{role.name} has been removed from the access role list.")
                    continue
            await ctx.send(
                f"{role.name} is not a role you have set. Run `{self.bot.get_prefix()}channellock role list` to see "
                f"all of your roles.")

    @role_remove.error
    async def role_remove_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to provide a role to remove.")



    @role.command(name="list")
    async def role_list(self, ctx):
        """List the locked roles."""
        admin = await self.config.guild(ctx.guild).admin_roles()
        supporter = await self.config.guild(ctx.guild).supporter_roles()
        access = await self.config.guild(ctx.guild).access_roles()
        admin = [ctx.guild.get_role(r).mention for r in admin]
        supporter = [ctx.guild.get_role(r).mention for r in supporter]
        access = [ctx.guild.get_role(r).mention for r in access]
        embed = discord.Embed(title=f"Configured Roles for {ctx.guild.name}")
        embed.add_field(name="Admin Roles", value="\n".join(admin))
        embed.add_field(name="Supporter Roles", value="\n".join(supporter))
        embed.add_field(name="Access Roles", value="\n".join(access))
        await ctx.send(embed=embed)
