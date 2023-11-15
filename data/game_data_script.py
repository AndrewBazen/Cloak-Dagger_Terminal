import sqlite3


conn = sqlite3.connect('data/game_data.sqlite')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS items (
        name TEXT,
        rarity TEXT,
        cost TEXT,
        item_type TEXT,
        description TEXT
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS weapons (
        name TEXT,
        rarity TEXT,
        weight INTEGER,
        cost TEXT,
        dmg_dice TEXT,
        th_dmg_dice TEXT,
        dmg_dice_num INTEGER,
        th_dmg_dice_num INTEGER,
        dmg_type TEXT,
        weapon_type TEXT,
        weapon_property TEXT,
        item_type TEXT,
        description TEXT
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS armor (
        name TEXT,
        rarity TEXT,
        cost TEXT,
        armor_type TEXT,
        armor_property TEXT,
        item_type TEXT,
        description TEXT
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS enemies (
        name TEXT,
        enemy_type TEXT,
        health INTEGER,
        mana INTEGER,
        attack_dice TEXT,
        attack_dice_num INTEGER,
        sp_atk_dice TEXT,
        sp_atk_dice_num TEXT,
        atk_dmg_type TEXT,
        loot FOREIGN KEY,
        description TEXT
        )""")
