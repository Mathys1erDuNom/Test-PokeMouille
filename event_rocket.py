import discord
from discord.ext import commands
from utils import is_croco
from new_db import copy_new_captures_table, clear_new_captures

def setup_rocket(bot):

    is_croco()
    @bot.command(name="eventrocket")
    @commands.has_permissions(administrator=True)
    async def resetcaptures(ctx):
        """
        !eventrocket
        Copie new_captures dans copie_new_captures, puis vide new_captures.
        """
        # 1. Copie de la table
        copy_new_captures_table()

        # 2. Vidage de la table originale
        clear_new_captures()

        # 3. Envoi de l'image + texte dans le channel
        file = discord.File("images/actu/vieuxchateau.jpeg", filename="reset.png")
        await ctx.send(
            content="✅ La table **new_captures** a été sauvegardée dans `copie_new_captures` puis vidée !",
            file=file
        )