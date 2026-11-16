"""Event Alola : quand il est actif, 30 % des spawns (spawn, devine, quiz) viennent de json/alola.json."""
import json
import os
import random

from utils import is_croco

ALOLA_CHANCE = 0.30

_alola_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "json", "alola.json")


def load_alola_pool(file_name: str = "alola.json") -> list:
    try:
        with open(os.path.join(os.path.dirname(_alola_path), file_name), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ALOLA] json/{file_name} illisible : {e}")
        return []


def pick_alola_pokemon(bot, shiny: bool = False):
    """Retourne un Pokémon d'Alola (30 % de chances si l'event est actif), sinon None."""
    pool = getattr(bot, "alola_pool", None)
    if not pool or random.random() >= ALOLA_CHANCE:
        return None
    # sans alola_shiny.json, un tirage shiny retombe sur le pool normal
    return random.choice((shiny and getattr(bot, "alola_shiny_pool", None)) or pool)


def setup_alola(bot):
    bot.alola_pool = []  # pool vide = event inactif
    bot.alola_shiny_pool = []

    @bot.command(name="alola_on")
    @is_croco()
    async def alola_on(ctx):
        """Active l'event Alola (relit json/alola.json et json/alola_shiny.json)."""
        bot.alola_pool = load_alola_pool()
        bot.alola_shiny_pool = load_alola_pool("alola_shiny.json")
        if not bot.alola_pool:
            await ctx.send("❌ `json/alola.json` est introuvable, vide ou invalide : event non activé.")
            return
        await ctx.send(
            f"🌺 Event Alola activé : {int(ALOLA_CHANCE * 100)} % de chances de spawn "
            f"parmi {len(bot.alola_pool)} Pokémon d'Alola."
        )

    @bot.command(name="alola_off")
    @is_croco()
    async def alola_off(ctx):
        """Désactive l'event Alola."""
        bot.alola_pool = []
        await ctx.send("⛔ Event Alola désactivé.")
