================
AutoDelete
================

This cog allows users to set a channel to automatically delete messages after a certain amount of time. It allows for setting specific users and roles to be exempt from the deletion. The bot must have the ``Manage Messages`` permission to use this cog.

.. note::

       This cog was designed specifically for The-High-Table server. It may not work as expected in other servers. If you would like to use this cog in your server, please let me know and I will make the necessary changes.

----------------
Installation
----------------
After following the instructions in :doc:`installation`, run the below commands to install and load the cog. ::

    [p]cog install brains-cogs autodelete
    [p]load autodelete


----------------
Commands
----------------
All commands are run through the bot command ``[p]autodelete``. This command also has an alias of ``[p]ad``. It requires the user to have the ``Manage Messages`` permission.

^^^^^^^^^^^^^^^^^
autodelete role
^^^^^^^^^^^^^^^^^
    This command has three sub commands: ``add``, ``remove``, and ``list``.

    ``add`` - Adds a role to the list of roles that are exempt from auto-deletion.
    ``remove`` - Removes a role from the list of roles that are exempt from auto-deletion.
    ``list`` - Lists all roles that are exempt from auto-deletion.

    **Usage:**
    ``[p]autodelete role add <role>``
    ``[p]autodelete role remove <role>``
    ``[p]autodelete role list``

^^^^^^^^^^^^^^^^^
autodelete user
^^^^^^^^^^^^^^^^^
    This command has three sub commands: ``add``, ``remove``, and ``list``.

    ``add`` - Adds a user to the list of users that are exempt from auto-deletion.
    ``remove`` - Removes a user from the list of users that are exempt from auto-deletion.
    ``list`` - Lists all users that are exempt from auto-deletion.

    **Usage:**
    ``[p]autodelete user add <user>``
    ``[p]autodelete user remove <user>``
    ``[p]autodelete user list``


^^^^^^^^^^^^^^^^^
autodelete channel
^^^^^^^^^^^^^^^^^
    This command has three sub commands: ``add``, ``remove``, and ``list``.

    ``add`` - Adds a channel to the list of channels that have auto-deletion enabled.
    ``remove`` - Removes a channel from the list of channels that have auto-deletion enabled.
    ``list`` - Lists all channels that have auto-deletion enabled.


    **Usage:**
    ``[p]autodelete channel add <channel> <time>``
    ``[p]autodelete channel remove <channel>``
    ``[p]autodelete channel list``

^^^^^^^^^^^^^^^^^
autodelete time
^^^^^^^^^^^^^^^^^
    This command has two sub commands: ``set`` and ``show``.

    ``show`` - Shows the time for auto-deletion.

    ``set`` - Sets the time for auto-deletion.

    **Usage:**
    ``[p]autodelete time set  <time>``

^^^^^^^^^^^^^^^^^
autodelete toggle
^^^^^^^^^^^^^^^^^
    This command toggles auto-deletion on and off for the server.

    **Usage:**
    ``[p]autodelete toggle``

