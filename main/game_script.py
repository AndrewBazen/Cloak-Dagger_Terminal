import random
import dice_roll
from pyfiglet import Figlet
import dungeon
import os
import shutil


class Adventurer:
    """
    the class for the player object
    """

    def __init__(self):
        self.name = ""
        self.race = Race()
        self.level = 1
        self.total_exp = 0
        self.exp_to_next_lvl = 100
        self.ad_class = AdClass()
        self.has_attack = True
        self.has_adv = False
        self.num_actions = 1
        self.max_hp = 15
        self.max_mp = 15
        self.hp = 15
        self.mp = 15
        # creates a dictionary for the player's backpack and preloads it with some items
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
        """
        prompts the user to set their stats

        Args:
            stats (Dictionary): the stats of the player
        """
        print("Stats: 1. str")
        print("       2. dex")
        print("       3. con")
        print("       4. int")
        print("       5. wis")
        print("       6. cha")
        for stat in stats:               # iterates through the stats
            bad_input = True
            
            # while loop to check if the user input is valid
            while bad_input:
                choice = input("Which stat would you like to put {stat} into?".format(stat=stat))    # prompts the user to choose a stat
                match choice:
                    case "1":        # checks if the user chose strength
                        self.stats["str"] = stat + self.race.modifiers["str"] + self.ad_class.modifiers["str"]
                        bad_input = False
                    case "2":        # checks if the user chose dexterity
                        self.stats["dex"] = stat + self.race.modifiers["str"] + self.ad_class.modifiers["str"]
                        bad_input = False
                    case "3":        # checks if the user chose constitution
                        # modifies the max hp based on the constitution stat
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
                    case "4":       # checks if the user chose intelligence
                        # modifies the max mp based on the intelligence stat
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
                    case "5":      # checks if the user chose wisdom
                        self.stats["wis"] = stat + self.race.modifiers["str"] + self.ad_class.modifiers["str"]
                        bad_input = False
                    case "6":     # checks if the user chose charisma
                        self.stats["cha"] = stat + self.race.modifiers["str"] + self.ad_class.modifiers["str"]
                        bad_input = False
                    case _:      # checks if the user chose an invalid option
                        print("That is not an option!")
                        bad_input = True
                        
    def update_stats(self):
        """
        recalculates the stats of the player
        """
        if self.equipped["Armor"] != "Empty":
            self.ac = self.equipped["Armor"].ac + self.modifiers["dex"]
        self.max_hp = 15 + self.modifiers["con"]
        self.max_mp = 15 + self.modifiers["int"]
        self.hp = self.max_hp
        self.mp = self.max_mp
        
    def level_up(self):
        """
        adds a level to the player and adjusts the stats accordingly
        """
        self.level += 1
        self.exp_to_next_lvl += self.exp_to_next_lvl * 1.5
        self.max_hp += dice_roll.roll(1, self.hit_dice)[1]
        self.max_mp += dice_roll.roll(1, self.hit_dice)[1]
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.num_attacks += 1
        
    def print_experience_bar(self, current_exp, next_level_exp):
        # Calculate the ratio of current experience to the experience needed
        ratio = current_exp / next_level_exp

        # Determine the width of the terminal
        terminal_width = shutil.get_terminal_size((80, 20)).columns/4

        # Calculate the number of characters to represent the experience bar
        bar_length = int(ratio * terminal_width)

        # Create the experience bar string
        exp_bar = '|' + '#' * bar_length + '-' * int(terminal_width - bar_length) + '|' + \
                    f' {current_exp}/{next_level_exp}'
                    
        # Print the experience bar
        print(exp_bar)

    def attack(self, enemy):
        """
        attack function for the player

        Args:
            enemy (Enemy): the enemy object

        Returns:
            Boolean: True if the player hits, False if the player misses
        """
        if self.hp != 0:     # checks if the player is alive
            # checks if the player has advantage or not
            if self.has_adv:
                # checks if the player has a strength or dexterity based weapon
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
        """
        sets the starting equipment for the player based on their class

        Args:
            weapons (Dictionary): the weapons dictionary
            armor (Dictionary): the armor dictionary
        """
        class_type = self.ad_class.name
        match class_type:
            case "barbarian":    # checks if the player is a barbarian
                self.equipped["Weapon"] = weapons["Handaxe"]
                self.equipped["Armor"] = armor["Hide"]
            case "rogue":        # checks if the player is a rogue
                self.equipped["Weapon"] = weapons["Dagger"]
                self.equipped["Armor"] = armor["Leather"]
            case "ranger":       # checks if the player is a ranger
                self.equipped["Weapon"] = weapons["Shortbow"]
                self.equipped["Armor"] = armor["Leather"]
            case "paladin":      # checks if the player is a paladin
                self.equipped["Weapon"] = weapons["Shortsword"]
                self.equipped["Armor"] = armor["Half-plate"]
            case "cleric":       # checks if the player is a cleric
                self.equipped["Weapon"] = weapons["Mace"]
                self.equipped["Armor"] = armor["Chainmail"]
            case "wizard":       # checks if the player is a wizard
                self.equipped["Weapon"] = weapons["Quarterstaff"]
            case "warlock":      # checks if the player is a warlock
                self.equipped["Weapon"] = weapons["Quarterstaff"]
            case "fighter":      # checks if the player is a fighter
                self.equipped["Weapon"] = weapons["Spear"]
                self.equipped["Armor"] = armor["Leather"]

    def equip_weapon(self, item):
        """
        equips a weapon to the player or replaces the equipped weapon

        Args:
            item (Weapon): the weapon to be equipped
        """
        if self.equipped["Weapon"] != "Empty":    # checks if the weapon slot is empty
            # asks the user if they want to replace the equipped weapon
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
        else:  # if the weapon slot is empty equip the weapon
            self.equipped["Weapon"] = item   
            print("You are now wielding the {item}".format(item=item))

    def equip_armor(self, item):
        """
        equips armor to the player or replaces the equipped armor

        Args:
            item (Armor): the armor to be equipped
        """
        if self.equipped["Armor"] != "Empty":  # checks if the armor slot is empty
            # asks the user if they want to replace the equipped armor
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
        else: # if the armor slot is empty equip the armor
            self.equipped["Armor"] = item
            print("You are now wielding the {item}".format(item=item))

    def add_item(self, item):
        """
        adds an item to the player's backpack

        Args:
            item (Item): the item to be added
        """
        # check if the item is a consumable, weapon, armor, or other item
        if item.item_type == "consumable":
            self.backpack["Consumables"].append(item)
            print("You placed the {item} in your backpack".format(item=item))
        elif item.item_type == "weapon" or item.item_type == "magic_weapon": 
            ans = input("Would you like to equip {item} (y/n)?")
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

            self.backpack["Other"].append(item)
            print("You placed the {item} in your backpack".format(item=item))

    def use_item(self, item, target):
        """
        allows the player to use an item, checking if it is a consumable or other item and its effect

        Args:
            item (Item): the item to be used
            target (Enemy): the enemy to be targeted
        """
        if item.item_type == "consumable":
            effect = dice_roll.roll(item.effect_dice[0], item.effect_dice[1])
            if item.effect == "inc_health" and effect < self.max_hp - self.hp:                     # if effect is less than total lost health
                self.hp += effect
                print("You use the {item} and regain {hp} health!".format(item=item, hp=effect))
                print("Your health is now {hp}/{max}".format(hp=self.hp, max=self.max_hp))
            elif item.effect == "inc_health" and effect >= self.max_hp - self.hp:                  # if effect is greater than total lost health
                self.hp = self.max_hp
                print("You use the {item} and regain {hp} health!".format(item=item, hp=effect))
                print("Your health is now {hp}/{max}".format(hp=self.hp, max=self.max_hp))
            elif item.effect == "inc_mana" and effect < self.max_mp - self.mp:                     # if effect is less than total lost mana
                self.mp += effect
                print("You use the {item} and regain {mp} mana!".format(item=item, mp=effect))
                print("Your health is now {mp}/{max}".format(mp=self.mp, max=self.max_mp))
            elif item.effect == "inc_mana" and effect >= self.max_mp - self.mp:                    # if effect is greater than total lost mana
                self.mp = self.max_mp
                print("You use the {item} and regain {mp} health!".format(item=item, mp=effect))
                print("Your health is now {mp}/{max}".format(mp=self.mp, max=self.max_mp))
        # TODO: add other item effects
        elif item.item_type == "other":
            item.interaction(target)    # TODO: add interaction function to other items
        else:
            print("That is not a usable item!")

    def check_inventory(self):
        """
        prints the inventory of the player
        """
        print("\n     ******  Inventory  ******")
        print("\n")
        print("Equipped:")
        print(f"\n     Weapon: {self.equipped['Weapon'].name}    Armor: {self.equipped['Armor'].name}")
        print("\n")
        print("Backpack:")
        for item in self.backpack:
            print(f"\n  - {item}\n")
            for i in self.backpack[item]:
                print(f"    - {i.name}")
        print("\n")
                
    def print_character_sheet(self):
        """
        prints the character sheet of the player
        """
        print("\n                          **** Character Sheet ****")
        print("\n")
        print("Character Name: {}     Race: {}     Class: Level {} {} ".format(self.name, self.race.name, self.level
                                                                        , self.ad_class.name))
        print("HP: {}/{}     MP: {}/{}".format(self.hp, self.max_hp, self.mp, self.max_mp))
        print("Experience:")
        self.print_experience_bar(self.total_exp, self.exp_to_next_lvl)
        print("\n")
        print("    Strength      Dexterity   Constitution  Intelligence     Wisdom       Charisma    ")     
        print("     ------        ------        ------        ------        ------        ------")
        print("     | {:2} |        | {:2} |        | {:2} |        | {:2} |        | {:2} |        | {:2} |".format(self.stats["str"]
                            , self.stats["dex"], self.stats["con"], self.stats["int"], self.stats["wis"], self.stats["cha"]))
        print("     ------        ------        ------        ------        ------        ------")
        print("      ({:2})          ({:2})          ({:2})          ({:2})          ({:2})          ({:2})".format(self.modifiers["str"]
                            , self.modifiers["dex"], self.modifiers["con"], self.modifiers["int"], self.modifiers["wis"], self.modifiers["cha"]))
        print("\n")
     


    def __repr__(self):
        return f"--- {self.name} ---\nRace: {self.race}  Class: {self.ad_class}\nHP: {self.hp}  MP: {self.mp}\n" \
               f"Stats: Str Dex Con Int Wis Cha\n        {self.stats}"
               
               
class AdClass:
    """
    class for character classes
    """
    
    def __init__(self, name="", hit_dice="d8", modifiers={"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}):
        self.name = name
        self.hit_dice = hit_dice
        self.modifiers = modifiers
        
    def __repr__(self):
        return f"{self.name}"
        
class Race:
    """
    class for character races
    """
    
    def __init__(self, name="", modifiers={"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}):
        self.name = name
        self.modifiers = modifiers
        
    def __repr__(self):
        return f"{self.name}"

class Enemy:
    """
    class for enemy objects
    """

    def __init__(self, name, ch_rating, drop_class, ac, hp, mp, stats, equipped):
        self.name = name
        self.ch_rating = ch_rating
        self.base_experience = ch_rating * 100
        self.drop_class = drop_class
        self.equipped = equipped
        self.has_adv = False
        self.ac = ac
        self.hp = hp
        self.mp = mp
        self.stats = stats
        self.modifiers = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}

    def attack(self, player):
        """
        the attack function for enemies

        Args:
            player (Adventurer): the player object

        Returns:
            Boolean: True if the enemy hits, False if the enemy misses
        """
        # checks if the enemy is alive
        if self.hp != 0:
            # checks if the enemy has advantage or not
            if self.has_adv:
                # checks if the enemy has a strength or dexterity based weapon
                if self.equipped["Weapon"].weapon_type == "versatile" or self.equipped["Weapon"].weapon_type == "two-handed" \
                    or self.equipped["Weapon"].weapon_type == "heavy":
                    hit_roll = max(dice_roll.roll(2, "d20")[0]) + self.modifiers["str"] + self.equipped["Weapon"].bonus
                    print("\n")
                    print(f"The {self.name} rolled a {hit_roll}!")
                    result = dice_roll.attack_roll(hit_roll, self, player)
                elif self.equipped["Weapon"].weapon_type == "finesse" or self.equipped["Weapon"].weapon_type ==\
                        "ranged" or self.equipped["Weapon"].weapon_type == "thrown":
                    hit_roll = max(dice_roll.roll(2, "d20")[0]) + self.modifiers["dex"] + self.equipped["Weapon"].bonus
                    print("\n")
                    print(f"The {self.name} rolled a {hit_roll}!")
                    result = dice_roll.attack_roll(hit_roll, self, player)
                else:
                    hit_roll = max(dice_roll.roll(2, "d20")[0]) + self.modifiers["str"] + self.equipped["Weapon"].bonus
                    print("\n")
                    print(f"The {self.name} rolled a {hit_roll}!")
                    result = dice_roll.attack_roll(hit_roll, self, player)
            elif not self.has_adv:
                if self.equipped["Weapon"].weapon_type == "versatile" or self.equipped["Weapon"].weapon_type == "two-handed" \
                    or self.equipped["Weapon"].weapon_type == "heavy":
                    hit_roll = max(dice_roll.roll(1, "d20")[0]) + self.modifiers["str"] + self.equipped["Weapon"].bonus
                    print("\n")
                    print(f"The {self.name} rolled a {hit_roll}!")
                    result = dice_roll.attack_roll(hit_roll, self, player)
                elif self.equipped["Weapon"].weapon_type == "finesse" or self.equipped["Weapon"].weapon_type ==\
                        "ranged" or self.equipped["Weapon"].weapon_type == "thrown":
                    hit_roll = dice_roll.roll(1, "d20")[1] + self.modifiers["dex"] + self.equipped["Weapon"].bonus
                    print("\n")
                    print(f"The {self.name} rolled a {hit_roll}!")
                    result = dice_roll.attack_roll(hit_roll, self, player)
                else:
                    hit_roll = dice_roll.roll(1, "d20")[1] + self.modifiers["str"] + self.equipped["Weapon"].bonus
                    print("\n")
                    print(f"The {self.name} rolled a {hit_roll}!")
                    result = dice_roll.enemy_attack_roll(hit_roll, self, player)
            return result
        
        
    def update_stats(self):
        """
        recalculates the stats of the enemy
        """
        if self.equipped["Armor"] != "Empty":
            self.ac = self.equipped["Armor"].ac + self.modifiers["dex"]
        self.max_hp = 15 + self.modifiers["con"]
        self.max_mp = 15 + self.modifiers["int"]
        self.hp = self.max_hp
        self.mp = self.max_mp

    def __repr__(self):
        return f"--- {self.name} ---\nChallenge Rating: {self.ch_rating}\nArmor Class: {self.ac}\nHP: {self.hp}  " \
               f"MP: {self.mp}"
               
class Boss(Enemy):
    """
    boss class

    Args:
        Enemy (Class): the parent class
    """
    
    def __init__(self, name, ch_rating, drop_class, ac, hp, mp, stats, equipped, special_attack):
        super().__init__(name, ch_rating, drop_class, ac, hp, mp, stats, equipped)
        self.special_attack = special_attack
        
    def __repr__(self):
        return super().__repr__() + f"\nSpecial Attack: {self.special_attack}"
                
        
class Spell():
    """
    the parent class for all spells
    """
    
    def __init__(self, name, level, dmg_type, dmg_dice, dmg_dice_num, mp_cost, num_targets):
        self.name = name
        self.level = level
        self.dmg_type = dmg_type
        self.dmg_dice = dmg_dice
        self.dmg_dice_num = dmg_dice_num
        self.mp_cost = mp_cost
        self.num_targets = num_targets
        
    def __repr__(self):
        return f"--- {self.name} ---\nLevel: {self.level}\nDamage Type: {self.dmg_type}\nDamage: {self.dmg_dice_num}" \
               f"{self.dmg_dice}\nMP Cost: {self.mp_cost}\nNumber of Targets: {self.num_targets}"
               
class Item:
    """
    the parent class for all items
    """

    def __init__(self, name="Empty", item_type="other", rarity="common", description=""):
        self.name = name
        self.item_type = ""
        self.rarity = ""
        self.description = ""

    def __repr__(self):
        return f"--- {self.name} ---\nType: {self.item_type}\nRarity: {self.rarity}\nDescription: {self.description}"
    
class Weapon(Item):
    """
    class for weapon items

    Args:
        Item (Class): the parent class
    """
    
    def __init__(self, name="Empty", item_type="weapon", rarity="common", description="", weapon_type="",
                 dmg_dice_num=1, damage_dice="", bonus=0):
        super().__init__(name, item_type, rarity, description)
        self.weapon_type = weapon_type
        self.dmg_dice_num = dmg_dice_num
        self.damage_dice = damage_dice
        self.bonus = bonus
        
    def __repr__(self):
        return super().__repr__() + f"\nWeapon Type: {self.weapon_type}\nDamage: {self.dmg_dice_num}{self.damage_dice}" \
                                     f"\nBonus: {self.bonus}"

class Armor(Item):
    """
    class for armor items

    Args:
        Item (Class): the parent class
    """
    
    def __init__(self, name="Empty", item_type="armor", rarity="common", description="", ac=0, bonus=0):
        super().__init__(name, item_type, rarity, description)
        self.ac = ac
        self.bonus = bonus
        
    def __repr__(self):
        return super().__repr__() + f"\nArmor Class: {self.ac}\nBonus: {self.bonus}"
        
class Consumable(Item):
    """
    class for consumable items

    Args:
        Item (Class): the parent class
    """
    
    def __init__(self, name="Empty", item_type="consumable", rarity="common", description="", effect="",
                 effect_dice=()):
        super().__init__(name, item_type, rarity, description)
        self.effect = effect
        self.effect_dice = effect_dice
        
    def __repr__(self):
        return super().__repr__() + f"\nEffect: {self.effect}\nEffect Dice: {self.effect_dice}"

def set_ad_modifiers(ad):
    """
    generates the modifiers for the player based on their stats

    Args:
        target (Adventurer/Enemy): player or enemy object
    """
    stats = ad.stats.items()
    for stat in stats:
        if 6 <= stat[1] <= 7:
            ad.modifiers[stat[0]] = -2
        elif 8 <= stat[1] <= 9:
            ad.modifiers[stat[0]] = -1
        elif 12 <= stat[1] <= 13:
            ad.modifiers[stat[0]] = 1
        elif 14 <= stat[1] <= 15:
            ad.modifiers[stat[0]] = 2
        elif 16 <= stat[1] <= 17:
            ad.modifiers[stat[0]] = 3
        elif 18 <= stat[1]:
            ad.modifiers[stat[0]] = 4
            

def set_modifiers(targets):
    """
    generates the modifiers for the player based on their stats

    Args:
        target (Adventurer/Enemy): player or enemy object
    """
    for target in targets:
        stats = target.stats.items()
        for stat in stats:
            if 6 <= stat[1] <= 7:
                target.modifiers[stat[0]] = -2
            elif 8 <= stat[1] <= 9:
                target.modifiers[stat[0]] = -1
            elif 12 <= stat[1] <= 13:
                target.modifiers[stat[0]] = 1
            elif 14 <= stat[1] <= 15:
                target.modifiers[stat[0]] = 2
            elif 16 <= stat[1] <= 17:
                target.modifiers[stat[0]] = 3
            elif 18 <= stat[1]:
                target.modifiers[stat[0]] = 4


def create_character(ad, classes, races):
    """
    This function creates a character with a given name, race, and class.

    Parameters:
    ad (Adventurer): The adventurer object to modify.
    classes (list): A list of available classes.
    races (list): A list of available races.

    Returns:
    None
    """
    keep_character = False           # boolean to keep the character          
    
    # while loop to keep the character                  
    while not keep_character:                                                     
        print("\nWhat is your name Adventurer?\n")
        ad.name = input("")                       
        print(f"\nHello {ad.name}, what race are you?\n")                       
        print("--- Races ---") 
        for race in races:
            print(race.name)
        print("\n")
        
        # While loop to check if an available race has been chosen
        while ad.race.name == "":                                                         
            temp_race = input("")
            for race in races:
                if temp_race == race.name:
                    ad.race = race
                else:
                    continue
            if ad.race == "":
                print("That race does not exist! please choose another")
        print("\nWhat class are you?\n")
        print("--- Classes ---")
        for cl in classes:
            print(cl)
        print("\n")
        
        # While loop to check if an available class has been chosen
        while ad.ad_class.name == "":
            temp_class = input("")
            for av_class in classes:
                if temp_class == av_class.name:
                    ad.ad_class = av_class
                else:
                    continue
            if ad.ad_class == "":
                print("That class does not exist! please choose another")
                
        # Prints the character and asks if the user wants to keep it
        print("\nHere is your adventurer!\n")
        print(f"--- {ad.name} ---")
        print(f"Race: {ad.race}")
        print(f"Class: {ad.ad_class}")
        print("\nwould you like to keep this character and roll stats? (y/n)")

        # While loop to check if the user wants to keep the character
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
    """
    This function prints the main menu for the game.
    """
    print("****      Game Menu      ****")
    print("1. Check Character")
    print("2. Check Inventory")
    print("3. Enter Dungeon")
    print("4. Quit game")


def in_game_menu():
    """
    This function prints the in-game menu for the game.
    """
    print("****      Game Menu      ****")
    print("1. Check Character")
    print("2. Check Inventory")
    print("3  Pick up item")
    print("4. Next Room")
    print("5. Quit game")


def inventory_menu():
    """
    This function prints the inventory menu for the game.
    """
    print("****      Inventory Menu      ****")
    print("1. List inventory")
    print("2. Equip item")
    print("3. Go back")


def fight_menu():
    """
    This function prints the fight menu for the game.
    """
    print("****      Fight      ****")
    print("1. List inventory")
    print("2. Use item")
    print("3. attack")
    print("4. Run")


def reveal_room(room, ad):
    """
    Prints the room description and the enemies in the room.

    Args:
        room (RoomNode): the room object
        ad (Adventurer): the player object

    Returns:
        Boolean: True if the player dies, False if the player wins
    """
def fight(room, player):
    """ 
    This function runs the fight between the player and the enemies.

    Args:
        num_enemies (int): the number of enemies in the room
        enemy (Enemy): the enemy object
        player (Adventurer): the player object

    Returns:
        boolean: True if the player dies, False if the player wins
    """
    room_complete = False
    while not room_complete:             # while player is alive and there are enemies left
        player.has_attack = True
        for enemy in room.enemies:
            print("\n")
            print(f"{enemy.name}s health: {enemy.hp}")
        print("\n")
        print(f"Your health: {player.hp}")
        print("\n")
        fight_menu()
        fight_option = input("What would you like to do?")
        match int(fight_option):
            case 1:                        # list inventory
                player.check_inventory()
            case 2:                        # use item
                print("\n")
                player.check_inventory()
                use = input("Which item would you like to use?")
                for item in player.backpack["Consumables"]:
                    if item.name == use:
                        player.use_item(item)
                    else:
                        print("That item is not in your backpack!")
            case 3:                         # attack
                if room.num_enemies > 1:
                    print("\n")
                    print("Which enemy would you like to attack?")
                    for enemy in room.enemies:
                        print(f"{enemy.name}")
                    attacked_enemy = input("")
                    for i in range(0, room.num_enemies-1):
                        if room.enemies[i].name == attacked_enemy and player.has_attack:
                            player.attack(room.enemies[i])
                            player.has_attack = False
                            if room.enemies[i].hp <= 0: # checks if the enemy is dead
                                enemy_name = room.enemies[i].name
                                room.enemies.remove(room.enemies[i])
                                room.num_enemies -= 1
                                print("\n")
                                print(f"You killed the {enemy_name}!")
                                print("\n")
                                if room.num_enemies != 0:
                                    print("Next enemy's turn!")
                                    for enemy in room.enemies:
                                        enemy.attack(player)
                                        if player.hp <= 0:
                                            game_over()
                                    print_enemies_left(room)
                            else:
                                for enemy in room.enemies:
                                    enemy.attack(player)
                                    if player.hp <= 0:
                                        game_over()
                else:
                    player.attack(room.enemies[0])
                    player.has_attack = False
                    if room.enemies[0].hp <= 0: # checks if the enemy is dead
                        last_enemy = room.enemies[0]
                        room.enemies.remove(room.enemies[0])
                        room.num_enemies -= 1
                        print("\n")
                        print(f"You killed the {last_enemy.name}!")
                        print("\n")
                        print("time to move on!")
                        player_choice = in_game_menu()
                        while player_choice != 4 or player_choice != 5:
                            if player_choice == 1:
                                player.print_character_sheet()
                            elif player_choice == 2:
                                player.check_inventory()
                            elif player_choice == 3:
                                print("\n")
                                player.check_inventory()
                                use = input("Which item would you like to use?")
                                for item in player.backpack["Consumables"]:
                                    if item.name == use:
                                        player.use_item(item)
                                    else:
                                        print("That item is not in your backpack!")
                            elif player_choice == 4:
                                room_complete = True
                            elif player_choice == 5:
                                game_over()
                            else:
                                print("That is not an option!")
                                player_choice = in_game_menu()
                    else:
                        room.enemies[0].attack(player)
                        if player.hp <= 0:
                            game_over()
                            
                            
def game_over():
    """
    This function ends the game.
    """
    print("You died!")
    print("Game Over!")
    print("Would you like to play again? (y/n)")
    play_again = input("")
    if play_again == 'y' or play_again == 'Y':
        main()
    elif play_again == 'n' or play_again == 'N':
        print("Thanks for playing!")
        quit()
                            

def main():
    """
    This function runs the game.
    """
    choice = 0
    curr_char_alive = True
    
    """
    These lists create all of the items, weapons, armor, spells, and enemies in the game, also creating bonuses.
    """
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
        "BattleStaff": Weapon("Staff", "weapon", "rare", "A simple sword", "two-handed", 1, "d10", 0),
        "Quarterstaff": Weapon("Quarterstaff", "weapon", "common", "A simple sword", "simple", 1, "d6", 0),
        "Spear": Weapon("Spear", "weapon", "uncommon", "A simple sword", "versatile", 1, "d8", 0),
        "Bite": Weapon("Bite", "weapon", "common", "A simple sword", "simple", 1, "d4", 0),
        "Claws": Weapon("Claw", "weapon", "common", "A simple sword", "simple", 1, "d6", 0),
        "Fangs": Weapon("Fangs", "weapon", "common", "A simple sword", "simple", 1, "d6", 0),
        "Tail": Weapon("Tail", "weapon", "common", "A simple sword", "simple", 2, "d6", 0),
        "Eye Rays": Weapon("Eye Rays", "weapon", "common", "A simple sword", "simple", 3, "d6", 0),
        "Greatclub": Weapon("Greatclub", "weapon", "rare", "A simple sword", "simple", 2, "d8", 0),
        "Tentacles": Weapon("Tenacles", "weapon", "common", "A simple sword", "simple", 2, "d8", 0),
        "Staff of Chaos": Weapon("Staff of Chaos", "magic_weapon", "legendary", "A staff that is powered by chaos", "two-handed", 1, "d10", dice_roll.roll(1, "d6")[1]),
    }
    armor = {
        "Hide": Armor("Hide", "armor", "common", "A simple sword", 10, 0),
        "Leather": Armor("Leather", "armor", "common", "A simple sword", 11, 0),
        "Studded Leather": Armor("Studded Leather", "armor", "uncommon", "A simple sword", 12, 0),
        "Chainmail": Armor("Chainmail", "armor", "uncommon", "A simple sword", 13, 0),
        "Plate": Armor("Plate", "armor", "rare", "A simple sword", 15, 0),
        "Half-Plate": Armor("Half-Plate", "armor", "uncommon", "A simple sword", 14, 0),
        "Scale": Armor("Scale", "armor", "common", "A simple sword", 12, 0),
        "Ancient Armor": Armor("Ancient Armor", "magic_armor", "legendary", "Armor that is blessed by the gods", 15, dice_roll.roll(1, "d6")[1]),
        "Astral Armor": Armor("Astral Armor", "magic_armor", "legendary", "Armor that is blessed by the gods", 14, dice_roll.roll(1, "d6")[1])
    }
    loot = [
        Item("Gold", "other", "uncommon", "A small pile of gold"),
        Item("Silver", "other", "common", "A small pile of silver"),
        Item("Small bag of gems", "other", "rare", "A small bag of gems"),
        Item("Platinum bar", "other", "rare", "A platinum bar"),
        Item("Gold bar", "other", "rare", "A gold bar"),
        Item("Jeweled egg", "other", "rare", "A jeweled egg"),
        Weapon("Poisoned Dagger", "weapon", "rare", "A dagger with a poison tip", "simple", 1, "d4", dice_roll.roll(1, "d4")[1]),
        Armor("Armor of protection", "magic-armor", "rare", "magically fortified armor", 13, dice_roll.roll(1, "d4")[1]),
        Consumable("Potion of healing", "consumable", "common", "A potion that heals 1d4 health", "inc_health", ("d4", 1)),
        Consumable("Potion of mana", "consumable", "common", "A potion that restores 1d4 mana", "inc_mana", ("d4", 1)),
        Consumable("Potion of strength", "consumable", "common", "A potion that increases strength by 1d4", "inc_str", ("d4", 1)),
        Consumable("Potion of dexterity", "consumable", "common", "A potion that increases dexterity by 1d4", "inc_dex", ("d4", 1)),
        Consumable("Potion of resistance", "consumable", "common", "A potion that increases constitution by 1d4", "inc_con", ("d4", 1)),
    ]
    rare_loot = [
        Weapon("Sword of the Sun", "magic_weapon", "legendary", "A sword that glows with the power of the sun", "versatile", 1, "d8", dice_roll.roll(1, "d6")[1]),
        Weapon("Staff of Chaos", "magic_weapon", "legendary", "A staff that is powered by chaos", "two-handed", 1, "d10", dice_roll.roll(1, "d6")[1]),
        Weapon("Hammer of Vodr", "magic_weapon", "legendary", "A hammer powered by divine energy", "two-handed", 1, "d10", dice_roll.roll(1, "d6")[1]),
        Armor("Armor of the Gods", "magic_armor", "legendary", "Armor that is blessed by the gods", 16, dice_roll.roll(1, "d6")[1]),
        Consumable("Potion of the Gods", "consumable", "legendary", "A potion that increases all stats by 1d6", "inc_all", ("d6", 1)),
        Armor("Ancient Armor", "magic_armor", "legendary", "Armor that is blessed by the gods", 15, dice_roll.roll(1, "d6")[1]),
        Armor("Astral Armor", "magic_armor", "legendary", "Armor that is blessed by the gods", 14, dice_roll.roll(1, "d6")[1]),
    ]
    spells = [
        Spell("Fireball", 3, "fire", "d6", 8, 5, 5),
        Spell("Lightning Bolt", 3, "lightning", "d6", 8, 5, 3),
        Spell("Magic Missile", 1, "force", "d4", 3, 1, 3),
        Spell("Cure Wounds", 1, "healing", "d8", 1, 1, 1),
        Spell("Healing Word", 1, "healing", "d4", 1, 1, 1),
        Spell("Chill Touch", 1, "necrotic", "d8", 1, 1, 1),
        Spell("Ray of Frost", 1, "cold", "d8", 1, 1, 1),
        Spell("Acid Splash", 1, "acid", "d6", 1, 1, 2),
        Spell("Viscious Mockery", 1, "psychic", "d4", 1, 1, 1),
    ]
    enemies = {
        "goblin": Enemy("goblin", 1, "common", 12, 7, 0, {"str": 8, "dex": 14, "con": 10, "int": 10, "wis": 8, "cha": 8}, {"Weapon": weapons["Shortsword"], "Armor": armor["Hide"]}),
        "orc": Enemy("orc", 2, "common", 13, 15, 0, {"str": 16, "dex": 12, "con": 16, "int": 7, "wis": 11, "cha": 10}, {"Weapon": weapons["Mace"], "Armor": armor["Hide"]}),
        "kobold": Enemy("kobold", .25, "common", 12, 5, 0, {"str": 7, "dex": 15, "con": 9, "int": 8, "wis": 7, "cha": 8}, {"Weapon": weapons["Dagger"], "Armor": armor["Hide"]}),
        "bugbear": Enemy("bugbear", 3, "rare", 16, 27, 0, {"str": 15, "dex": 14, "con": 13, "int": 8, "wis": 11, "cha": 9}, {"Weapon": weapons["Battleaxe"], "Armor": armor["Hide"]}),
        "hobgoblin": Enemy("hobgoblin", 2, "rare", 18, 11, 0, {"str": 13, "dex": 12, "con": 12, "int": 10, "wis": 10, "cha": 9}, {"Weapon": weapons["Longsword"], "Armor": armor["Chainmail"]}),
        "sprite": Enemy("sprite", .25, "common", 15, 2, 0, {"str": 3, "dex": 18, "con": 10, "int": 14, "wis": 13, "cha": 11}, {"Weapon": weapons["Dagger"], "Armor": armor["Leather"]}),
        "giant rat": Enemy("giant rat", 1, "common", 12, 7, 0, {"str": 7, "dex": 15, "con": 11, "int": 2, "wis": 10, "cha": 4}, {"Weapon": weapons["Bite"], "Armor": armor["Hide"]}),
        "giant spider": Enemy("giant spider", 1, "common", 14, 11, 0, {"str": 14, "dex": 16, "con": 12, "int": 2, "wis": 11, "cha": 4}, {"Weapon": weapons["Bite"], "Armor": armor["Hide"]}),
        "giant wolf spider": Enemy("giant wolf spider", 1, "common", 13, 11, 0, {"str": 12, "dex": 16, "con": 13, "int": 3, "wis": 12, "cha": 6}, {"Weapon": weapons["Fangs"], "Armor": armor["Hide"]}),
        "dire wolf": Enemy("dire wolf", 2, "rare", 14, 37, 0, {"str": 17, "dex": 15, "con": 15, "int": 3, "wis": 12, "cha": 7}, {"Weapon": weapons["Claws"], "Armor": armor["Hide"]}),
        "driad": Enemy("driad", .5, "common", 11, 11, 0, {"str": 10, "dex": 14, "con": 10, "int": 12, "wis": 13, "cha": 14}, {"Weapon": weapons["Dagger"], "Armor": armor["Leather"]}),
    }
    bosses = {
        "goblin boss": Boss("goblin boss", 5, "common", 17, 21, 0, {"str": 14, "dex": 10, "con": 14, "int": 10, "wis": 8, "cha": 10}, {"Weapon": weapons["Shortsword"], "Armor": armor["Chainmail"]}, spells[0]), 
        "orc war chief": Boss("orc war chief", 4, "common", 16, 45, 0, {"str": 18, "dex": 12, "con": 16, "int": 7, "wis": 11, "cha": 10}, {"Weapon": weapons["Greatsword"], "Armor": armor["Plate"]}, spells[1]),
        "kobold king": Boss("kobold king", 1, "common", 13, 27, 0, {"str": 9, "dex": 15, "con": 9, "int": 8, "wis": 7, "cha": 8}, {"Weapon": weapons["Shortsword"], "Armor": armor["Leather"]}, spells[2]),
        "bugbear chief": Boss("bugbear chief", 6, "common", 16, 65, 0, {"str": 17, "dex": 14, "con": 13, "int": 8, "wis": 11, "cha": 9}, {"Weapon": weapons["Battleaxe"], "Armor": armor["Chainmail"]}, spells[3]),
        "hobgoblin warlord": Boss("hobgoblin warlord", 5, "common", 18, 45, 0, {"str": 15, "dex": 12, "con": 12, "int": 10, "wis": 10, "cha": 9}, {"Weapon": weapons["Longsword"], "Armor": armor["Plate"]}, spells[4]),
        "manticore": Boss("Manticore", 3, "common", 14, 68, 0, {"str": 17, "dex": 16, "con": 17, "int": 7, "wis": 12, "cha": 8}, {"Weapon": weapons["Tail"], "Armor": armor["Leather"]}, spells[5]),
        "ogre": Boss("Ogre", 2, "common", 11, 59, 0, {"str": 19, "dex": 8, "con": 16, "int": 5, "wis": 7, "cha": 7}, {"Weapon": weapons["Greatclub"], "Armor": armor["Hide"]}, spells[6]),
        "warlock": Boss("Warlock", 3, "common", 11, 59, 0, {"str": 8, "dex": 14, "con": 14, "int": 11, "wis": 12, "cha": 16}, {"Weapon": weapons["BattleStaff"], "Armor": armor["Leather"]}, spells[7]),
        "beholder": Boss("Beholder", 9, "common", 18, 180, 0, {"str": 10, "dex": 14, "con": 18, "int": 17, "wis": 15, "cha": 17}, {"Weapon": weapons["Eye Rays"], "Armor": armor["Plate"]}, spells[8]),
        "lich": Boss("Lich", 11, "common", 17, 135, 0, {"str": 11, "dex": 16, "con": 16, "int": 20, "wis": 14, "cha": 16}, {"Weapon": weapons["Staff of Chaos"], "Armor": armor["Ancient Armor"]}, spells[8]),
        "illithid": Boss("Illithid", 7, "common", 15, 71, 0, {"str": 11, "dex": 12, "con": 11, "int": 19, "wis": 17, "cha": 17}, {"Weapon": weapons["Tentacles"], "Armor": armor["Astral Armor"]}, spells[8]),
    }
    races = [
        Race("elf", {"str": 0, "dex": 2, "con": 0, "int": 0, "wis": 0, "cha": 0}),
        Race("dwarf", {"str": 0, "dex": 0, "con": 2, "int": 0, "wis": 0, "cha": 0}),
        Race("teifling", {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 2}),
        Race("halfling", {"str": 0, "dex": 2, "con": 0, "int": 0, "wis": 0, "cha": 0}),
        Race("goliath", {"str": 2, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}),
        Race("human", {"str": 1, "dex": 1, "con": 1, "int": 1, "wis": 1, "cha": 1}),
    ]
    classes = [
        AdClass("barbarian", "d12", {"str": 2, "dex": 0, "con": 2, "int": 0, "wis": 0, "cha": 0}),
        AdClass("rogue", "d8", {"str": 0, "dex": 2, "con": 0, "int": 0, "wis": 0, "cha": 0}),
        AdClass("ranger", "d10", {"str": 0, "dex": 2, "con": 0, "int": 0, "wis": 0, "cha": 0}),
        AdClass("paladin", "d10", {"str": 2, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 2}),
        AdClass("cleric", "d8", {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 2, "cha": 2}),
        AdClass("wizard", "d6", {"str": 0, "dex": 0, "con": 0, "int": 2, "wis": 0, "cha": 2}),
        AdClass("warlock", "d8", {"str": 0, "dex": 0, "con": 0, "int": 2, "wis": 0, "cha": 2}),
        AdClass("fighter", "d10", {"str": 2, "dex": 0, "con": 2, "int": 0, "wis": 0, "cha": 0}),
    ]
    
    # Sets the modifiers for all of the enemies and bosses
    set_modifiers(enemies.values())
    set_modifiers(bosses.values())
    
    for enemy in enemies.values():
        enemy.update_stats()
    for boss in bosses.values():
        boss.update_stats()
    
    # Creates the player object
    ad = Adventurer()

    # Prints the title screen
    custom_banner = Figlet(font='rozzo')
    print(custom_banner.renderText('Cloak\n   &\nDagger'))
    print("\n Hello and welcome to the world of DnD!")
    print("-----------------------------------------")

    # The main game loop
    while choice != "4":
        
        # Creates the character
        create_character(ad, classes, races)
        ad.set_starting_equip(weapons, armor)
        print("\nHere are your stats!")
        ad_stats = dice_roll.roll_stats()
        print(ad_stats)
        print("\n")
        ad.set_player_stats(ad_stats)
        set_ad_modifiers(ad)
        ad.update_stats()
        ad.print_character_sheet()
        print(f"Saving Throws: Str - {ad.modifiers['str']} Dex - {ad.modifiers['dex']} Con - {ad.modifiers['con']}")
        print(f"               Int - {ad.modifiers['int']} Wis - {ad.modifiers['wis']} Cha - {ad.modifiers['cha']}")
        print("\n")
        print("-----------------------------------------")
        print("\n")
        print("Now that you have your character, you can enter the dungeon!\n")
        
        # The in-game loop
        while choice != "4" and curr_char_alive:
            main_menu()
            print("\n")
            choice = input("Please make a selection\n")
            match int(choice):
                case 1:           # checks the character
                    print("\n")
                    print(ad)
                    print("\n")
                case 2:           # checks the inventory
                    print("\n")
                    inv_choice = 0
                    # The inventory loop
                    while inv_choice != "3":
                        inventory_menu()
                        inv_choice = input("\nplease make a selection\n")
                        match int(inv_choice):
                            case 1:           # lists the inventory
                                ad.check_inventory()
                            case 2:           # equips an item
                                done = False
                                while not done:
                                    print("\n")
                                    equip = input("Which item would you like to equip?\n")
                                    for item in ad.backpack["Weapons"]:
                                        if item.name != equip:
                                            continue
                                        ad.equip_weapon(item)
                                        done = True
                                    for item in ad.backpack["Armor"]:
                                        if item.name != equip:
                                            continue
                                        ad.equip_armor(item)
                                        done = True
                                    if not done:
                                        print("That item is not in your backpack!")
                case 3:            # enters the dungeon
                    
                    # Creates the dungeon
                    new_dungeon = dungeon.create_dungeon(ad.level, loot, rare_loot, enemies, bosses,
                                                         1)
                    # The dungeon loop
                    while not new_dungeon.is_empty():
                        game_over = reveal_room(new_dungeon, ad)
                        if game_over:
                            curr_char_alive = False
                            break
                        else:
                            new_dungeon.remove(new_dungeon.head)

    return


if __name__ == "__main__":
    main()
