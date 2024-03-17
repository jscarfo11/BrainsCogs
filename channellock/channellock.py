import discord
import asyncio

from discord.ext.commands import Context
from discord.ext.commands._types import BotT

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
            "lock_image": "",
            "unlock_image": "",
        }
        self.config.register_guild(**default_guild)

    async def cog_check(self, ctx: Context[BotT]) -> bool:
        value = (await self.bot.is_owner(ctx.author)
                 or await self.bot.is_admin(ctx.author) or await self.bot.is_mod(ctx.author))
        return value

    async def lock_channel(self, ctx, roles):
        everyone = discord.utils.get(ctx.guild.roles, name="@everyone")
        for role in roles:
            role = ctx.guild.get_role(role)
            await ctx.channel.set_permissions(role, send_messages=False, read_messages=True)
        admin_roles = await self.config.guild(ctx.guild).admin_roles()
        for role in admin_roles:
            role = ctx.guild.get_role(role)
            await ctx.channel.set_permissions(role, send_messages=True, read_messages=True)
        await ctx.channel.set_permissions(everyone, send_messages=False, read_messages=True)
        async with self.config.guild(ctx.guild).locked_channels() as channels:
            channels.append(ctx.channel.id)

    async def channel_unlock(self, ctx, roles):
        channel = ctx.channel
        everyone = discord.utils.get(ctx.guild.roles, name="@everyone")
        for role in roles:
            role = ctx.guild.get_role(role)
            await ctx.channel.set_permissions(role, send_messages=True, read_messages=True)

        await ctx.channel.set_permissions(everyone, send_messages=False, read_messages=True)
        async with self.config.guild(channel.guild).locked_channels() as channels:
            channels.remove(channel.id)

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
        if not roles:
            param = commands.Parameter("roles", commands.Parameter.VAR_POSITIONAL)
            raise commands.MissingRequiredArgument(param)

        for role in roles:
            async with self.config.guild(ctx.guild).admin_roles() as r:
                if role.id in r:
                    return await ctx.send(f"{role.name} is already an admin role.")
            async with self.config.guild(ctx.guild).supporter_roles() as r:
                if role.id in r:
                    return await ctx.send(f"{role.name} is already a supporter role.")
            async with self.config.guild(ctx.guild).access_roles() as r:
                if role.id in r:
                    return await ctx.send(f"{role.name} is already an access role.")

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
        if not roles:
            param = commands.Parameter("roles", commands.Parameter.VAR_POSITIONAL)
            raise commands.MissingRequiredArgument(param)

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

    @role_add.error
    @role_remove.error
    async def role_error_handler(self, ctx, error):
        print(type(error))
        if isinstance(error, commands.RoleNotFound):
            await ctx.send("Role not found. If you are using the role name and it has a space, use double quotes.")
        else:
            await ctx.bot.on_command_error(ctx, error, unhandled_by_cog=True)

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

    @channellock.command(name="lockimage")
    async def lock_image(self, ctx, url: str = None):
        """Set the lock image. \nIf no URL is provided, the lock image will be removed."""
        if not url:
            await self.config.guild(ctx.guild).lock_image.set("")
            return await ctx.send("Lock image removed.")
        try:
            embed = discord.Embed(color=discord.Color.red())
            embed.set_image(url=url)
            await ctx.send(embed=embed)
        except discord.HTTPException:
            return await ctx.send("Invalid URL.")
        await self.config.guild(ctx.guild).lock_image.set(url)
        await ctx.send("Lock image set.")

    @channellock.command(name="unlockimage")
    async def unlock_image(self, ctx, url: str = None):
        """Set the unlock image. \nIf no URL is provided, the unlock image will be removed."""
        if not url:
            await self.config.guild(ctx.guild).unlock_image.set("")
            return await ctx.send("Unlock image removed.")
        try:
            embed = discord.Embed(color=discord.Color.green())
            embed.set_image(url=url)
            await ctx.send(embed=embed)
        except discord.HTTPException:
            return await ctx.send("Invalid URL.")
        await self.config.guild(ctx.guild).unlock_image.set(url)
        await ctx.send("Unlock image set.")

    @commands.command(name="lock", aliases=["lockchannel", "bd", "botdown"])
    async def lock(self, ctx):
        """Lock a channel."""
        channel = ctx.channel
        if channel.id in await self.config.guild(ctx.guild).locked_channels():
            return await ctx.send("This channel is already locked.")
        if channel.id in await self.config.guild(ctx.guild).supporter_channels():
            supporter = await self.config.guild(ctx.guild).supporter_roles()
            await self.lock_channel(ctx, supporter)
        elif channel.id in await self.config.guild(ctx.guild).regular_channels():
            regular = await self.config.guild(ctx.guild).access_roles()
            await self.lock_channel(ctx, regular)
        else:
            return await ctx.send("This channel is not configured to be locked.")
        await ctx.message.delete()
        image = await self.config.guild(ctx.guild).lock_image()
        if image:
            embed = discord.Embed(color=discord.Color.red())
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Channel locked.")

    @commands.command(name="unlock", aliases=["unlockchannel", "bu", "botup", "bbo", "botbackonline"])
    async def unlock(self, ctx):
        """"Unlock a channel."""
        channel = ctx.channel
        if channel.id not in await self.config.guild(ctx.guild).locked_channels():
            return await ctx.send("This channel is not locked.")
        if channel.id in await self.config.guild(ctx.guild).supporter_channels():
            supporter = await self.config.guild(ctx.guild).supporter_roles()
            if not supporter:
                return await ctx.send("This channel is locked to supporter roles, but no supporter roles are set.")
            await self.channel_unlock(ctx, supporter)
        elif channel.id in await self.config.guild(ctx.guild).regular_channels():
            regular = await self.config.guild(ctx.guild).access_roles()
            if not regular:
                return await ctx.send("This channel is locked to regular roles, but no regular roles are set.")
            await self.channel_unlock(ctx, regular)
        else:
            return await ctx.send("This channel is not configured to be locked.")
        await ctx.message.delete()
        image = await self.config.guild(ctx.guild).unlock_image()
        if image:
            embed = discord.Embed(color=discord.Color.green())
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Channel unlocked.")
