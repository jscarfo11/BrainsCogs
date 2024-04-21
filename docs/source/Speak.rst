================
Speak
================

This cog allows you to talk as the bot within a server. All of the commands in this cog are restricted to server admins only.

.. note::

        At this moment, this cog does not work in dms, only in servers. This is a planned feature.

----------------
Installation
----------------
After following the instructions in :doc:`installation`, run the below commands to install and load the cog. ::

    [p]cog install brains-cogs speak
    [p]load speak

--------
Commands
--------
^^^^^^^
speak
^^^^^^^

    Speak as the bot in a server. The alias for this command is ``say``.

    Usage: ::

        [p]speak <channel[optional]> <message>

    Examples: ::

        [p]speak channel-link Hello, World!
        [p]speak hi!
        [p]say channel-id Welcome!


^^^^^^^
reply
^^^^^^^
    Reply to a message as the bot

    Usage: ::

    [p]reply <mention[optional]> <message-to-reply-to> <message-to-reply-with>

    Examples: ::

    [p]reply message-link text
    [p]reply 1 message-link text # This message will ping the user being replied to


^^^^^^^
editmsg
^^^^^^^
    Edit a message already sent by the bot. Only works on messages sent in the last 14 days and owned by the bot.

    Usage: ::

    [p]editmsg <message-to-reply-to> <new-message-content>

    Examples: ::

    [p]editmsg message-link Oops!

^^^^^^^
tunnel
^^^^^^^
    Allow for any messages sent in a selected channel to be sent to you as a dm by the bot. Also allows for you to dm the bot, and have those messages appear in the selected channel as if you has used the say command.

    Usage: ::

    [p]tunnel <channel-link>


    You can then close the tunnel by responding to the dm with the message: ::

        close_tunnel


