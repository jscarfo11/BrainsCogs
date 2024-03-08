import discord
import asyncio

from discord.ext.commands import Context
from discord.ext.commands._types import BotT

from redbot.core import checks, commands, Config


class AutoDelete(commands.Cog):
    def __init__(self, bot):  # Basically just setting up the config
        self.bot = bot
        self.config = Config.get_conf(self, identifier=17981871242730416904)
        default_guild = {
            "on": False,
            "channels": [],
            "users": [],
            "roles": [],
            "time": 5,
        }
        self.config.register_guild(**default_guild)

        # async def cog_check(self, ctx: Context[BotT]) -> bool:

    #     return await ctx.bot.is_admin(ctx.author)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:  # If it's a dm
            return
        if not await self.config.guild(message.guild).on():
            return
        if message.author.bot:
            return
        if message.channel.id not in await self.config.guild(message.guild).channels():
            return
        if message.author.id in await self.config.guild(message.guild).users():
            return
        config_roles = await self.config.guild(message.guild).roles()  # get user roles
        user_roles = (r.id for r in message.author.roles)

        if any(role in config_roles for role in user_roles):  # get
            return
        # if any(role in await self.config.guild(message.guild).roles() for role in message.author.roles):
        #     return
        await asyncio.sleep(await self.config.guild(message.guild).time())
        await message.delete()

    @checks.admin_or_permissions(manage_messages=True)
    @commands.group(name="autodelete", aliases=["ad"])
    async def autodelete(self, ctx):
        """Auto delete messages in certain channels."""
        pass

    @autodelete.command(name="toggle")
    async def toggle(self, ctx):
        """Toggle auto delete on or off."""
        on = await self.config.guild(ctx.guild).on()
        await self.config.guild(ctx.guild).on.set(not on)
        if on:
            await ctx.send("Auto delete is now off.")
        else:
            await ctx.send("Auto delete is now on.")

    @autodelete.group(name="channel", aliases=["channels"])
    async def channel(self, ctx):
        """Manage AutoDelete channels."""
        pass

    @channel.command(name="add")
    async def add_channel(self, ctx, channel: discord.TextChannel):
        """Add a channel to auto delete."""
        async with self.config.guild(ctx.guild).channels() as channels:
            if channel.id in channels:
                await ctx.send("That channel is already in the list.")
                return
            channels.append(channel.id)
        await ctx.send(f"{channel.mention} has been added to the list.")

    @channel.command(name="remove")
    async def remove_channel(self, ctx, channel: discord.TextChannel):
        """Remove a channel from auto delete."""
        async with self.config.guild(ctx.guild).channels() as channels:
            if channel.id not in channels:
                await ctx.send("That channel is not in the list.")
                return
            channels.remove(channel.id)
        await ctx.send(f"{channel.mention} has been removed from the list.")

    @channel.command(name="list")
    async def list_channels(self, ctx):
        """List all channels in auto delete."""
        channels = await self.config.guild(ctx.guild).channels()
        if not channels:
            await ctx.send("No channels are in the list.")
            return
        channels = [ctx.guild.get_channel(c).mention for c in channels]
        description = "\n".join(channels)
        embed = discord.Embed(title="Auto Delete Channels", description=description, color=await ctx.embed_color())
        await ctx.send(embed=embed)

    @autodelete.group(name="user", aliases=["users"])
    async def user(self, ctx):
        """Manage AutoDelete users."""
        pass

    @user.command(name="add")
    async def add_user(self, ctx, user: discord.Member):
        """Add a user to auto delete."""
        async with self.config.guild(ctx.guild).users() as users:
            if user.id in users:
                await ctx.send("That user is already in the list.")
                return
            users.append(user.id)
        await ctx.send(f"{user.mention} has been added to the list.")

    @user.command(name="remove")
    async def remove_user(self, ctx, user: discord.Member):
        """Remove a user from auto delete."""
        async with self.config.guild(ctx.guild).users() as users:
            if user.id not in users:
                await ctx.send("That user is not in the list.")
                return
            users.remove(user.id)
        await ctx.send(f"{user.mention} has been removed from the list.")

    @user.command(name="list")
    async def list_users(self, ctx):
        """List all users in auto delete."""
        users = await self.config.guild(ctx.guild).users()
        if not users:
            await ctx.send("No users are in the list.")
            return
        users = [ctx.guild.get_member(u).mention for u in users]
        description = "\n".join(users)
        embed = discord.Embed(title="Auto Delete Users", description=description, color=await ctx.embed_color())
        await ctx.send(embed=embed)

    @autodelete.group(name="role", aliases=["roles"])
    async def role(self, ctx):
        """Manage AutoDelete roles."""
        pass

    @role.command(name="add")
    async def add_role(self, ctx, role: discord.Role):
        """Add a role to auto delete."""
        async with self.config.guild(ctx.guild).roles() as roles:
            if role.id in roles:
                await ctx.send("That role is already in the list.")
                return
            roles.append(role.id)
        await ctx.send(f"{role.name} has been added to the list.")

    @role.command(name="remove")
    async def remove_role(self, ctx, role: discord.Role):
        """Remove a role from auto delete."""
        async with self.config.guild(ctx.guild).roles() as roles:
            if role.id not in roles:
                await ctx.send("That role is not in the list.")
                return
            roles.remove(role.id)
        await ctx.send(f"{role.name} has been removed from the list.")

    @role.command(name="list")
    async def list_roles(self, ctx):
        """List all roles in auto delete."""
        roles = await self.config.guild(ctx.guild).roles()
        if not roles:
            await ctx.send("No roles are in the list.")
            return
        roles = [ctx.guild.get_role(r).mention for r in roles]
        description = "\n".join(roles)
        embed = discord.Embed(title="Auto Delete Roles", description=description, color=await ctx.embed_color())
        await ctx.send(embed=embed)

    @autodelete.group(name="time")
    async def autodelete_time(self, ctx):
        """Manage the amount of time before the messages get deleted"""
        pass

    @autodelete_time.command(name='set')
    async def time_set(self, ctx, num: int):
        """Set the amount of time for the autodelete"""
        await self.config.guild(ctx.guild).time.set(num)
        await ctx.send(f"The message delete time is now {num} seconds")

    @autodelete_time.command(name='show')
    async def time_show(self, ctx):
        """Gets the current amount of time for the autodelete"""
        num = await self.config.guild(ctx.guild).time()
        await ctx.send(f'The current amount of time before auto-deleting a message is {num} seconds.')