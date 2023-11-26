import random
import dice_roll


class RoomNode:

    def __init__(self, val, num_enemies=1, enemies=[], loot=None, puzzles=None):
        self.val = val
        self.next = None
        self.num_enemies = num_enemies
        self.enemies = enemies
        self.puzzles = puzzles
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
    return enemy_loot


def create_dungeon(player_level, loot, rare_loot, enemies, bosses, num_rooms):
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
    dungeon.head = RoomNode("boss room", random.randint(1,), bosses[random.randint(0, 3)], rare_loot[0])
    counter = num_rooms
    while counter > 0:
        # room_roll = dice_roll.roll(1, "d4")
        room_roll = 1
        match room_roll[0]:
            case 1:
                # set up values for the while loop
                room_filled = False
                lvl_enemies = []
                scaled_enemies = []
                enemy_loot = []
                num_enemies = random.randint(1, 3)    # number of enemies in the room
                
                # create a list of enemies that are within 1 challenge rating of the player or less
                for enemy in enemies:
                    if enemy.ch_rating > player_level + 1:
                        continue
                    else:
                        lvl_enemies.append(enemy)
                        
                # create a list of enemies that are within 1 challenge rating of the player or less, scaled to the number of enemies in the room
                for enemy in enemies:
                    if enemy.ch_rating * num_enemies > player_level + 1:
                        continue
                    else:
                        scaled_enemies.append(enemy)

                # while loop to fill the room with enemies
                while room_filled == False:
                    
                    # if there is only one enemy in the room, choose a random enemy from the list
                    if num_enemies == 1:
                        enemy_loot.append(get_enemy_loot(enemy_type[0], loot, rare_loot))
                        room_filled = True
                        counter -= 1
                    # if there are more than one enemy in the room, choose a random number of enemy types from the list
                    else:
                        enemy_types = random.randint(1, num_enemies)
                        if enemy_types == 1:
                                enemy_loot.append(get_enemy_loot(enemy_to_add, loot, rare_loot))
                            room_filled = True
                            counter -= 1
                        else:
                            enemy_types_to_add = []
                            enemies_added = 0
                            duplicates = 0
                            while enemy_types_to_add.count() < num_enemies:
                                if scaled_enemies.count() < num_enemies:
                                    duplicates = num_enemies - scaled_enemies.count()
                                
                                enemy_type = scaled_enemies[random.randint(0, len(scaled_enemies))]
                                if enemy_type in enemy_types_to_add:
                                    continue
                                enemy_types_to_add.append(enemy_type)
                                enemy_loot.append(get_enemy_loot(enemy_type, loot, rare_loot))
                            room_filled = True
            case 2:
                dungeon.insert("Loot room", None, None, loot[random.randint(0, 1)], None)
                counter -= 1
            case 3:
                dungeon.insert("Rest room", None, None, None, None)
                counter -= 1
            case 4:
                dungeon.insert("Empty room", None, None, None, None)
                counter -= 1
    return dungeon
