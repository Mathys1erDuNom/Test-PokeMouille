import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Connexion globale à la base
conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cur = conn.cursor()

script_dir = os.path.dirname(os.path.abspath(__file__))


# Création de la table chenil
cur.execute("""
CREATE TABLE IF NOT EXISTS chenil (
    user_id      TEXT PRIMARY KEY,
    pokemon_name TEXT NOT NULL,
    is_egg       BOOLEAN DEFAULT FALSE,
    egg_xp       INTEGER DEFAULT 0,
    egg_xp_evo   INTEGER DEFAULT 400
);
""")
conn.commit()

# Migration douce : ajout de colonnes si nécessaire
for col, definition in [
    ("is_egg",     "BOOLEAN DEFAULT FALSE"),
    ("egg_xp",     "INTEGER DEFAULT 0"),
    ("egg_xp_evo", "INTEGER DEFAULT 400"),
]:
    try:
        cur.execute(f"ALTER TABLE chenil ADD COLUMN IF NOT EXISTS {col} {definition};")
        conn.commit()
    except Exception:
        conn.rollback()


def get_chenil_pokemon(user_id: str) -> dict | None:
    cur.execute(
        "SELECT pokemon_name, is_egg, egg_xp, egg_xp_evo FROM chenil WHERE user_id = %s",
        (user_id,)
    )
    row = cur.fetchone()
    if not row:
        return None
    return {
        "name":       row[0],
        "is_egg":     row[1],
        "egg_xp":     row[2],
        "egg_xp_evo": row[3],
    }


def set_chenil_pokemon(user_id: str, pokemon_name: str, is_egg: bool = False, egg_xp_evo: int = 400):
    cur.execute("""
        INSERT INTO chenil (user_id, pokemon_name, is_egg, egg_xp, egg_xp_evo)
        VALUES (%s, %s, %s, 0, %s)
        ON CONFLICT (user_id) DO UPDATE SET
            pokemon_name = EXCLUDED.pokemon_name,
            is_egg       = EXCLUDED.is_egg,
            egg_xp       = 0,
            egg_xp_evo   = EXCLUDED.egg_xp_evo
    """, (user_id, pokemon_name, is_egg, egg_xp_evo))
    conn.commit()


def remove_chenil_pokemon(user_id: str):
    cur.execute("DELETE FROM chenil WHERE user_id = %s", (user_id,))
    conn.commit()


def add_egg_xp(user_id: str, amount: int) -> bool:
    cur.execute(
        "UPDATE chenil SET egg_xp = egg_xp + %s WHERE user_id = %s",
        (amount, user_id)
    )
    conn.commit()
    cur.execute(
        "SELECT egg_xp, egg_xp_evo FROM chenil WHERE user_id = %s",
        (user_id,)
    )
    row = cur.fetchone()
    return bool(row and row[0] >= row[1])


def get_egg_info(user_id: str) -> tuple[int, int] | None:
    """Retourne (egg_xp, egg_xp_evo) ou None si pas de ligne."""
    cur.execute("SELECT egg_xp, egg_xp_evo FROM chenil WHERE user_id = %s", (user_id,))
    row = cur.fetchone()
    if not row:
        return None
    return (row[0], row[1])
