# This script was written by Conroy

import googletrans
from discord.ext import commands


# inherit from commands.Cog
class Translations(commands.Cog):

    def __init__(self, bot):
        # reference the bot object from Main.py
        self.bot = bot

    # *args is used to store a variable number of arguments
    @commands.command(help=("Translates a message. Type the language or "
                            "language code after the command followed by a message."))
    async def translate(self, ctx, language, *args):

        channel = ctx.message.channel

        # make sure that the language name is in lowercase
        # (all of the keys in the googletrans library are lowercase)
        lang = language.lower()

        # check that the language specified is actually in the dictionary
        # in the googletrans library (see googletrans documentation)
        if lang not in googletrans.LANGUAGES and lang not in googletrans.LANGCODES:

            # tell the user that the language was not found/recognized
            await channel.send(f"I do not recognize a laguage called {lang}.")

        else:

            # get the user's original text by concatenating the "arguments"
            # after the "langauge" variable
            original_text = " ".join(args)

            # create an instance of the translator object
            translator = googletrans.Translator()

            # get the translated text (dest is the destination language)
            translated_text = translator.translate(original_text, dest=lang).text

            # send the translated text!
            await channel.send(translated_text)


# this function connects this cog (via the Translations class) to the bot object
def setup(bot):
    bot.add_cog(Translations(bot))
