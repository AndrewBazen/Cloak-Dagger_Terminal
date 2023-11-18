import random
import dice_roll
import requests
from ast import literal_eval
from pyfiglet import Figlet
from bs4 import BeautifulSoup
import sqlite3
import dungeon

conn = sqlite3.connect('/data/game_data.sqlite')

c = conn.cursor()


class Adventurer:

    def __init__(self):
        self.name = ""
        self.race = ''
        self.level = 1
        self.exp_to_next_lvl = 100
        self.ad_class = ''
        self.has_adv = False
        self.max_hp = 15
        self.max_mp = 15
        self.hp = 15
        self.mp = 15
        self.backpack = {"Weapons": [], "Armor": [], "Consumables": [], "Other": []}
        self.equipped = {"Weapon": Item(), "Armor": Item()}
        self.stats = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}
        self.ac = 0
        self.modifiers = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}

    def set_player_stats(self, stats):
        print("Stats: 1. str")
        print("       2. dex")
        print("       3. con")
        print("       4. int")
        print("       5. wis")
        print("       6. cha")
        for stat in stats:
            bad_input = True
            while bad_input:
                choice = input("Which stat would you like to put {stat} into?".format(stat=stat))
                match choice:
                    case "1":
                        self.stats["str"] = stat
                        bad_input = False
                    case "2":
                        self.stats["dex"] = stat
                        bad_input = False
                    case "3":
                        if stat < 10:
                            self.max_hp -= 1
                            self.hp = self.max_hp
                        elif 10 <= stat < 13:
                            self.max_hp += 1
                            self.hp = self.max_hp
                        elif 13 <= stat < 16:
                            self.max_hp += 2
                            self.hp = self.max_hp
                        elif stat > 18:
                            self.max_hp += 3
                            self.hp = self.max_hp
                        self.stats["con"] = stat
                        bad_input = False
                    case "4":
                        if stat < 10:
                            self.max_mp -= 1
                            self.mp = self.max_mp
                        elif 10 <= stat < 13:
                            self.max_mp += 1
                            self.mp = self.max_mp
                        elif 13 <= stat < 16:
                            self.max_mp += 2
                            self.mp = self.max_mp
                        elif stat > 18:
                            self.max_mp += 3
                            self.mp = self.max_mp
                        self.stats["int"] = stat
                        bad_input = False
                    case "5":
                        self.stats["wis"] = stat
                        bad_input = False
                    case "6":
                        self.stats["cha"] = stat
                        bad_input = False
                    case _:
                        print("That is not an option!")
                        bad_input = True

    def attack(self, enemy):
        if self.hp != 0:
            if self.has_adv:
                if self.equipped["Weapon"].weapon_property == "versatile" or self.equipped["Weapon"].weapon_property ==\
                        "heavy" or self.equipped["Weapon"].weapon_property == "light":
                    hit_roll = max(dice_roll.roll(2, "d20")[0]) + self.modifiers["str"]
                    print("\n")
                    print(f"You rolled a {hit_roll}!")
                    dice_roll.attack_roll(hit_roll, self, enemy)
                elif self.equipped["Weapon"].weapon_property == "finesse" or self.equipped["Weapon"].weapon_property ==\
                        "thrown" or self.equipped["Weapon"].weapon_property == "ammunition" or \
                        self.equipped["Weapon"].weapon_property == "light":
                    hit_roll = max(dice_roll.roll(2, "d20")[0]) + self.modifiers["dex"]
                    print("\n")
                    print(f"You rolled a {hit_roll}!")
                    dice_roll.attack_roll(hit_roll, self, enemy)
                else:
                    hit_roll = max(dice_roll.roll(2, "d20")[0]) + self.modifiers["str"]
                    print("\n")
                    print(f"You rolled a {hit_roll}!")
                    dice_roll.attack_roll(hit_roll, self, enemy)
            elif not self.has_adv:
                if self.equipped["Weapon"].weapon_property == "versatile" or self.equipped["Weapon"].weapon_property ==\
                        "heavy" or self.equipped["Weapon"].weapon_property == "light":
                    hit_roll = dice_roll.roll(1, "d20")[1] + self.modifiers["str"]
                    print("\n")
                    print(f"You rolled a {hit_roll}!")
                    dice_roll.attack_roll(hit_roll, self, enemy)
                elif self.equipped["Weapon"].weapon_property == "finesse" or self.equipped["Weapon"].weapon_property ==\
                        "thrown" or self.equipped["Weapon"].weapon_property == "ammunition" or \
                        self.equipped["Weapon"].weapon_property == "light":
                    hit_roll = dice_roll.roll(1, "d20")[1] + self.modifiers["dex"]
                    print("\n")
                    print(f"You rolled a {hit_roll}!")
                    dice_roll.attack_roll(hit_roll, self, enemy)
                else:
                    hit_roll = dice_roll.roll(1, "d20")[1] + self.modifiers["str"]
                    print("\n")
                    print(f"You rolled a {hit_roll}!")
                    dice_roll.attack_roll(hit_roll, self, enemy)

    def set_starting_equip(self, equipment):
        class_type = self.ad_class
        match class_type:
            case "barbarian":
                self.equipped["Weapon"] = equipment[0]
                self.equipped["Armor"] = equipment[17]
            case "rogue":
                self.equipped["Weapon"] = equipment[9]
                self.equipped["Armor"] = equipment[17]
            case "ranger":
                self.equipped["Weapon"] = equipment[24]
                self.equipped["Armor"] = equipment[17]
            case "paladin":
                self.equipped["Weapon"] = equipment[25]
                self.equipped["Armor"] = equipment[17]
            case "cleric":
                self.equipped["Weapon"] = equipment[26]
                self.equipped["Armor"] = equipment[17]
            case "wizard":
                self.equipped["Weapon"] = equipment[33]
                self.equipped["Armor"] = equipment[17]
            case "warlock":
                self.equipped["Weapon"] = equipment[40]
                self.equipped["Armor"] = equipment[17]
            case "fighter":
                self.equipped["Weapon"] = equipment[40]
                self.equipped["Armor"] = equipment[17]

    def equip_weapon(self, item):
        if self.equipped["Weapon"] != "":
            replace = input("You already have {cur} equipped, would you like to replace it with {item} "
                            "(y/n)?".format(cur=self.equipped["Weapon"], item=item))
            # replaces equipped weapon or places the new weapon in the backpack
            if replace == 'y' or replace == 'Y':
                self.backpack["Weapons"].append(self.equipped["Weapon"])
                self.equipped["Weapon"] = item
                print("You placed the {cur} in your backpack and equipped the "
                      "{item}".format(cur=self.equipped["Weapon"], item=item))
            elif replace == 'n' or replace == 'N':
                return
        else:
            self.equipped["Weapon"] = item
            print("You are now wielding the {item}".format(item=item))

    def equip_armor(self, item):
        if self.equipped["Armor"] != "":
            replace = input("You already have {cur} equipped, would you like to replace it with {item} "
                            "(y/n)?".format(cur=self.equipped["Armor"], item=item))
            # replaces equipped weapon or places the new weapon in the backpack
            if replace == 'y' or replace == 'Y':
                self.backpack["Armor"].append(self.equipped["Armor"])
                self.equipped["Armor"] = item
                print("You placed the {cur} in your backpack and equipped the "
                      "{item}".format(cur=self.equipped["Armor"], item=item))
            elif replace == 'n' or replace == 'N':
                return
        else:
            self.equipped["Armor"] = item
            print("You are now wielding the {item}".format(item=item))

    def add_item(self, item):
        # check if the item is a consumable, weapon, armor, or other
        if item.item_type == "consumable":
            # place it in the backpack print a message
            self.backpack["Consumables"].append(item)
            print("You placed the {item} in your backpack".format(item=item))
        elif item.item_type == "weapon" or item.item_type == "magic_weapon":
            # checks if the user wants to equip the new weapon
            ans = input("Would you like to equip {item} (y/n)?")
            # if the weapon slot is empty it is equipped otherwise it asks to replace weapons
            if ans == 'y' or ans == 'Y':
                self.equip_weapon(item)
            elif ans == 'n' or ans == 'N':
                self.backpack["Weapons"].append(item)
                print("You placed the {item} in your backpack".format(item=item))
        elif item.item_type == "armor" or item.item_type == "magic_armor":
            ans = input("Would you like to equip {item} (y/n)?")
            if ans == 'y' or ans == 'Y':
                self.equip_armor(item)
            elif ans == 'n' or ans == 'N':
                self.backpack["Armor"].append(item)
                print("You placed the {item} in your backpack".format(item=item))
        else:
            # place it in the backpack print a message
            self.backpack["Other"].append(item)
            print("You placed the {item} in your backpack".format(item=item))

    def use_item(self, item, target):
        if item.item_type == "consumable":
            effect = dice_roll.roll(item.effect_dice[0], item.effect_dice[1])
            if item.effect == "inc_health" and effect < self.max_hp - self.hp:
                self.hp += effect
                print("You use the {item} and regain {hp} health!".format(item=item, hp=effect))
                print("Your health is now {hp}/{max}".format(hp=self.hp, max=self.max_hp))
            elif item.effect == "inc_health" and effect >= self.max_hp - self.hp:
                self.hp = self.max_hp
                print("You use the {item} and regain {hp} health!".format(item=item, hp=effect))
                print("Your health is now {hp}/{max}".format(hp=self.hp, max=self.max_hp))
            elif item.effect == "inc_mana" and effect < self.max_mp - self.mp:
                self.mp += effect
                print("You use the {item} and regain {mp} mana!".format(item=item, mp=effect))
                print("Your health is now {mp}/{max}".format(mp=self.mp, max=self.max_mp))
            elif item.effect == "inc_mana" and effect >= self.max_mp - self.mp:
                self.mp = self.max_mp
                print("You use the {item} and regain {mp} health!".format(item=item, mp=effect))
                print("Your health is now {mp}/{max}".format(mp=self.mp, max=self.max_mp))
        elif item.item_type == "other":
            return item.interaction(target)
        else:
            print("That is not a usable item!")

    def check_inventory(self):
        for item in self.backpack:
            print("- {item}".format(item=item))
            for i in self.backpack[item]:
                print(f"    - {i.name}")

    def __repr__(self):
        return f"--- {self.name} ---\nRace: {self.race}  Class: {self.ad_class}\nHP: {self.hp}  MP: {self.mp}\n" \
               f"Stats: Str Dex Con Int Wis Cha\n        {self.stats}"


class Enemy:

    def __init__(self, name):
        self.name = name
        self.ch_rating = 0
        self.backpack = []
        self.equipped = {"Weapon": Item(), "Armor": Item()}
        self.ac = 0
        self.hp = 0
        self.mp = 0
        self.stats = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}
        self.str = 0
        self.dex = 0
        self.con = 0
        self.int = 0
        self.wis = 0
        self.cha = 0
        self.modifiers = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}

    def attack(self, player):
        if self.hp != 0:
            hit_roll = dice_roll.roll(1, "d20")[1]
            result = dice_roll.enemy_attack_roll(hit_roll, self, player)
            return result

    def set_starting_equip(self, weapon, armor):
        self.equipped["Weapon"] = weapon
        self.equipped["Armor"] = armor

    def set_stats(self):
        info = get_monster_info(self)
        self.ch_rating = info['challenge_rating']
        self.ac = info['armor_class'] + self.equipped["Armor"].bonus
        self.hp = info['hit_points']
        self.stats["str"] = info['strength']
        self.stats["dex"] = info['dexterity']
        self.stats["con"] = info['constitution']
        self.stats["int"] = info['intelligence']
        self.stats["wis"] = info['wisdom']
        self.stats["cha"] = info['charisma']
        if "spellcasting" in info:
            self.mp = self.int * self.ch_rating
        else:
            self.mp = 0

    def __repr__(self):
        return f"--- {self.name} ---\nChallenge Rating: {self.ch_rating}\nArmor Class: {self.ac}\nHP: {self.hp}  " \
               f"MP: {self.mp}"

    def __init__(self, name="Empty", effect="None"):
        self.name = name
        self.rarity = ""
        self.bonus = 0
        self.effect = effect
        self.effect_dice = ""
        self.weapon_type = ""
        self.weapon_property = ""
        self.item_type = ""
        self.description = ""


    def interaction(self, target):
        pass

    def __repr__(self):
        return f"--- {self.name} ---\nType: {self.item_type}  description: {self.description}"

class

def set_modifiers(player):
    stats = player.stats.items()
    for stat in stats:
        if 6 <= stat[1] <= 7:
            player.modifiers[stat[0]] = -2
        elif 8 <= stat[1] <= 9:
            player.modifiers[stat[0]] = -1
        elif 12 <= stat[1] <= 13:
            player.modifiers[stat[0]] = 1
        elif 14 <= stat[1] <= 15:
            player.modifiers[stat[0]] = 2
        elif 16 <= stat[1] <= 17:
            player.modifiers[stat[0]] = 3
        elif 18 <= stat[1]:
            player.modifiers[stat[0]] = 4


def get_enemy_info(monster):
    pass


def get_item_info(item):
    name = item.name
    pass


def create_character(ad, classes, races):
    keep_character = False
    while not keep_character:
        ad.name = input("What is your name, Adventurer?")
        print(f"\nHello {ad.name}, what race are you?\n")
        print("--- Races ---")
        for race in races:
            print(race)
        print("\n")
        while ad.race == "":
            temp_race = input("")
            if temp_race in races:
                ad.race = temp_race
            else:
                print("That race does not exist! please choose another")

        print("\nWhat class are you?\n")
        print("--- Classes ---")
        for cl in classes:
            print(cl)
        print("\n")
        while ad.ad_class == "":
            temp_class = input("")
            if temp_class in classes:
                ad.ad_class = temp_class
            else:
                print("That class does not exist! please choose another")

        print("Here is your adventurer!\n")
        print(f"--- {ad.name} ---")
        print(f"Race: {ad.race}")
        print(f"Class: {ad.ad_class}")
        print("would you like to keep this character and roll stats? (y/n)")

        correct_input = False
        while not correct_input:
            ad_choice = input("")
            if ad_choice == 'y' or ad_choice == 'Y':
                keep_character = True
                correct_input = True
            elif ad_choice == 'n' or ad_choice == 'N':
                keep_character = False
                correct_input = True
            else:
                print("That is not an option!")
                print("would you like to keep this character and roll stats? (y/n)")


def main_menu():
    print("****      Game Menu      ****")
    print("1. Check Character")
    print("2. Check Inventory")
    print("3. Enter Dungeon")
    print("4. Quit game")


def in_game_menu():
    print("****      Game Menu      ****")
    print("1. Check Character")
    print("2. Check Inventory")
    print("3  Pick up item")
    print("4. Next Room")
    print("5. Quit game")


def inventory_menu():
    print("****      Inventory Menu      ****")
    print("1. List inventory")
    print("2. Equip item")
    print("3. Go back")


def fight_menu():
    print("****      Fight      ****")
    print("1. List inventory")
    print("2. Use item")
    print("3. attack")
    print("4. Run")


def reveal_room(room, ad):
    room_type = room.val
    match room_type:
        case "Fight room":
            print(f"your find yourself in a dark room with {room.num_enemies} {room.enemies.name}s")
            game_over = fight(room.num_enemies, room.enemies, ad)
            if game_over:
                return game_over
        case "Loot room":
            pass
        case "Empty room":
            pass
        case "boss room":
            pass


def get_enemies(enemies):
    pass


def get_equipment(equipment):
    pass


def get_loot(loot):
    pass


def get_rare_loot(rare_loot):
    pass


def fight(num_enemies, enemy, player):
    done = False
    while player.hp > 0 and num_enemies > 0:
        new_enemy = enemy
        while not done:
            print(f"{enemy.name}s left: {num_enemies}")
            print(f"Current {enemy.name}s health: {enemy.hp}")
            print("\n")
            print(f"Your health: {player.hp}")
            print("\n")
            fight_menu()
            fight_option = input("What would you like to do?")
            match int(fight_option):
                case 1:
                    player.check_inventory()
                case 2:
                    print("\n")
                    player.check_inventory()
                    use = input("Which item would you like to use?")
                    for item in player.backpack["Consumables"]:
                        if item.name == use:
                            player.use_item(item)
                        else:
                            print("That item is not in your backpack!")
                case 3:
                    player.attack(new_enemy)
                    if new_enemy.hp <= 0:
                        num_enemies -= 1
                        print("\n")
                        print(f"There are {num_enemies} left!")
                    else:
                        result = new_enemy.attack(player)
                        if result:
                            return result


def main():
    choice = 0
    curr_char_alive = True
    equipment = []
    get_equipment(equipment)
    print(equipment)
    loot = []
    get_loot_table(loot)
    rare_loot_table = []
    get_rare_loot_table(rare_loot_table)
    enemies = [Enemy("Goblin"), Enemy("Bandit"), Enemy("Cultist"), Enemy("Satyr")]
    bosses = [Enemy("BugBear"), Enemy("Dire Wolf"), Enemy("Dryad"), Enemy("Cult Fanatic")]
    puzzles = []
    puzzle_keys = [Item("Large Gem", "other", ),
                   Item("Large Gem", "other")]
    for enemy in enemies:
        enemy.set_stats()
        set_modifiers(enemy)
        enemy.set_starting_equip(equipment[5], equipment[17])
    for boss in bosses:
        boss.set_stats()
        set_modifiers(boss)
        boss.set_starting_equip(equipment[5], equipment[17])

    races = ["elf", "dwarf", "teifling", "halfling", "goliath"]
    classes = ["barbarian", "rogue", "ranger", "paladin", "cleric", "wizard", "warlock", "fighter"]
    ad = Adventurer()
    ad.set_starting_equip(equipment)

    custom_banner = Figlet(font='rozzo')
    print(custom_banner.renderText('Cloak\n   &\nDagger'))
    print("\n Hello and welcome to the world of DnD!")
    print("-----------------------------------------")

    while choice != "4":
        create_character(ad, classes, races)
        print("\nHere are your stats!")
        ad_stats = dice_roll.roll_stats()
        print(ad_stats)
        print("\n")
        ad.set_player_stats(ad_stats)
        set_modifiers(ad)
        print(ad)
        print(ad.modifiers)
        while choice != "4" and curr_char_alive:
            main_menu()
            choice = input("Please make a selection")
            match int(choice):
                case 1:
                    print("\n")
                    print(ad)
                    print("\n")
                case 2:
                    print("\n")
                    inv_choice = 0
                    while inv_choice != "3":
                        inventory_menu()
                        inv_choice = input("please make a selection")
                        match int(inv_choice):
                            case 1:
                                ad.check_inventory()
                            case 2:
                                done = False
                                while not done:
                                    print("\n")
                                    equip = input("Which item would you like to equip?")
                                    for item in ad.backpack["Weapons"]:
                                        if item.name == equip:
                                            ad.equip_weapon(item)
                                            done = True
                                    for item in ad.backpack["Armor"]:
                                        if item.name == equip:
                                            ad.equip_armor(item)
                                            done = True
                                        else:
                                            print("That item is not in your backpack!")
                case 3:
                    new_dungeon = dungeon.create_dungeon(ad.level, loot, rare_loot_table, puzzle_keys, enemies, bosses,
                                                         random.randint(4, 10), puzzles)
                    while not new_dungeon.is_empty():
                        game_over = reveal_room(new_dungeon.head, ad)
                        if game_over:
                            curr_char_alive = False
                            break
                        else:
                            new_dungeon.remove(new_dungeon.head)

    return


if __name__ == "__main__":
    main()
