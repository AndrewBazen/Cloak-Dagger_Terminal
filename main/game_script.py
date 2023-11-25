import random
import dice_roll
from pyfiglet import Figlet
import dungeon


class Adventurer:

    def __init__(self):
        self.name = ""
        self.race = Race()
        self.level = 1
        self.total_exp = 0
        self.exp_to_next_lvl = 100
        self.ad_class = AdClass()
        self.has_adv = False
        self.num_actions = 1
        self.max_hp = 15
        self.max_mp = 15
        self.hp = 15
        self.mp = 15
        self.backpack = {"Weapons": [], "Armor": [], "Consumables": [
                Consumable("Potion of Healing", "consumable", "common", "A potion that heals 1d4+1 health", "inc_health"),
                Consumable("Potion of Mana", "consumable", "common", "A potion that heals 1d4+1 mana", "inc_mana"),
            ], "Other": [
                Item("Rope", "other", "common", "A 50ft rope"),
                Item("Torch", "other", "common", "A torch"),
                Item("Bedroll", "other", "common", "A bedroll"),
            ]}
        self.equipped = {"Weapon": Weapon(), "Armor": Armor()}
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
                        self.stats["str"] = stat + self.race.modifiers["str"] + self.ad_class.modifiers["str"]
                        bad_input = False
                    case "2":
                        self.stats["dex"] = stat + self.race.modifiers["str"] + self.ad_class.modifiers["str"]
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
                        self.stats["con"] = stat + self.race.modifiers["str"] + self.ad_class.modifiers["str"]
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
                        self.stats["int"] = stat + self.race.modifiers["str"] + self.ad_class.modifiers["str"]
                        bad_input = False
                    case "5":
                        self.stats["wis"] = stat + self.race.modifiers["str"] + self.ad_class.modifiers["str"]
                        bad_input = False
                    case "6":
                        self.stats["cha"] = stat + self.race.modifiers["str"] + self.ad_class.modifiers["str"]
                        bad_input = False
                    case _:
                        print("That is not an option!")
                        bad_input = True
                        
    def update_stats(self):
            self.ac = self.equipped["Armor"].ac + self.modifiers["dex"]
        self.max_hp = 15 + self.modifiers["con"]
        self.max_mp = 15 + self.modifiers["int"]
        self.hp = self.max_hp
        self.mp = self.max_mp
        
    def level_up(self):
        self.level += 1
        self.exp_to_next_lvl += self.exp_to_next_lvl * 1.5
        self.max_hp += dice_roll.roll(1, self.hit_dice)[1]
        self.max_mp += dice_roll.roll(1, self.hit_dice)[1]
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.num_attacks += 1
        self.update_stats()

    def attack(self, enemy):
        if self.hp != 0:
            if self.has_adv:
                if self.equipped["Weapon"].weapon_type == "versatile" or self.equipped["Weapon"].weapon_type == "two-handed" \
                    or self.equipped["Weapon"].weapon_type == "heavy":
                    hit_roll = max(dice_roll.roll(2, "d20")[0]) + self.modifiers["str"] + self.equipped["Weapon"].bonus
                    print("\n")
                    print(f"You rolled a {hit_roll}!")
                    result = dice_roll.attack_roll(hit_roll, self, enemy)
                elif self.equipped["Weapon"].weapon_type == "finesse" or self.equipped["Weapon"].weapon_type ==\
                        "ranged" or self.equipped["Weapon"].weapon_type == "thrown":
                    hit_roll = max(dice_roll.roll(2, "d20")[0]) + self.modifiers["dex"] + self.equipped["Weapon"].bonus
                    print("\n")
                    print(f"You rolled a {hit_roll}!")
                    result = dice_roll.attack_roll(hit_roll, self, enemy)
                else:
                    hit_roll = max(dice_roll.roll(2, "d20")[0]) + self.modifiers["str"] + self.equipped["Weapon"].bonus
                    print("\n")
                    print(f"You rolled a {hit_roll}!")
                    result = dice_roll.attack_roll(hit_roll, self, enemy)
            elif not self.has_adv:
                if self.equipped["Weapon"].weapon_type == "versatile" or self.equipped["Weapon"].weapon_type == "two-handed" \
                    or self.equipped["Weapon"].weapon_type == "heavy":
                    hit_roll = max(dice_roll.roll(1, "d20")[0]) + self.modifiers["str"] + self.equipped["Weapon"].bonus
                    print("\n")
                    print(f"You rolled a {hit_roll}!")
                    result = dice_roll.attack_roll(hit_roll, self, enemy)
                elif self.equipped["Weapon"].weapon_type == "finesse" or self.equipped["Weapon"].weapon_type ==\
                        "ranged" or self.equipped["Weapon"].weapon_type == "thrown":
                    hit_roll = dice_roll.roll(1, "d20")[1] + self.modifiers["dex"] + self.equipped["Weapon"].bonus
                    print("\n")
                    print(f"You rolled a {hit_roll}!")
                    result = dice_roll.attack_roll(hit_roll, self, enemy)
                else:
                    hit_roll = dice_roll.roll(1, "d20")[1] + self.modifiers["str"] + self.equipped["Weapon"].bonus
                    print("\n")
                    print(f"You rolled a {hit_roll}!")
                    result = dice_roll.attack_roll(hit_roll, self, enemy)
            return result

    def set_starting_equip(self, weapons, armor):
        class_type = self.ad_class
        match class_type:
            case "barbarian":
                self.equipped["Weapon"] = weapons["Handaxe"]
                self.equipped["Armor"] = armor["Hide"]
            case "rogue":
                self.equipped["Weapon"] = weapons["Dagger"]
                self.equipped["Armor"] = armor["Leather"]
            case "ranger":
                self.equipped["Weapon"] = weapons["Shortbow"]
                self.equipped["Armor"] = armor["Leather"]
            case "paladin":
                self.equipped["Weapon"] = weapons["Shortsword"]
                self.equipped["Armor"] = armor["half-plate"]
            case "cleric":
                self.equipped["Weapon"] = weapons["Mace"]
                self.equipped["Armor"] = armor["Chainmail"]
            case "wizard":
                self.equipped["Weapon"] = weapons["Quarterstaff"]
            case "warlock":
                self.equipped["Weapon"] = weapons["Quarterstaff"]
            case "fighter":
                self.equipped["Weapon"] = weapons["spear"]
                self.equipped["Armor"] = armor["Leather"]

    def equip_weapon(self, item):
        if self.equipped["Weapon"] != "Empty":
            replace = input("You already have {cur} equipped, would you like to replace it with {item} "
                            "(y/n)?".format(cur=self.equipped["Weapon"], item=item))
            # replaces equipped weapon or places the new weapon in the backpack
            if replace == 'y' or replace == 'Y':
                self.add_item(self.equipped["Weapon"])
                self.equipped["Weapon"] = item
                print("You placed the {cur} in your backpack and equipped the "
                      "{item}".format(cur=self.equipped["Weapon"], item=item))
            elif replace == 'n' or replace == 'N':
                self.add_item(item)
                print("You placed the {item} in your backpack and equipped the ".format(item=item))
                return
        else:
            self.equipped["Weapon"] = item
            print("You are now wielding the {item}".format(item=item))

    def equip_armor(self, item):
        if self.equipped["Armor"] != "Empty":
            replace = input("You already have {cur} equipped, would you like to replace it with {item} "
                            "(y/n)?".format(cur=self.equipped["Armor"], item=item))
            # replaces equipped weapon or places the new weapon in the backpack
            if replace == 'y' or replace == 'Y':
                self.add_item(self.equipped["Armor"])
                self.equipped["Armor"] = item
                print("You placed the {cur} in your backpack and equipped the "
                      "{item}".format(cur=self.equipped["Armor"], item=item))
            elif replace == 'n' or replace == 'N':
                self.add_item(item)
                print("You placed the {item} in your backpack and equipped the ".format(item=item))
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
               
               
class AdClass:
    """
    class for character classes
    """
    
    def __init__(self, name, hit_dice, modifiers={"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}):
        self.name = name
        self.hit_dice = hit_dice
        self.modifiers = modifiers
        
        
class Race:
    """
    class for character races
    """
    
    def __init__(self, name="", modifiers={"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}):
        self.name = name
        self.modifiers = modifiers


class Enemy:

    def __init__(self, name, ch_rating, drop_class, ac, hp, mp, stats, modifiers):
        self.name = name
        self.ch_rating = ch_rating
        self.drop_class = drop_class
        self.equipped = {"Weapon": Weapon(), "Armor": Armor()}
        self.ac = ac
        self.hp = hp
        self.mp = mp
        self.stats = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}
        self.modifiers = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}

    def attack(self, player):
        if self.hp != 0:
            hit_roll = dice_roll.roll(1, "d20")[1]
            result = dice_roll.enemy_attack_roll(hit_roll, self, player)
            return result

    def __repr__(self):
        return f"--- {self.name} ---\nChallenge Rating: {self.ch_rating}\nArmor Class: {self.ac}\nHP: {self.hp}  " \
               f"MP: {self.mp}"
               
class Item:

    def __init__(self, name="Empty", item_type="other", rarity="common", description=""):
        self.name = name
        self.item_type = ""
        self.rarity = ""
        self.description = ""

    def __repr__(self):
        return f"--- {self.name} ---\nType: {self.item_type} Rarity: {self.rarity}\nDescription: {self.description}"
    
class Weapon(Item):
    
    def __init__(self, name="Empty", item_type="weapon", rarity="common", description="", weapon_type="",
                 dmg_dice_num=1, damage_dice="", bonus=0):
        super().__init__(name, item_type, rarity, description)
        self.weapon_type = weapon_type
        self.dmg_dice_num = dmg_dice_num
        self.damage_dice = damage_dice
        self.bonus = bonus

class Armor(Item):
    
    def __init__(self, name="Empty", item_type="armor", rarity="common", description="", ac=0, bonus=0):
        super().__init__(name, item_type, rarity, description)
        self.ac = ac
        self.bonus = bonus
        
class Consumable(Item):
    
    def __init__(self, name="Empty", item_type="consumable", rarity="common", description="", effect="",
                 effect_dice=()):
        super().__init__(name, item_type, rarity, description)
        self.effect = effect
        self.effect_dice = effect_dice
        


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


def create_character(ad, classes, races):
    while not keep_character:                                                     
        ad.name = input("What is your name, Adventurer?")                          
        print(f"\nHello {ad.name}, what race are you?\n")                       
        print("--- Races ---") 
        for race in races:
            print(race.name)
        print("\n")
        
        # While loop to check if an available race has been chosen
        while ad.race == "":                                                         
            temp_race = input("")
            for race in races:
                if temp_race == race.name:
                    ad.race = temp_race
                else:
                    continue
            if ad.race == "":
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
    weapons = {
        "Shortsword": Weapon("Shortsword", "weapon", "common", "A simple sword", "simple", 1, "d6", 0),
        "Longsword": Weapon("Longsword", "weapon", "uncommon", "A simple sword", "versatile", 1, "d8", 0),
        "Greatsword": Weapon("Greatsword", "weapon", "rare", "A simple sword", "two-handed", 1, "d10", 0),
        "Rapier": Weapon("Rapier", "weapon", "common", "A simple sword", "finesse", 1, "d8", 0),
        "Dagger": Weapon("Dagger", "weapon", "common", "A simple sword", "simple", 1, "d4", 0),
        "Shortbow": Weapon("Shortbow", "weapon", "common", "A simple sword", "ranged", 1, "d6", 0),
        "Longbow": Weapon("Longbow", "weapon", "uncommon", "A simple sword", "ranged", 1, "d8", 0),
        "Greatbow": Weapon("Greatbow", "weapon", "rare", "A simple sword", "ranged", 1, "d10", 0),
        "Handaxe": Weapon("Handaxe", "weapon", "common", "A simple sword", "simple", 1, "d6", 0),
        "Battleaxe": Weapon("Battleaxe", "weapon", "uncommon", "A simple sword", "versatile", 1, "d8", 0),
        "Greataxe": Weapon("Greataxe", "weapon", "rare", "A simple sword", "two-handed", 1, "d10", 0),
        "Mace": Weapon("Mace", "weapon", "common", "A simple sword", "simple", 1, "d6", 0),
        "Warhammer": Weapon("Warhammer", "weapon", "uncommon", "A simple sword", "versatile", 1, "d8", 0),
        "BattleStaff": Weapon("staff", "weapon", "rare", "A simple sword", "two-handed", 1, "d10", 0),
        "Quarterstaff": Weapon("quarterstaff", "weapon", "common", "A simple sword", "simple", 1, "d6", 0),
        "Spear": Weapon("spear", "weapon", "uncommon", "A simple sword", "versatile", 1, "d8", 0),
    }
    armor = {
        "Leather": Armor("Leather", "armor", "common", "A simple sword", 11, 0),
        "Chainmail": Armor("Chainmail", "armor", "uncommon", "A simple sword", 13, 0),
        "Plate": Armor("Plate", "armor", "rare", "A simple sword", 15, 0),
        "Half-Plate": Armor("Half-Plate", "armor", "uncommon", "A simple sword", 14, 0),
        "Scale": Armor("Scale", "armor", "common", "A simple sword", 12, 0),
    }
    loot = {
      
    }
    rare_loot = {
        
    }
    enemies = {
        
    }
    bosses = {
        
    }
    puzzles = {
        
    }
    puzzle_keys = {
        
    }
    races = ["elf", "dwarf", "teifling", "halfling", "goliath"]
    classes = ["barbarian", "rogue", "ranger", "paladin", "cleric", "wizard", "warlock", "fighter"]
    
    ad = Adventurer()

    custom_banner = Figlet(font='rozzo')
    print(custom_banner.renderText('Cloak\n   &\nDagger'))
    print("\n Hello and welcome to the world of DnD!")
    print("-----------------------------------------")

    while choice != "4":
        create_character(ad, classes, races)
        ad.set_starting_equip(weapons, armor)
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
                    new_dungeon = dungeon.create_dungeon(ad.level, loot, rare_loot, puzzle_keys, enemies, bosses,
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
