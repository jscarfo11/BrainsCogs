================
SwitchCodes
================

This cog allows for users to store and search for nintendo switch friendcodes within a server.

.. note::

        This cog was originally a commission done by `Leet <https://github.com/leetfin>`_ however has been customized since then.

----------------
Installation
----------------
After following the instructions in :doc:`installation`, run the below commands to install and load the cog. ::

    [p]cog install brains-cogs switchcodes
    [p]load switchcodes

--------
Commands
--------

^^^^^^^^^^^^^^^^^^^^^
friendcode (fc)
^^^^^^^^^^^^^^^^^^^^^

    Search for a users friend code. This command can also be run by using ``fc``.

    Usage ::

    [p]friendcode @user # displays the users friend code from their discord user
    [p]fc user-id # displays the code from their id


    Examples: ::

    [p]fc brains_ # Response: SW-1234-1234-1234


^^^^^^^^^^^^^^^^^^^^^^^^^^^^
friendcode add (fc add)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Add your own friend code to the system. Friend codes are always 12 digits long and all numbers.

    Usage: ::

    [p]fc add <your-friend-code>

    Examples: ::

    [p]fc add 123412341234 # Response: Your friend code has been set to: 1234-1234-1234.



^^^^^^^^^^^^^^^^^^^^^^^^^^^^
friendcode remove (fc remove)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Remove your friend code from the system. It will ask for a confirmation before removing.

    Usage: ::

    [p]fc remove

    Examples: ::

    User: [p]fc remove
    Response: Are you sure you want to remove your friend code? (yes/no)
    User: yes
    Response: Your friend code has been removed.
