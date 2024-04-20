import discord
import textwrap
import rapidfuzz
import pokebase

from rapidfuzz import utils, fuzz
from redbot.core import commands
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
from requests.exceptions import HTTPError


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


async def get_pokemon(ctx: commands.Context, pokemon: str, fuzzy_list: list[str]):
    try:
        result = pokebase.pokemon(int(pokemon))
    except ValueError:
        try:
            result = pokebase.pokemon(pokemon.lower())
            assert result.id
        except (HTTPError, AttributeError):
            result = await fuzzy_search(ctx, pokemon, fuzzy_list)
            if result is False:
                await ctx.send("Pokemon not found. Please check your spelling and try again.")
                return None
            elif result is None:
                await ctx.send("Sorry, I couldn't find the right pokemon. Please try again.")
                return None
            result = pokebase.pokemon(result)
    except HTTPError:
        await ctx.send("There is not a pokemon with that ID.")
        return None

    try:
        assert result.id
    except AttributeError:
        await ctx.send("Something went wrong. Please report this to the developer.")
        raise ConnectionRefusedError("Pokemon not found. Site is probably down.")

    return result


async def fuzzy_search(ctx: commands.Context, pokemon: str, pokemon_list: list[str]):
    x = rapidfuzz.process.extractOne(pokemon, pokemon_list, processor=utils.default_process, score_cutoff=80,
                                     scorer=fuzz.WRatio)
    if x is None:
        return False
    message = await ctx.send(f"Did you mean {x[0].strip().capitalize()}?")
    start_adding_reactions(message, ReactionPredicate.YES_OR_NO_EMOJIS)
    pred = ReactionPredicate.yes_or_no(message, ctx.author)
    await ctx.bot.wait_for("reaction_add", check=pred)

    if pred.result is True:
        return x[0].strip().lower()
    else:
        return None


async def get_all_matches(pokemon: str, pokemon_list: list[str]):
    options = rapidfuzz.process.extract(pokemon, pokemon_list, processor=utils.default_process, score_cutoff=60)
    final = []
    for i in options:
        x = i[0]
        mon = pokebase.pokemon(x)
        final.append("".join([f"{mon.name.capitalize()} ({mon.id})"]))
    return final


async def fuzzy_move(ctx: commands.Context, move: str):
    move_list = [i.name for i in pokebase.move('w').results]
    x = rapidfuzz.process.extractOne(move, move_list, processor=utils.default_process, score_cutoff=80,
                                     scorer=fuzz.WRatio)
    if x is None:
        await ctx.send("Move not found. Please check your spelling and try again.")
        return None
    message = await ctx.send(f"Did you mean {x[0].strip().capitalize()}?")
    start_adding_reactions(message, ReactionPredicate.YES_OR_NO_EMOJIS)
    pred = ReactionPredicate.yes_or_no(message, ctx.author)
    await ctx.bot.wait_for("reaction_add", check=pred)
    if pred.result is True:
        return x[0]
    else:
        await ctx.send("Sorry, I couldn't find the right move. Please try again.")
        return None


async def fuzzy_ability(ctx: commands.Context, ability: str):
    ability_list = [i.name for i in pokebase.ability('w').results]
    x = rapidfuzz.process.extractOne(ability, ability_list, processor=utils.default_process, score_cutoff=80,
                                     scorer=fuzz.WRatio)
    if x is None:
        await ctx.send("Ability not found. Please check your spelling and try again.")
        return None
    message = await ctx.send(f"Did you mean {x[0].strip().capitalize()}?")
    start_adding_reactions(message, ReactionPredicate.YES_OR_NO_EMOJIS)
    pred = ReactionPredicate.yes_or_no(message, ctx.author)
    await ctx.bot.wait_for("reaction_add", check=pred)
    if pred.result is True:
        return x[0]
    else:
        await ctx.send("Sorry, I couldn't find the right ability. Please try again.")
        return None

