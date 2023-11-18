import random
import dice_roll


class RoomNode:

    def __init__(self, val, num_enemies=1, enemies=None, loot=None, puzzles=None):
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

    def insert(self, val, num_enemies, enemies, loot, puzzles):
        new_node = RoomNode(val, num_enemies, enemies, loot, puzzles)
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


def create_dungeon(player_level, loot, rare_loot, puzzle_keys, enemies, bosses, num_rooms, puzzles):
    dungeon = LinkedList()
    dungeon.head = RoomNode("boss room", 1, bosses[random.randint(0, 3)], rare_loot[0])
    counter = num_rooms
    while counter > 0:
        room_roll = dice_roll.roll(1, "d4")
        match room_roll[0]:
            case 1:
                enemy_type = enemies[random.randint(0, 3)]
                while enemy_type.ch_rating - player_level > 2:
                    enemy_type = enemies[random.randint(0, 3)]
                dungeon.insert("Fight room", random.randint(1, 3), enemy_type, enemy_type.loot, None)
                counter -= 1
            case 2:
                dungeon.insert("Loot room", None, None, loot[random.randint(0, 1)], None)
                counter -= 1
            case 3:
                dungeon.insert("Puzzle room", None, None, puzzle_keys, puzzles)
                counter -= 1
            case 4:
                dungeon.insert("Empty room", None, None, None, None)
                counter -= 1
    return dungeon
