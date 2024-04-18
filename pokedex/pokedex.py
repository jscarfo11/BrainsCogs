import discord
import requests
import pokebase as pb
import textwrap

from redbot.core import commands


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
        for element, value in index.items():
            if value and len(str(value)) <= 1024:
                embed.add_field(name=element, value="\n".join(textwrap.wrap(str(value), 25)))
            elif value and len(str(value)) > 1024:
                embed.add_field(name=element, value="Value too long to display.")
            else:
                embed.add_field(name=element, value="N/A")

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
        for element, value in index.items():
            if value and len(str(value)) <= 1024:
                embed.add_field(name=element, value="\n".join(textwrap.wrap(str(value), 25)))
            elif value and len(str(value)) > 1024:
                embed.add_field(name=element, value="Value too long to display.")
            else:
                embed.add_field(name=element, value="N/A")

        await ctx.send(embed=embed)







async def setup(bot):
    await bot.add_cog(Pokedex(bot))
