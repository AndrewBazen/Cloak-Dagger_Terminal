import sqlite3
import requests
import json
import csv
from ast import literal_eval
from bs4 import BeautifulSoup


conn = sqlite3.connect('data/game_data.sqlite')

c = conn.cursor()


c.execute("""CREATE TABLE IF NOT EXISTS items (
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


# c.execute("""CREATE TABLE IF NOT EXISTS enemies (
#         name TEXT,
#         ch_rating INTEGER,
#         armor_class INTEGER
#         )""")


# def insert_enemies():
#     url = "https://www.dnd5eapi.co/api/monsters/"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     soup = soup.text.strip("\"")
#     soup = soup.strip("'")
#     soup = soup.replace("true", "True")
#     soup = soup.replace("false", "False")
#     enemy_dict = literal_eval(soup)
#     results = enemy_dict["results"]
#     for enemy in results:
#         print(enemy)
#         name = enemy["index"].lower()
#         url = f"https://www.dnd5eapi.co/api/monsters/{name}"
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         soup = soup.text.strip("\"")
#         soup = soup.strip("'")
#         soup = soup.replace("true", "True")
#         soup = soup.replace("false", "False")
#         single_enemy_dict = literal_eval(soup)
#         with open(f"{single_enemy_dict['name']}.json", 'w') as enemy_json:
#             json.dump(single_enemy_dict, enemy_json)

#         c.execute(f"""INSERT INTO enemies (name, ch_rating, armor_class)
#                         VALUES ('{single_enemy_dict['name']}', {single_enemy_dict['challenge_rating']}, {single_enemy_dict['armor_class'][0]['value']})
#                         """)

def insert_items():
    url = "https://www.dnd5eapi.co/api/equipment/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup = soup.text.strip("\"")
    soup = soup.strip("'")
    soup = soup.replace("true", "True")
    soup = soup.replace("false", "False")
    item_dict = literal_eval(soup)
    print(item_dict)
    results = item_dict["results"]
    for item in results:
        print(item)
        name = item["index"].lower()
        url = f"https://www.dnd5eapi.co/api/equipment/{name}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        soup = soup.text.strip("\"")
        soup = soup.strip("'")
        soup = soup.replace("true", "True")
        soup = soup.replace("false", "False")
        single_item_dict = literal_eval(soup)
        single_item_dict["index"].lower()
        try:
            single_item_dict['rarity']
        except KeyError:
            single_item_dict['rarity'] = "None"
        try:
            weight = single_item_dict["weight"]
        except KeyError:
            weight = 0
        try:
            cost = f"{single_item_dict['cost']['quantity']} " + single_item_dict["cost"]["unit"]
        except KeyError:
            cost = 0
        if type(single_item_dict["desc"]) == list:
            try:
                desc = single_item_dict["desc"][0]
                desc = desc.replace("'", "")
                print(desc)
            except IndexError:
                desc = "None"
        else:
            desc = "None"
        if single_item_dict["equipment_category"]["index"] == "weapon":
            properties = single_item_dict["properties"]
            if len(properties) != 0:
                weap_property = single_item_dict["properties"][0]["index"]
            else:
                weap_property = "None"
        else:
            weap_property = "None"

        if single_item_dict["equipment_category"]["index"] == "weapon":
            try: 
                single_item_dict["damage"]
                dmg_dice = single_item_dict["damage"]["damage_dice"]
                dmg_dice_num = single_item_dict["damage"]["damage_dice_count"]
                dmg_type = single_item_dict["damage"]["damage_type"]["index"]
                th_dmg_dice = single_item_dict["two_handed_damage"]["damage_dice"]
                th_dmg_dice_num = single_item_dict["two_handed_damage"]["damage_dice_count"]
            except KeyError:
                dmg_dice = "None"
                dmg_dice_num = 0
                dmg_type = "None"
                th_dmg_dice = "None"
                th_dmg_dice_num = 0
        else:
            dmg_dice = "None"
            dmg_dice_num = 0
            dmg_type = "None"
            th_dmg_dice = "None"
            th_dmg_dice_num = 0

        c.execute(f"""INSERT INTO items (name, rarity, weight, cost, dmg_dice, th_dmg_dice, dmg_dice_num, th_dmg_dice_num,
                  weapon_type, weapon_property, item_type, description) VALUES ('{name}', '{single_item_dict['rarity']}', {weight}, 
                  '{cost}', '{dmg_dice}', '{th_dmg_dice}', {dmg_dice_num}, {th_dmg_dice_num}, '{dmg_type}', '{weap_property}', 
                  '{single_item_dict['equipment_category']['index']}', '{desc}')
                        """)

insert_items()
# insert_enemies()
conn.commit()
conn.close()