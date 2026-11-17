"""Event Formes régionales : quand il est actif, 30 % des spawns (spawn, devine, quiz)
viennent de json/alola.json, json/alola_shiny.json, json/galar.json et json/galar_shiny.json."""
import json
import os
import random

from utils import is_croco

FORME_REGIONALE_CHANCE = 1 #0.30

_json_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "json")


def load_regional_pool(file_name: str) -> list:
    try:
        with open(os.path.join(_json_dir, file_name), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[FORME_REGIONALE] json/{file_name} illisible : {e}")
        return []


def pick_forme_regionale_pokemon(bot, shiny: bool = False):
    """Retourne un Pokémon Alola/Galar (30 % de chances si l'event est actif), sinon None."""
    pool = getattr(bot, "forme_regionale_pool", None)
    if not pool or random.random() >= FORME_REGIONALE_CHANCE:
        return None
    # sans pool shiny, un tirage shiny retombe sur le pool normal
    shiny_pool = getattr(bot, "forme_regionale_shiny_pool", None)
    return random.choice((shiny and shiny_pool) or pool)


def setup_forme_regionale(bot):
    bot.forme_regionale_pool = []  # pool vide = event inactif
    bot.forme_regionale_shiny_pool = []

    @bot.command(name="forme_regionale_on")
    @is_croco()
    async def forme_regionale_on(ctx):
        """Active l'event Formes régionales (relit les json Alola et Galar, normaux et shiny)."""
        bot.forme_regionale_pool = (
            load_regional_pool("alola.json") + load_regional_pool("galar.json")
        )
        bot.forme_regionale_shiny_pool = (
            load_regional_pool("alola_shiny.json") + load_regional_pool("galar_shiny.json")
        )
        if not bot.forme_regionale_pool:
            await ctx.send("❌ Les json de formes régionales sont introuvables, vides ou invalides : event non activé.")
            return
        await ctx.send(
            f"🌺 Event Formes régionales activé : {int(FORME_REGIONALE_CHANCE * 100)} % de chances de spawn "
            f"parmi {len(bot.forme_regionale_pool)} Pokémon (Alola + Galar)."
        )

    @bot.command(name="forme_regionale_off")
    @is_croco()
    async def forme_regionale_off(ctx):
        """Désactive l'event Formes régionales."""
        bot.forme_regionale_pool = []
        await ctx.send("⛔ Event Formes régionales désactivé.")
