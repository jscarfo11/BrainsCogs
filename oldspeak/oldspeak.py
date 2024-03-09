# Say by retke, aka El Laggron
from lib2to3.pgen2.token import COMMA
from os import name
import typing

import discord
import asyncio
import logging
import re

from typing import Optional, Union

from redbot.core import checks, commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.tunnel import Tunnel

_ = Translator("Say", __file__)
BaseCog = getattr(commands, "Cog", object)

# Red 3.0 backwards compatibility, thanks Sinbad
listener = getattr(commands.Cog, "listener", None)
if listener is None:

    def listener(name=None):
        return lambda x: x


ROLE_MENTION_REGEX = re.compile(r"<@&(?P<id>[0-9]{17,19})>")


@cog_i18n(_)
class OldSpeak(BaseCog):
    """
    Speak as if you were the bot
    """

    def __init__(self, bot):
        self.bot = bot
        self.interaction = []

    __author__ = ["retke (El Laggron)"]
    __version__ = "1.6.1"

    async def say(
        self,
        ctx: commands.Context,
        channel: Optional[discord.TextChannel],
        text: str,
        files: list,
        mentions: discord.AllowedMentions = None,
        delete: int = None,
    ):
        if not channel:
            channel = ctx.channel
        if not text and not files:
            await ctx.send_help()
            return

        # preparing context info in case of an error
        if files != []:
            error_message = (
                "Has files: yes\n"
                f"Number of files: {len(files)}\n"
                f"Files URL: " + ", ".join([x.url for x in ctx.message.attachments])
            )
        else:
            error_message = "Has files: no"

        # sending the message
        try:
            await channel.send(text, files=files, allowed_mentions=mentions, delete_after=delete)
        except discord.errors.HTTPException as e:
            author = ctx.author
            if not ctx.guild.me.permissions_in(channel).send_messages:
                try:
                    await ctx.send(
                        _("I am not allowed to send messages in ") + channel.mention,
                        delete_after=2,
                    )
                except discord.errors.Forbidden:
                    await author.send(
                        _("I am not allowed to send messages in ") + channel.mention,
                        delete_after=15,
                    )
                    # If this fails then fuck the command author
            elif not ctx.guild.me.permissions_in(channel).attach_files:
                try:
                    await ctx.send(
                        _("I am not allowed to upload files in ") + channel.mention, delete_after=2
                    )
                except discord.errors.Forbidden:
                    await author.send(
                        _("I am not allowed to upload files in ") + channel.mention,
                        delete_after=15,
                    )
            else:
                await ctx.send(
                   _("Unknown permissions error when sending a message.\n{error_message}") + channel.mention,
                        delete_after=15,
                )

    @commands.command(name="say")
    @checks.admin_or_permissions(administrator=True)
    async def _say(
        self, ctx: commands.Context, channel: Optional[discord.TextChannel], *, text: str = ""
    ):
        """
        Make the bot say what you want in the desired channel.

        If no channel is specified, the message will be send in the current channel.
        You can attach some files to upload them to Discord.

        Example usage :
        - `!say #general hello there`
        - `!say owo I have a file` (a file is attached to the command message)
        """

        files = await Tunnel.files_from_attatch(ctx.message)
        await self.say(ctx, channel, text, files)

    @commands.command(name="sayad")
    @checks.admin_or_permissions(administrator=True)
    async def _sayautodelete(
        self,
        ctx: commands.Context,
        channel: Optional[discord.TextChannel],
        delete_delay: int,
        *,
        text: str = "",
    ):
        """
        Same as say command, except it deletes the said message after a set number of seconds.
        """

        files = await Tunnel.files_from_attatch(ctx.message)
        await self.say(ctx, channel, text, files, delete=delete_delay)

    @commands.command(name="sayd", aliases=["sd"])
    @checks.admin_or_permissions(administrator=True)
    async def _saydelete(
        self, ctx: commands.Context, channel: Optional[discord.TextChannel], *, text: str = ""
    ):
        """
        Same as say command, except it deletes your message.

        If the message wasn't removed, then I don't have enough permissions.
        """

        # download the files BEFORE deleting the message
        author = ctx.author
        files = await Tunnel.files_from_attatch(ctx.message)

        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            try:
                await ctx.send(_("Not enough permissions to delete messages."), delete_after=2)
            except discord.errors.Forbidden:
                await author.send(_("Not enough permissions to delete messages."), delete_after=15)

        await self.say(ctx, channel, text, files)

    @commands.command(name="saym", aliases=["sm"])
    @checks.admin_or_permissions(administrator=True)
    async def _saymention(
        self, ctx: commands.Context, channel: Optional[discord.TextChannel], *, text: str = ""
    ):
        """
        Same as say command, except role and mass mentions are enabled.
        """
        message = ctx.message
        channel = channel or ctx.channel
        guild = channel.guild
        files = await Tunnel.files_from_attach(message)

        role_mentions = list(
            filter(
                None,
                (ctx.guild.get_role(int(x)) for x in ROLE_MENTION_REGEX.findall(message.content)),
            )
        )
        mention_everyone = "@everyone" in message.content or "@here" in message.content
        if not role_mentions and not mention_everyone:
            # no mentions, nothing to check
            return await self.say(ctx, channel, text, files)
        non_mentionable_roles = [x for x in role_mentions if x.mentionable is False]

        if not channel.permissions_for(guild.me).mention_everyone:
            if non_mentionable_roles:
                await ctx.send(
                    _(
                        "I can't mention the following roles: {roles}\nTurn on "
                        "mentions or grant me the correct permissions.\n"
                    ).format(roles=", ".join([x.name for x in non_mentionable_roles]))
                )
                return
            if mention_everyone:
                await ctx.send(_("I don't have the permission to mention everyone."))
                return
        if not channel.permissions_for(ctx.author).mention_everyone:
            if non_mentionable_roles:
                await ctx.send(
                    _(
                        "You're not allowed to mention the following roles: {roles}\nTurn on "
                        "mentions for that role or have the correct permissions.\n"
                    ).format(roles=", ".join([x.name for x in non_mentionable_roles]))
                )
                return
            if mention_everyone:
                await ctx.send(_("You don't have the permission yourself to do mass mentions."))
                return
        await self.say(
            ctx, channel, text, files, mentions=discord.AllowedMentions(everyone=True, roles=True)
        )

    @commands.command(name="interact")
    @checks.admin_or_permissions(administrator=True)
    async def _interact(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """Start receiving and sending messages as the bot through DM"""

        u = ctx.author
        if channel is None:
            if isinstance(ctx.channel, discord.DMChannel):
                await ctx.send(
                    _(
                        "You need to give a channel to enable this in DM. You can "
                        "give the channel ID too."
                    )
                )
                return
            else:
                channel = ctx.channel

        if u in self.interaction:
            await ctx.send(_("A session is already running."))
            return

        message = await u.send(
            _(
                "I will start sending you messages from {0}.\n"
                "Just send me any message and I will send it in that channel.\n"
                "React with ❌ on this message to end the session.\n"
                "If no message was send or received in the last 5 minutes, "
                "the request will time out and stop."
            ).format(channel.mention)
        )
        await message.add_reaction("❌")
        self.interaction.append(u)

        while True:

            if u not in self.interaction:
                return

            try:
                message = await self.bot.wait_for("message", timeout=300)
            except asyncio.TimeoutError:
                await u.send(_("Request timed out. Session closed"))
                self.interaction.remove(u)
                return

            if message.author == u and isinstance(message.channel, discord.DMChannel):
                files = await Tunnel.files_from_attatch(message)
                if message.content.startswith(tuple(await self.bot.get_valid_prefixes())):
                    return
                await channel.send(message.content, files=files)
            elif (
                message.channel != channel
                or message.author == channel.guild.me
                or message.author == u
            ):
                pass

            else:
                embed = discord.Embed()
                embed.set_author(
                    name="{} | {}".format(str(message.author), message.author.id),
                    icon_url=message.author.avatar
                )
                embed.set_footer(text=message.created_at.strftime("%d %b %Y %H:%M"))
                embed.description = message.content
                embed.colour = message.author.color

                if message.attachments != []:
                    embed.set_image(url=message.attachments[0].url)

                await u.send(embed=embed)
    @commands.command(name="reply")
    @checks.admin_or_permissions(administrator=True)
    async def _reply(self, ctx: commands.Context, to_mention: typing.Optional[bool], message: discord.Message, *, content: str):
        """Reply to a message using the Discord reply feature."""
        if not to_mention:
            mention_author = False
        else:
            mention_author = to_mention

        try:
            await message.reply(content, mention_author=mention_author)
        except discord.Forbidden:
            return await ctx.send("I cannot reply to the message!")
        return await ctx.tick()
    @commands.command(aliases=['editmsg'])
    @checks.admin()
    async def editmessage(
        self, ctx, ecid: int, editid: int, ccid: int, *, content: Union[int, str]
    ):
        """Edits a message with the content of another message or the specified content.

        Arguments:
            - ecid: The ID of the channel of the message you are editing (Required)

            - editid: The ID of the message you are editing (Required)

            - ccid: The ID of the channel of the message you are copying from.  If you are giving the raw content yourself, pass 0 as the channel ID. (Optional)

            - content: The ID of the message that contains the contents of what you want the other message to become, or the new content of the message.  (Required, integer (for message id) or text (for new content)

        Examples:
        `[p]editmessage <edit_channel_id> <edit_message_id> <copy_channel_id> <copy_message_id>`
        `[p]editmessage <edit_channel_id> <edit_message_id> 0 New content here`

        Real Examples:
        `[p]editmessage 133251234164375552 578969593708806144 133251234164375552 578968157520134161`
        `[p]editmessage 133251234164375552 578969593708806144 0 ah bruh`
        """
        if isinstance(content, int) and ccid == 0:
            return await ctx.send(
                "You provided an ID of a message to copy from, but didn't provide a channel ID to get the message from."
            )

        # Make sure channels and IDs are all good
        editchannel = self.bot.get_channel(ecid)
        if not editchannel or not type(editchannel) == discord.TextChannel:
            return await ctx.send("Invalid channel for the message you are editing.")
        if not editchannel.permissions_for(ctx.author).manage_messages and not (
            await self.bot.is_owner(ctx.author)
        ):
            return await ctx.send("You do not have permission to edit messages in that channel.")
        try:
            editmessage = await editchannel.fetch_message(editid)
        except discord.NotFound:
            return await ctx.send(
                "Invalid editing message ID, or you passed the wrong channel ID for the message."
            )
        except discord.Forbidden:
            return await ctx.send(
                "I'm not allowed to view the channel which contains the message I am editing."
            )
        if ccid != 0 and type(content) == int:
            copychannel = self.bot.get_channel(ccid)
            if not copychannel or not type(editchannel) == discord.TextChannel:
                return await ctx.send("Invalid ID for channel of the message to copy from.")
            try:
                copymessage = await copychannel.fetch_message(content)
            except discord.NotFound:
                return await ctx.send(
                    "Invalid copying message ID, or you passed the wrong channel ID for the message."
                )
            except discord.Forbidden:
                return await ctx.send(
                    "I'm not allowed to view the channel of the message from which I am copying."
                )

            # All checks passed
            content = copymessage.content
            try:
                embed = copymessage.embeds[0]
            except IndexError:
                embed = None
            try:
                await editmessage.edit(content=content, embed=embed)
            except discord.errors.Forbidden:
                return await ctx.send("I can only edit my own messages.")
            await ctx.send(f"Message successfully edited.  Jump URL: {editmessage.jump_url}")
        else:
            try:
                await editmessage.edit(content=content, embed=None)
                await ctx.send(f"Message successfully edited.  Jump URL: {editmessage.jump_url}")
            except discord.errors.Forbidden:
                await ctx.send("I can only edit my own messages.")
    @commands.command(hidden=True)
    @checks.is_owner()
    async def sayinfo(self, ctx):
        """
        Get informations about the cog.
        """
        await ctx.send(
            _(
                "Laggron's Dumb Cogs V3 - say\n\n"
                "Version: {0.__version__}\n"
                "Author: {0.__author__}\n"
                "Github repository: https://github.com/retke/Laggrons-Dumb-Cogs/tree/v3\n"
                "Discord server: https://discord.gg/GET4DVk\n"
                "Documentation: http://laggrons-dumb-cogs.readthedocs.io/\n"
                "Help translating the cog: https://crowdin.com/project/laggrons-dumb-cogs/\n\n"
                "Support my work on Patreon: https://www.patreon.com/retke"
            ).format(self)
        )

    @listener()
    async def on_reaction_add(self, reaction, user):
        if user in self.interaction:
            channel = reaction.message.channel
            if isinstance(channel, discord.DMChannel):
                await self.stop_interaction(user)

    async def stop_interaction(self, user):
        self.interaction.remove(user)
        await user.send(_("Session closed"))

    def __unload(self):
        self.cog_unload()