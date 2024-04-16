import discord

from redbot.core import commands, Config
from redbot.core.utils.predicates import MessagePredicate
from mctools import RCONClient, PINGClient, QUERYClient


class MinecraftRCON(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.valid_responses = ['[0m', '']
        self.config = Config.get_conf(self, identifier=655564502358165984158594)
        default_guild = {
            "host": "",
            "port": 0,
            "password": "",
            "admins": [],
            "rcon_channel": [],
            "whitelist": {}
        }
        self.config.register_guild(**default_guild)

    @commands.group()
    async def rcon(self, ctx):
        """Run RCON commands on the server."""
        pass

    @rcon.command()
    async def run(self, ctx, *, command):
        """Run a minecraft command on the server using the RCON protocol."""
        admins = await self.config.guild(ctx.guild).admins()

        if ctx.author.id not in admins:
            await ctx.send("You do not have permission to run this command.")
            return

        if not command:
            await ctx.send("Please provide a command to run.")
            return
        await ctx.typing()
        host = await self.config.guild(ctx.guild).host()
        port = await self.config.guild(ctx.guild).port()
        password = await self.config.guild(ctx.guild).password()
        if not host or not port or not password:
            await ctx.send("Please set up the RCON connection first.")
            return
        rcon = RCONClient(host, port=port)
        try:
            if rcon.login(password):
                resp = rcon.command(command).strip("[0m")
                if resp in self.valid_responses:
                    await ctx.send("Command executed successfully.")
                else:
                    await ctx.send(f"Response: {resp}")
            else:
                await ctx.send("Failed to login to RCON.")
        except ConnectionRefusedError:
            await ctx.send("Failed to connect to RCON. Check that the server is online and the RCON port is "
                           "correct.")
        except Exception as e:
            await ctx.send(f"An error occurred. Please try again later.")
            raise e

    @rcon.group()
    async def setup(self, ctx):
        """Set up the RCON connection."""
        pass

    @setup.command()
    async def host(self, ctx, host: str):
        """Set the host for the minecraft server."""
        admins = await self.config.guild(ctx.guild).admins()
        if ctx.author.id not in admins:
            return await ctx.send("You do not have permission to run this command.")
        if not host:
            return await ctx.send("Please provide a host.")
        await self.config.guild(ctx.guild).host.set(host)
        await ctx.send("Host set successfully.")

    @setup.command()
    async def port(self, ctx, port):
        """Set the port for the minecraft server."""

        admins = await self.config.guild(ctx.guild).admins()
        if ctx.author.id not in admins:
            return await ctx.send("You do not have permission to run this command.")
        await self.config.guild(ctx.guild).port.set(port)
        await ctx.send("Port set successfully.")

    @setup.command()
    async def password(self, ctx, *, password: str):
        """Set the password for the RCON connection."""
        admins = await self.config.guild(ctx.guild).admins()
        if ctx.author.id not in admins:
            return await ctx.send("You do not have permission to run this command.")
        if not password:
            return await ctx.send("Please provide a password.")
        await self.config.guild(ctx.guild).password.set(password)
        try:
            await ctx.message.delete(delay=5)
            await ctx.send("Password set successfully. Your message will be deleted in 5 seconds.")
        except discord.HTTPException:
            await ctx.send("Password set successfully. Please delete your message manually.")

    @setup.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Set the channel for RCON messages."""
        admins = await self.config.guild(ctx.guild).admins()
        if ctx.author.id not in admins:
            return await ctx.send("You do not have permission to run this command.")
        message = MessagePredicate.lower_contained_in(["add", "a", "remove", "r", "cancel", "c"])
        embed = discord.Embed(title="Add/Remove Admin",
                              description=f"Would you like to add or remove {channel.mention} as a RCON message channel?",
                              color=await ctx.embed_color())
        embed.set_footer(
            text="Type 'add' to add the channel as an admin, 'remove' to remove it, or 'cancel' to cancel.")
        await ctx.send(embed=embed)
        try:
            await self.bot.wait_for("message", check=message, timeout=10)
        except TimeoutError:
            await ctx.send("You took too long to respond.")
            return
        if message.result in [0, 1]:
            async with self.config.guild(ctx.guild).rcon_channel() as channels:
                if channel.id in channels:
                    return await ctx.send("This channel is already included")
                channels.append(channel.id)
            return await ctx.send(f"{channel.mention} is now a RCON message channel.")
        elif message.result in [2, 3]:
            async with self.config.guild(ctx.guild).rcon_channel() as channels:
                if channel.id not in channels:
                    return await ctx.send("This channel is not a RCON message channel.")
                channels.remove(channel.id)
            return await ctx.send("This channel is no longer a RCON message channel.")
        else:
            return await ctx.send("Cancelled.")

    @setup.command(aliases=["showsettings"])
    async def settings(self, ctx):
        """Show the current RCON settings."""
        admins = await self.config.guild(ctx.guild).admins()
        if ctx.author.id not in admins:
            return await ctx.send("You do not have permission to run this command.")

        host = await self.config.guild(ctx.guild).host()
        port = await self.config.guild(ctx.guild).port()
        embed = discord.Embed(title=f"RCON Settings for {ctx.guild.name}", color=await ctx.embed_color())
        embed.add_field(name="Host", value=host)
        embed.add_field(name="Port", value=port)
        embed.add_field(name="Password", value="**********")
        embed.set_footer(text="To change these settings, use the rconsetup command.")
        embed.add_field(name="Admins", value=", ".join(
            [str(ctx.guild.get_member(a)) for a in await self.config.guild(ctx.guild).admins()]))
        await ctx.send(embed=embed)

    @setup.command()
    async def admin(self, ctx, user: discord.Member):
        """RCON Admin management."""
        admins = await self.config.guild(ctx.guild).admins()
        if ctx.author.id not in admins and not await self.bot.is_admin(ctx.author) and not await self.bot.is_owner(
                ctx.author):
            await ctx.send("You do not have permission to run this command.")
            return
        message = MessagePredicate.lower_contained_in(["add", "a", "remove", "r", "cancel", "c"])
        embed = discord.Embed(title="Add/Remove Admin",
                              description=f"Would you like to add or remove {user.mention} as an admin?",
                              color=await ctx.embed_color())
        embed.set_footer(text="Type 'add' to add the user as an admin, 'remove' to remove them, or 'cancel' to cancel.")
        await ctx.send(embed=embed)
        try:
            await self.bot.wait_for("message", check=message, timeout=10)
        except TimeoutError:
            await ctx.send("You took too long to respond.")
            return
        if message.result in [0, 1]:
            async with self.config.guild(ctx.guild).admins() as admins:
                if user.id in admins:
                    return await ctx.send("This user is already an admin.")
                admins.append(user.id)
            return await ctx.send(f"{user.mention} is now an admin.")
        elif message.result in [2, 3]:
            async with self.config.guild(ctx.guild).admins() as admins:
                if user.id not in admins:
                    return await ctx.send("This user is not an admin.")
                admins.remove(user.id)
            return await ctx.send("This user is no longer an admin.")
        else:
            return await ctx.send("Cancelled.")

    @setup.command()
    async def clear_config(self, ctx):
        """Clear the RCON config."""
        admins = await self.config.guild(ctx.guild).admins()
        if ctx.author.id not in admins and not await self.bot.is_admin(ctx.author) and not await self.bot.is_owner(
                ctx.author):
            return await ctx.send("You do not have permission to run this command.")
        check = MessagePredicate.yes_or_no()
        try:
            await ctx.send("Are you sure you want to clear the config? This cannot be undone. Yes/No")
            await self.bot.wait_for("message", check=check, timeout=10)
        except TimeoutError:
            return await ctx.send("You took too long to respond.")
        if not check.result:
            return await ctx.send("Cancelled.")
        await self.config.guild(ctx.guild).clear()
        await ctx.send("Config cleared successfully.")

    @rcon.command()
    async def ping(self, ctx):
        """Ping the server to check if it's online."""
        await ctx.typing()
        host = await self.config.guild(ctx.guild).host()
        if not host:
            return await ctx.send("Please set up the RCON connection first.")
        client = PINGClient(host, port=25565, proto_num=0)
        try:
            await ctx.send(f"Server is online. Response time: {client.ping()}ms")
        except ConnectionRefusedError:
            await ctx.send("Server is offline. This command may be having issues. Use `[p]rcon players` to check.")

    @rcon.command()
    async def players(self, ctx):
        """Get the players on the server."""
        host = await self.config.guild(ctx.guild).host()
        query = QUERYClient(host)
        if not host:
            return await ctx.send("Please set up the RCON connection first.")
        try:
            stats = query.get_full_stats()
            embed = discord.Embed(title=f"Players on {host}", color=await ctx.embed_color())
            embed.add_field(name="Players", value=", ".join(stats['players']).strip('\x1b[0m'))
            embed.add_field(name="Player Count", value=stats['numplayers'] + "/" + stats['maxplayers'])
            await ctx.send(embed=embed)
        except ConnectionRefusedError:
            await ctx.send("Server is offline.")

    @rcon.group()
    async def whitelist(self, ctx):
        """Whitelist management commands."""
        pass

    @whitelist.command()
    async def add(self, ctx, user: str):
        """Add a user to the whitelist."""
        host = await self.config.guild(ctx.guild).host()
        port = await self.config.guild(ctx.guild).port()
        password = await self.config.guild(ctx.guild).password()
        rcon = RCONClient(host, port=port)
        async with self.config.guild(ctx.guild).whitelist() as whitelist:
            if ctx.author.id in whitelist:
                return await ctx.send("You are already on the whitelist.")
            try:
                if rcon.login(password):
                    resp = rcon.command(f"whitelist add {user}").strip("[0m")
                    if resp in self.valid_responses or resp == f"Added {user} to the whitelist":
                        await ctx.send(f"{user} has been added to the whitelist.")
                        whitelist[str(ctx.author.id)] = user
                    else:
                        await ctx.send(f"Response: {resp}")
                else:
                    await ctx.send("Failed to login to RCON.")
            except ConnectionRefusedError:
                await ctx.send("Failed to connect to RCON. Check that the server is online and the RCON port is "
                               "correct.")

    @whitelist.command()
    async def remove(self, ctx, user: str):
        """Remove a user from the whitelist."""
        host = await self.config.guild(ctx.guild).host()
        port = await self.config.guild(ctx.guild).port()
        password = await self.config.guild(ctx.guild).password()
        rcon = RCONClient(host, port=port)
        async with self.config.guild(ctx.guild).admins() as admins:
            if ctx.author.id not in admins:
                return await ctx.send("You do not have permission to run this command.")
        async with self.config.guild(ctx.guild).whitelist() as whitelist:
            try:
                if rcon.login(password):
                    resp = rcon.command(f"whitelist remove {user}").strip("[0m")
                    if resp in self.valid_responses or resp == f"Removed {user} from the whitelist":
                        await ctx.send(f"{user} has been removed from the whitelist.")
                        whitelist.pop(str(ctx.author.id))
                    else:
                        await ctx.send(f"Response: {resp}")
                else:
                    await ctx.send("Failed to login to RCON.")
            except ConnectionRefusedError:
                await ctx.send("Failed to connect to RCON. Check that the server is online and the RCON port is "
                               "correct.")

    @whitelist.command(aliases=["showlist", "list"])
    async def show(self, ctx):
        """Display the whitelist."""
        async with self.config.guild(ctx.guild).whitelist() as whitelist:
            if not whitelist:
                return await ctx.send("The whitelist is empty.")
            embed = discord.Embed(title="Whitelist", color=await ctx.embed_color())
            for k, v in whitelist.items():
                embed.add_field(name=k, value=v)
            await ctx.send(embed=embed)

    @whitelist.command()
    async def override(self, ctx, user: discord.Member, user_override: str):
        """Override a user's whitelist entry."""
        async with self.config.guild(ctx.guild).admins() as admins:
            if ctx.author.id not in admins:
                return await ctx.send("You do not have permission to run this command.")
        async with self.config.guild(ctx.guild).whitelist() as whitelist:
            whitelist[str(user.id)] = user_override
            await ctx.send(f"{user.name}'s whitelist entry has been overridden with {user_override}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id not in await self.config.guild(message.guild).rcon_channel():
            return

        if message.author.bot:
            return
        if message.content.startswith("!rcon"):
            return await message.channel.send("Please don't use the RCON commands in this channel.")
        if message.content.startswith("!"):
            return
        msg = message.content
        if "{password}" in msg:
            async with self.config.guild(message.guild).admin() as admins:
                x = [message.guild.get_member(a) for a in admins]
            return await message.channel.send("Please don't include the password in your message. " +
                                              ", ".join([i.mention for i in x]))

        host = await self.config.guild(message.guild).host()
        port = await self.config.guild(message.guild).port()
        password = await self.config.guild(message.guild).password()
        rcon = RCONClient(host, port=port)
        try:
            if rcon.login(password):
                password = "**********"
                msg = "say " + "[DISCORD] " + f"[{message.author.name}] " + msg
                resp = rcon.command(msg).strip("[0m")
                if resp in self.valid_responses:
                    await message.add_reaction("✅")
                else:
                    await message.channel.send(f"Response: {resp}")
            else:
                await message.channel.send("Failed to login to RCON.")
        except ConnectionRefusedError:
            await message.channel.send(
                "Failed to connect to RCON. Check that the server is online and the RCON port is "
                "correct.")
        except Exception as e:
            await message.channel.send(f"An error occurred. Please try again later.")
            raise e


async def setup(bot):
    await bot.add_cog(MinecraftRCON(bot))
