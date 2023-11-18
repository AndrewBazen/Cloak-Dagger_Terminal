import random


def roll(num_dice, dice_type):
    rolls = []
    match dice_type:
        case "d20":
            counter = num_dice
            dice_total = 0
            while counter > 0:
                rand = random.randint(1, 20)
                rolls.append(rand)
                dice_total += rand
                counter = counter - 1
            return rolls, dice_total
        case "d12":
            counter = num_dice
            dice_total = 0
            while counter > 0:
                rand = random.randint(1, 12)
                rolls.append(rand)
                dice_total += rand
                counter = counter - 1
            return rolls, dice_total
        case "d10":
            counter = num_dice
            dice_total = 0
            while counter > 0:
                rand = random.randint(1, 10)
                rolls.append(rand)
                dice_total += rand
                counter = counter - 1
            return rolls, dice_total
        case "d8":
            counter = num_dice
            dice_total = 0
            while counter > 0:
                rand = random.randint(1, 8)
                rolls.append(rand)
                dice_total += rand
                counter = counter - 1
            return rolls, dice_total
        case "d6":
            counter = num_dice
            dice_total = 0
            while counter > 0:
                rand = random.randint(1, 6)
                rolls.append(rand)
                dice_total += rand
                counter = counter - 1
            return rolls, dice_total
        case "d4":
            counter = num_dice
            dice_total = 0
            while counter > 0:
                rand = random.randint(1, 4)
                rolls.append(rand)
                dice_total += rand
                counter = counter - 1
            return rolls, dice_total


def roll_stats():
    stats = []
    while len(stats) < 6:
        total = 0
        result = roll(4, "d6")[0]
        result.remove(min(result))
        for num in result:
            total += num
        stats.append(total)
    return stats


def attack_roll(hit_roll, player, enemy):
    if hit_roll == 20:
        print("That's a CRITICAL HIT!!")
        dmg = roll(int(player.equipped["Weapon"].dmg_dice_num), player.equipped["Weapon"].dmg_dice)
        damage = dmg[1] * 2
        if enemy.hp > damage:
            enemy.hp -= damage
            print("\n")
            print(f"You dealt {damage} critical damage!")
        else:
            print("\n")
            print(f"You decimated the {enemy.name}!")
    elif hit_roll >= enemy.ac:
        dmg = roll(int(player.equipped["Weapon"].dmg_dice_num), player.equipped["Weapon"].dmg_dice)
        damage = dmg[1]
        if enemy.hp > damage:
            enemy.hp -= damage
            print("\n")
            print(f"You dealt {damage} damage!")
        else:
            print("\n")
            print(f"You defeated the {enemy.name}!")
    else:
        print("\n")
        print("Your attack missed!")


def enemy_attack_roll(hit_roll, enemy, player):
    result = False
    if hit_roll == 20:
        print("That's a CRITICAL HIT!!")
        dmg = roll(enemy.dmg_dice_num, enemy.dmg_dice)
        damage = dmg[1] * 2
        if player.hp > damage:
            player.hp -= damage
            print("\n")
            print(f"The {enemy.name} dealt {damage} critical damage!")
        else:
            print("\n")
            print(f"You were decimated by the {enemy.name}!")
            result = True
    elif hit_roll >= player.ac:
        dmg = roll(enemy.dmg_dice_num, enemy.dmg_dice)
        damage = dmg[1]
        if player.hp > damage:
            player.hp -= damage
            print("\n")
            print(f"The {enemy.name} dealt {damage} damage!")
        else:
            print("\n")
            print(f"You were defeated by the {enemy.name}!")
            result = True
    else:
        print("\n")
        print(f"The {enemy.name}'s attack missed!")
    return result
