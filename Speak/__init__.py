from .mycog import Speak


def setup(bot):
    bot.add_cog(Speak(bot))