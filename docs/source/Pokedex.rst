================
Pokedex
================

This cog is a simple pokedex that allows users to search for pokemon information. It uses the pokeapi to get the information.
.. note::

    This cog would not be possible without the pokeapi. You can find more information about the pokeapi at https://pokeapi.co/
----------------
Installation
----------------
After following the instructions in :doc:`installation`, run the below commands to install and load the cog. ::

    [p]cog install brains-cogs pokedex
    [p]load pokedex


----------------
Commands
----------------
All commands are run through the bot command ``[p]pokedex``. This command also has aliases of ``[p]dex`` and ``[p]pd``. It can be used by any user.

^^^^^^^^^^^^^^^^^
pokedex search
^^^^^^^^^^^^^^^^^
    This command is used to search for a pokemon. It will return information about the pokemon. If the pokemon is not found, it will return an error message. Its aliases are ``pokemon``, ``poke`` and ``p``.

    Usage: ::

        [p]pokedex search <pokemon>
        [p]pokedex pokemon <pokemon>
        [p]pokedex poke <pokemon>
        [p]pokedex p <pokemon>

    Examples: ::

        [p]pokedex search bulbasaur
        [p]pokedex p Bulbasaur
        [p]pokedex pokemon 1

^^^^^^^^^^^^^^^^^
pokedex find
^^^^^^^^^^^^^^^^^
    This command is used to find the name or ID number of a pokemon that is required by pokeapi. It will return the name of the pokemon. It will attempt to find the closest match to the input.

    Usage: ::

        [p]pokedex find <pokemon>

    Examples: ::

            [p]pokedex find bulba
            [p]pokedex find Raichu Alola

^^^^^^^^^^^^^^^^^
pokedex ability
^^^^^^^^^^^^^^^^^
    This command is used to search for an ability. It will return information about the ability. If the ability is not found, it will return an error message. It has an alias of ``a``.

    Usage: ::

        [p]pokedex ability <ability>
        [p]pokedex a <ability>

    Examples: ::

        [p]pokedex ability overgrow
        [p]pokedex a blaze

^^^^^^^^^^^^^^^^^
pokedex move
^^^^^^^^^^^^^^^^^
    This command is used to search for a move. It will return information about the move. If the move is not found, it will return an error message. Its aliases are ``learn`` and ``learns``.

    Usage: ::

        [p]pokedex move <move>
        [p]pokedex learn <move>

    Examples: ::

        [p]pokedex move tackle
        [p]pokedex learn ember


^^^^^^^^^^^^^^^^^
pokedex moveset
^^^^^^^^^^^^^^^^^
    This command is used to search for a moveset of a pokemon. It will return information about the moveset. If the pokemon is not found, it will return an error message. Its aliases are ``movepool``, ``move_set``, and ``moves``.

    Usage: ::

        [p]pokedex moveset <pokemon>
        [p]pokedex ms <pokemon>
        [p]pokedex moves <pokemon>

    Examples: ::

        [p]pokedex moveset bulbasaur
        [p]pokedex ms 1
        [p]pokedex moves charmander

^^^^^^^^^^^^^^^^^
pokedex item
^^^^^^^^^^^^^^^^^
    This command is used to search for an item. It will return information about the item. If the item is not found, it will return an error message. It has an alias of ``i``.

    Usage: ::

        [p]pokedex item <item>
        [p]pokedex i <item>

    Examples: ::

        [p]pokedex item master ball
        [p]pokedex i poke ball

^^^^^^^^^^^^^^^^^
pokedex sprite
^^^^^^^^^^^^^^^^^
    This command is used to search for a sprite of a pokemon. It will return a link to the sprite. If the pokemon is not found, it will return an error message. Its aliases are ``image`` and ``img``.

    It has optional arguments of ``shiny``, ``gender``, and ``front``. If the shiny argument is set to anything other than ``0`` or ``False``, it will return the shiny sprite. If the gender argument is set to `F` or `female`, it will return the female sprite. If the front argument is set to ``B`` or ``back``, it will return the back sprite. Otherwise, it will return the front sprite.

    Usage: ::

        [p]pokedex sprite <pokemon>
        [p]pokedex image <pokemon> <shiny>
        [p]pokedex img <pokemon> <shiny> <gender> <front>

    Examples: ::
        [p]pokedex sprite bulbasaur
        [p]pokedex img charmander shiny F B
        [p]pokedex image 1 True