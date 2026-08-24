import discord
from discord.ext import commands
from utils import is_croco
from badge_db import get_user_badges
from new_db import copy_new_captures_table, clear_new_captures, restore_from_copie_new_captures

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
        file = discord.File("images/giovanni.jpg", filename="giovanni.jpg")

        # Image en premier
        await ctx.send(file=file)

        # Texte ensuite
        await ctx.send(
            "Dresseurs, écoutez-moi attentivement.\n\n"
            "Vos Pokémon ont disparu.\n\n"
            "Inutile de les chercher. C’est moi qui les ai pris.\n\n"
            "La Team Rocket s’est emparée de vos précieux compagnons, "
            "et ils sont désormais sous notre contrôle.\n\n"
            "Vous voulez les récupérer ? Alors venez les chercher.\n\n"
            "Mes hommes sont dans la région Rocket.\n\n"
            "Affrontez-les, et prouvez que vous êtes capables de récupérer ce qui vous appartient.\n\n"
            "Mais ne vous méprenez pas… chaque membre de la Team Rocket "
            "que vous vaincrez vous rapprochera de moi.\n\n"
            "Et lorsque vous serez enfin face à moi… nous verrons si vous êtes "
            "réellement capables de récupérer vos Pokémon.\n\n"
            "À bientôt, dresseurs.\n\n"
            "— Giovanni"
        )
        
    is_croco()
    @bot.command(name="restorerocket")
    async def restorecaptures(ctx):
        """
        !restorerocket
        Restaure uniquement les Pokémon du membre qui a exécuté la commande.
        """
        user_id = str(ctx.author.id)
        required_badges = {100, 101, 102, 103, 104, 105, 106, 107}
        user_badges = set(get_user_badges(user_id))

        if not required_badges.issubset(user_badges):
            missing_badges = [
                badge_name
                for badge_name, badge_id in {
                    "Jessie": 100,
                    "James": 101,
                    "Butch" : 102,
                    "Cassidy": 103,
                    "Proton" : 104,
                    "Ariana": 105,
                    "Archer" : 106,
                    "Giovanni": 107,
                }.items()
                if badge_id not in user_badges
            ]
            await ctx.send(
                f"❌ Tu ne peux pas utiliser `!restorerocket` tant que tu n’as pas les machines "
                f"{', '.join(missing_badges)}."
            )
            return

        result = restore_from_copie_new_captures(user_id)

        await ctx.send(
            f"✅ Restauration terminée pour {ctx.author.mention} !\n"
            f"➕ {result['inserted']} Pokémon ajouté(s)\n"
            f"📈 {result['updated']} Pokémon déjà existants (IV augmentés de +4)"
        )