================
MinecraftRCON
================

This cog allows for server admins to remotely control their Minecraft server using the RCON protocol. It also allows users to whitelist themselves on the server.

There is also an option for moderators to configure a channel to emulate the server chat. This allows for users to send messages in the channel that will be sent to the server chat. Messages from the server chat will also be sent to the channel.

----------------
Installation
----------------
After following the instructions in :doc:`installation`, run the below commands to install and load the cog. ::

    [p]cog install brains-cogs minecraftrcon
    [p]load minecraftrcon

--------
Commands
--------

^^^^^^^^^^^^^^^^^^^^^
rcon setup
^^^^^^^^^^^^^^^^^^^^^

    This command is home to all of the server setting commands. It is also where the RCON connection is established.

    The different subcommands are as follows: ::

    - rcon setup host <host>: Sets the host of the Minecraft server.
    - rcon setup port <port>: Sets the port of the Minecraft server.
    - rcon setup password <password>: Sets the RCON password of the Minecraft server.

    These three commands are required to be run before any other commands can be used. ::

    - rcon setup chat <channel>: Sets the channel to emulate the server chat.
    - rcon setup admin <user> : Allows for server admins to give users the ability to interact with the server.
    - rcon setup showsettings: Shows the current settings of the server, without the password.
    - rcon setup clear_config: Clears the current settings of the server. This command will ask for confirmation before clearing the settings.

    ``rcon setup admin <user>`` is the only command restricted to users with the admin role. This command allows for server admins to give users the ability to interact with the server. All other commands are restricted to users with RCON admin role.

^^^^^^^^^^^^^^^^^^^^^
rcon run
^^^^^^^^^^^^^^^^^^^^^

    This command is used to run commands on the Minecraft server.

    Usage: ::

    [p]rcon run <command>

    This command is restricted to users with the RCON admin role.

    Example: ::

    [p]rcon run say Hello, world!

    This command will send the message "Hello, world!" to the server chat.

^^^^^^^^^^^^^^^^^^^^^
rcon whitelist
^^^^^^^^^^^^^^^^^^^^^

    This command is used to whitelist users on the Minecraft server. It links the users discord account to their Minecraft username. This allows for messages sent in the server chat to be linked to the users discord account.
    It four subcommands: ::

    - rcon whitelist add <minecraft_username>: Adds the user to the whitelist.
    - rcon whitelist remove <minecraft_username>: Removes the user from the whitelist.
    - rcon whitelist show: Shows the current whitelist.
    - rcon whitelist link <minecraft_username> <discord_user>: Links the discord user to the Minecraft username.


    Any user can add themselves to the whitelist. However, only users with the admin role can remove users from the whitelist or link discord users to Minecraft usernames. Even if a user gets banned from the server, they will still be linked to their discord account. This is to prevent users from impersonating other users.

    Example: ::

    [p]rcon whitelist add Notch
    This links the user "Notch" to the discord account that ran the command. ::

    [p]rcon whitelist link Notch @Notch#1234

    This links the user "Notch" to the discord user @Notch#1234. This exists so users who are already on the whitelist can have their discord account linked to their Minecraft username.


^^^^^^^^^^^^^^^^^^^^^
rcon ping
^^^^^^^^^^^^^^^^^^^^^

    This command is used to check the connection to the Minecraft server. It will return the latency of the connection.

    Usage: ::

    [p]rcon ping

    This command is unrestricted.

^^^^^^^^^^^^^^^^^^^^^
rcon players
^^^^^^^^^^^^^^^^^^^^^

    This command is used to check the current players on the Minecraft server.

    Usage: ::

    [p]rcon players

    This command is unrestricted.


