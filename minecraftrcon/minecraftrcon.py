import discord

from redbot.core import commands, Config
from redbot.core.utils.predicates import MessagePredicate
from mctools import RCONClient


class MinecraftRCON(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.valid_responses = ['[0m', '']
        self.config = Config.get_conf(self, identifier=655564502358165984158594)
        default_guild = {
            "host": "",
            "port": 0,
            "password": "",
            "admins": []
        }
        self.config.register_guild(**default_guild)

    @commands.group()
    async def rcon(self, ctx):
        """Run RCON commands on the server."""
        pass

    @rcon.command()
    async def run(self, ctx, *, command):
        """Run an RCON command on the server."""
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
        """Set the host for the RCON connection."""
        admins = await self.config.guild(ctx.guild).admins()
        if ctx.author.id not in admins:
            return await ctx.send("You do not have permission to run this command.")
        if not host:
            return await ctx.send("Please provide a host.")
        await self.config.guild(ctx.guild).host.set(host)
        await ctx.send("Host set successfully.")

    @setup.command()
    async def port(self, ctx, port):
        """Set the port for the RCON connection."""

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
        """Add an admin to the RCON connection."""
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

        # admins.append(user.id)
        # await self.config.guild(ctx.guild).admins.set(admins)
        # await ctx.send("Admin added successfully.")

    @setup.command()
    async def rcon_clear_config(self, ctx):
        """Clear the RCON config."""
        admins = await self.config.guild(ctx.guild).admins()
        if ctx.author.id not in admins and not self.bot.is_admin(ctx.author) and not self.bot.is_owner(ctx.author):
            await ctx.send("You do not have permission to run this command.")
            return
        await self.config.guild(ctx.guild).clear()
        await ctx.send("Config cleared successfully.")




async def setup(bot):
    await bot.add_cog(MinecraftRCON(bot))
