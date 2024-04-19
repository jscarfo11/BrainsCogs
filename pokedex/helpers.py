import discord
import textwrap
import rapidfuzz

from rapidfuzz import utils, fuzz
from redbot.core import commands
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions


async def construct_embed(index: dict, embed: discord.Embed):
    for element, value in index.items():
        if value and len(str(value)) <= 1024:
            embed.add_field(name=element, value="\n".join(textwrap.wrap(str(value), 25)))
        elif value and len(str(value)) > 1024:
            embed.add_field(name=element, value="Value too long to display.")
        else:
            embed.add_field(name=element, value="N/A")


async def get_sprite(pokemon, shiny: bool, gender: str, front: bool) -> str:
    female = pokemon.sprites.front_female
    if shiny:
        if front and (gender == 'M' or female is None):
            return pokemon.sprites.front_shiny
        elif front:
            return pokemon.sprites.front_shiny_female
        elif gender == 'M' or female is None:
            return pokemon.sprites.back_shiny
        else:
            return pokemon.sprites.back_shiny_female

    elif front:
        if gender == 'M' or female is None:
            return pokemon.sprites.front_default
        else:
            return pokemon.sprites.front_female
    else:
        if gender == 'M' or female is None:
            return pokemon.sprites.back_default
        else:
            return pokemon.sprites.back_female


async def fuzzy_search(ctx: commands.Context, pokemon: str):
    with open("pokedex/pokemon.txt", "r") as f:
        pokemon_list = f.readlines()
    x = rapidfuzz.process.extractOne(pokemon, pokemon_list, processor=utils.default_process, score_cutoff=80, scorer=fuzz.WRatio)
    message = await ctx.send(f"Did you mean {x[0].strip()}?")
    start_adding_reactions(message, ReactionPredicate.YES_OR_NO_EMOJIS)
    pred = ReactionPredicate.yes_or_no(message, ctx.author)
    await ctx.bot.wait_for("reaction_add", check=pred)

    if pred.result is True:
        return x[0].strip()
    else:
        return None
