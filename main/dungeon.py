import random
import game_script
import dice_roll
import copy


class RoomNode:

    def __init__(self, val, num_enemies=0, enemies=[], loot=[]):
        self.val = val
        self.next = None
        self.num_enemies = num_enemies
        self.enemies = enemies
        self.loot = loot
        
    def get_data(self):
        return self.val

    def set_data(self, val):
        self.val = val

    def get_next(self):
        return self.next

    def set_next(self, nxt):
        self.next = nxt


class LinkedList:

    def __init__(self, head=None):
        self.head = head
        self.count = 0

    def insert(self, val, num_enemies, enemies, loot):
        new_node = RoomNode(val, num_enemies, enemies, loot)
        new_node.set_next(self.head)
        self.head = new_node
        self.count += 1

    def find(self, val):
        item = self.head
        while item is not None:
            if item.get_data() == val:
                return item
            else:
                item = item.get_next()
        return None

    def remove(self, item):
        curr = item
        nxt = None
        if curr is None:
            return
        else:
            nxt = curr.get_next()
            self.head = nxt
            curr = self.head
            nxt = curr.get_next()
            curr.set_next(nxt)
            self.count -= 1

    def get_count(self):
        return self.count

    def is_empty(self):
        return self.head is None
    
def get_enemy_loot(enemy, loot, rare_loot):
    """
    this function returns a list of loot that the enemy drops

    Args:
        enemy (Enemy): the enemy that is dropping loot
        loot (List): a list of loot that can be found in the dungeon
        rare_loot (List): a list of rare loot that can be found in the dungeon

    Returns:
        List: a list of loot that the enemy drops
    """
    if enemy.drop_class == "common":
        enemy_loot = [loot[random.randint(0, len(loot)-1)]]
    elif enemy.drop_class == "rare":
        drop_chance = random.randint(1, 100)
        if drop_chance <= 10:
            enemy_loot = [rare_loot[random.randint(0, len(rare_loot)-1)]]
        else:
            enemy_loot = [loot[random.randint(0, len(loot)-1)]]
    new_loot = copy.deepcopy(enemy_loot)
    return new_loot

def get_loot(player, loot, rare_loot):
    """
    this function returns a list of loot that the player finds in a loot room

    Args:
        player (Player): the player that is finding loot
        loot (List): a list of loot that can be found in the dungeon
        rare_loot (List): a list of rare loot that can be found in the dungeon

    Returns:
        List: a list of loot that the player finds
    """
    loot_found = []
    loot_roll = dice_roll.roll(1, "d100")[1]
    if loot_roll <= 10:
        new_loot = copy.deepcopy(rare_loot[random.randint(0, len(rare_loot)-1)])
        loot_found.append(new_loot)
    else:
        new_loot = copy.deepcopy(loot[random.randint(0, len(loot)-1)])
        loot_found.append(new_loot)
    return loot_found


def create_dungeon(player, loot, rare_loot, enemies, bosses, num_rooms):
    """
    this function creates a dungeon based on the player's level and the a predetermined list of enemies, loot, and bosses

    Args:
        player_level (int): the level of the player
        loot (List): a list of loot that can be found in the dungeon
        rare_loot (List): a list of rare loot that can be found in the dungeon
        enemies (List): a list of enemies that can be found in the dungeon
        bosses (List): a list of bosses that can be found in the dungeon
        num_rooms (int): the number of rooms in the dungeon

    Returns:
        LinkedList: a linked list of rooms that make up the dungeon, with the head being the boss room
    """
    dungeon = LinkedList()
    lvl_bosses = []
    for boss in bosses.values():
        if boss.ch_rating > player.level + 2:
            continue
        else:
            new_boss = copy.deepcopy(boss)
            lvl_bosses.append(new_boss)
            
    dungeon.head = RoomNode("boss room", 1, lvl_bosses[random.randint(0, len(lvl_bosses)-1)], rare_loot[random.randint(0, len(rare_loot)-1)])
    counter = num_rooms
    while counter > 0:
        room_roll = dice_roll.roll(1, "d4")
        room_roll = 1
        match room_roll:
            case 1:
                # set up values for the while loop
                room_filled = False
                lvl_enemies = []
                scaled_enemies = []
                enemy_loot = []
                num_enemies = random.randint(1, 3)    # number of enemies in the room
                
                # create a list of enemies that are within 1 challenge rating of the player or less
                for enemy in enemies.values():
                    if enemy.ch_rating > player.level + 1:
                        continue
                    else:
                        new_enemy = copy.deepcopy(enemy)
                        lvl_enemies.append(new_enemy)
                        
                # create a list of enemies that are within 1 challenge rating of the player or less, scaled to the number of enemies in the room
                for enemy in enemies.values():
                    if enemy.ch_rating * num_enemies > player.level + 1:
                        continue
                    else:
                        new_enemy = copy.deepcopy(enemy)
                        scaled_enemies.append(new_enemy)

                # while loop to fill the room with enemies
                while room_filled == False:
                    enemy_type = []
                    # if there is only one enemy in the room, choose a random enemy from the list
                    if num_enemies == 1:
                        enemy_type = [lvl_enemies[random.randint(0, len(lvl_enemies)-1)]]  # choose a random enemy from the list
                        enemy_loot.append(get_enemy_loot(enemy_type[0], loot, rare_loot))
                        dungeon.insert("Fight room", num_enemies, enemy_type, enemy_loot)
                        room_filled = True
                        counter -= 1
                    # if there are more than one enemy in the room, choose a random number of enemy types from the list
                    else:
                        enemy_types = random.randint(1, num_enemies)
                        if enemy_types == 1:
                            enemy_to_add = scaled_enemies[random.randint(0, len(scaled_enemies)-1)]
                            for i in range(num_enemies):
                                new_enemy = copy.deepcopy(enemy_to_add)
                                enemy_type.append(new_enemy)  # choose a random enemy from the list
                                enemy_loot.append(get_enemy_loot(enemy_to_add, loot, rare_loot))
                            dungeon.insert("Fight room", num_enemies, enemy_type, enemy_loot)
                            room_filled = True
                            counter -= 1
                        else:
                            enemies_to_add = []
                            enemy_types_to_add = []
                            for i in range(enemy_types):
                                enemy_types_to_add.append(scaled_enemies[random.randint(0, len(scaled_enemies)-1)])
                            while len(enemies_to_add) < num_enemies:
                                for enemy_type in enemy_types_to_add:
                                    new_enemy = copy.deepcopy(enemy_type)
                                    enemies_to_add.append(new_enemy)
                                if len(enemies_to_add) != num_enemies:
                                    duplicates = num_enemies - len(enemies_to_add)
                                    for i in range(duplicates):
                                        new_enemy = copy.deepcopy(enemy_types_to_add[random.randint(0, len(enemy_types_to_add)-1)])
                                        enemies_to_add.append(new_enemy)
                            for enemy in enemies_to_add:
                                enemy_loot.append(get_enemy_loot(enemy, loot, rare_loot))
                            dungeon.insert("Fight room", num_enemies, enemy_types_to_add, enemy_loot)
                            room_filled = True
                            counter -= 1
            case 2:
                dungeon.insert("Loot room", 0, [], get_loot(player, loot, rare_loot))     
                counter -= 1
            case 3:
                dungeon.insert("Rest room", 0, [], [])
                counter -= 1
            case 4:
                dungeon.insert("Empty room", 0, [], [])
                counter -= 1
    return dungeon
