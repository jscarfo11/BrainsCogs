import discord
import requests
import pokebase as pb
import textwrap

from redbot.core import commands
from .helpers import construct_embed


class Pokedex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def pokedex(self, ctx):
        """Get information about Pokemon."""
        pass

    @pokedex.command()
    async def pokemon(self, ctx, pokemon):
        """Get some basic information about a Pokemon by name or ID."""
        try:
            pokemon = int(pokemon)
        except ValueError:
            pass

        try:
            pokemon = pb.pokemon(pokemon)
            assert pokemon.id

        except requests.exceptions.HTTPError:  # Fuzzy search
            return await ctx.send("Pokemon not found. Please check your spelling and try again.")
        except AttributeError:  # Fuzzy search
            return await ctx.send("Pokemon not found. Please check your spelling and try again.")

        embed = discord.Embed(title=f"#{pokemon.id}: {pokemon.name.capitalize()}", color=await ctx.embed_color())
        embed.set_image(url=pokemon.sprites.front_default)
        embed.add_field(name="Height", value=f"{pokemon.height}m")
        embed.add_field(name="Weight", value=f"{pokemon.weight}kg")
        embed.add_field(name="Base Experience", value=pokemon.base_experience)
        embed.add_field(name="Types", value=", ".join([t.type.name.capitalize() for t in pokemon.types]))
        abilities = []
        for ability in pokemon.abilities:
            if ability.is_hidden:
                abilities.append(f"{ability.ability.name.capitalize()} (H)")
            else:
                abilities.append(ability.ability.name.capitalize())
        embed.add_field(name="Abilities", value=", ".join(abilities))
        embed.add_field(name="Base Stats", value=" / ".join([f"{s.base_stat}" for s in pokemon.stats]))
        await ctx.send(embed=embed)

    @pokedex.command()
    async def name(self, ctx, num: int):
        """Get the name of a Pokemon by ID."""
        try:
            pokemon = pb.pokemon(num)
            assert pokemon.id
        except requests.exceptions.HTTPError:  # Fuzzy search
            return await ctx.send("Pokemon not found. Please check your spelling and try again.")
        except AttributeError:  # Fuzzy search
            return await ctx.send("Pokemon not found. Please check your spelling and try again.")
        await ctx.send(f"#{pokemon.id}: {pokemon.name.capitalize()}")

    @pokedex.command()
    async def id(self, ctx, pokemon: str):
        """Get the ID of a Pokemon by name."""
        try:
            pokemon = pb.pokemon(pokemon)
            assert pokemon.id
        except requests.exceptions.HTTPError:
            return await ctx.send("Pokemon not found. Please check your spelling and try again.")
        except AttributeError:
            return await ctx.send("Pokemon not found. Please check your spelling and try again.")
        await ctx.send(f"#{pokemon.id}: {pokemon.name.capitalize()}")

    @pokedex.command()
    async def ability(self, ctx, ability: str):
        """Get information about an ability by name."""
        try:
            ability = pb.ability(ability)
            assert ability.id
        except requests.exceptions.HTTPError:
            return await ctx.send("Ability not found. Please check your spelling and try again.")
        except AttributeError:
            return await ctx.send("Ability not found. Please check your spelling and try again. A")
        embed = discord.Embed(title=f"{ability.name.capitalize()}", color=await ctx.embed_color())
        learns = []
        for i in ability.pokemon:
            learns.append(i.pokemon.name.capitalize())
        index = {
            'Effect': ability.effect_entries[1].short_effect,
            "Flavor Text": ability.flavor_text_entries[1].flavor_text,
            "Learned By": ", \n".join(learns)
        }
        await construct_embed(ctx, index, embed)
        await ctx.send(embed=embed)

    @pokedex.command()
    async def move(self, ctx, move):
        """Get information about a move by name."""
        try:
            move = pb.move(move)
            assert move.id
        except requests.exceptions.HTTPError:
            return await ctx.send("Move not found. Please check your spelling and try again.")
        except AttributeError:
            return await ctx.send("Move not found. Please check your spelling and try again.")
        embed = discord.Embed(title=f"{move.name.capitalize()}", color=await ctx.embed_color())
        learn = []
        for i in move.learned_by_pokemon:
            learn.append(i.name.capitalize())

        index = {
            'Type': move.type.name.capitalize(),
            'Power': move.power,
            'PP': move.pp,
            'Accuracy': move.accuracy,
            'Effect': move.effect_entries[0].short_effect,
            'Learned By': ", \n".join(learn)

        }
        await construct_embed(ctx, index, embed)

        await ctx.send(embed=embed)

    @pokedex.command(aliases=["moves", "movepool", "move_set"])
    async def moveset(self, ctx, pokemon):
        """Get the moveset of a Pokemon by name or ID."""
        try:
            pokemon = pb.pokemon(pokemon)
            assert pokemon.id
        except requests.exceptions.HTTPError:
            return await ctx.send("Pokemon not found. Please check your spelling and try again.")
        except AttributeError:
            return await ctx.send("Pokemon not found. Please check your spelling and try again.")
        moves = []
        for i in pokemon.moves:
            moves.append([i.move.name.capitalize(), i.version_group_details[0].level_learned_at, i])
        levelup = []
        tutor = []
        machine = []
        for move in moves:
            if move[2].version_group_details[0].move_learn_method.name == "level-up":
                levelup.append([move[0], move[1]])
            elif move[2].version_group_details[0].move_learn_method.name == "machine":
                machine.append(f"{move[0]}")
            elif move[2].version_group_details[0].move_learn_method.name == "tutor":
                tutor.append(f"{move[0]}")

        levelup = sorted(levelup, key=lambda x: x[1])
        levelup = [f"{i[0]} at level {i[1]}" for i in levelup]

        embed = discord.Embed(title=f"{pokemon.name.capitalize()}", color=await ctx.embed_color())
        embed.add_field(name="Level-up", value="\n".join(levelup))
        embed.add_field(name="Machine", value="\n".join(machine))
        embed.add_field(name="Tutor", value="\n".join(tutor))

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Pokedex(bot))
