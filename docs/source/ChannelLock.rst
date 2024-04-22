================
ChannelLock
================

This cog allows you to lock a channel so that only certain roles can send messages in it. This is useful for bot commands channels, where you want to prevent users from sending messages in the channel when the bot is offline. The bot requires the `embed links`, the `mange roles`, and the `manage channels` permissions to work properly.

.. note::

       This cog was designed specifically for The-High-Table server. It may not work as expected in other servers. If you would like to use this cog in your server, please let me know and I will make the necessary changes.

----------------
Installation
----------------
After following the instructions in :doc:`installation`, run the below commands to install and load the cog. ::

    [p]cog install brains-cogs channellock
    [p]load channellock

--------
Commands
--------
^^^^^^^
channellock
^^^^^^^

    This command is the main command for the cog. It allows you to manage all of the settings for the channel lock. It has an alias of ``cl``.

    It has the following subcommands:

    **channel**
        This subcommand allows you to add a channel to the configuration, remove a channel from the configuration, or list all of the channels in the configuration.
        Its subcommands are:
        ``add`` - Adds a channel to the configuration.
        ``remove`` - Removes a channel from the configuration.
        ``list`` - Lists all of the channels in the configuration.

    **role**
        This subcommand allows you to add a role to the configuration, remove a role from the configuration, or list all of the roles in the configuration.
        Its subcommands are:
        ``add`` - Adds a role to the configuration.
        ``remove`` - Removes a role from the configuration.
        ``list`` - Lists all of the roles in the configuration.

    **lockimage**
        This subcommand allows you to set the image that will be displayed in the embed when the channel gets locked.
        It has one argument:
        ``url`` - The URL of the image that you want to set.
        If you do not provide a URL, the image will be removed.

    **unlockimage**
        This subcommand allows you to set the image that will be displayed in the embed when the channel gets unlocked.
        It has one argument:
        ``url`` - The URL of the image that you want to set.
        If you do not provide a URL, the image will be removed.


    **Usage:** ::

            [p]channellock channel add #channel
            [p]channellock channel remove #channel
            [p]channellock channel list
            [p]cl role add @role
            [p]cl role remove @role
            [p]cl role list
            [p]cl lockimage url
            [p]cl unlockimage url


^^^^^^^^^
lock
^^^^^^^^^

    This command allows you to lock the channel the command is sent in. When a channel is locked, only the roles that have been added to the configuration can send messages in the channel. If the channel has not been added to the configuration, the command return an error message.

    **Usage:** ::

            [p]lock


^^^^^^^^^^
unlock
^^^^^^^^^^

    This command allows you to unlock the channel the command is sent in. When a channel is unlocked, all roles specified by the config can send messages in the channel.

    **Usage:** ::

            [p]unlock

