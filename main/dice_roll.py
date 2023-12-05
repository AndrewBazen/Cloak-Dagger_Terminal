import random
import time
import sys


def slow_print(text, delay=0.1, end='\n', flush=True):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    if flush:
        sys.stdout.flush()


def loading_animation(string, duration=3, delay=0.1):
    animation_chars = ['|', '/', '-', '\\']

    start_time = time.time()
    while time.time() - start_time < duration:
        for char in animation_chars:
            sys.stdout.write('\r' + string + char)
            sys.stdout.flush()
            time.sleep(delay)
            

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


def roll_terminal(num_dice, dice_type):
    rolls = []
    match dice_type:
        case "d20":
            counter = num_dice
            dice_total = 0
            # Print loading text
            roll_text = f"Rolling {num_dice}{dice_type}..."
            slow_print(roll_text, end='', flush=False)
            loading_animation(roll_text)
            print("\n")
            while counter > 0:
                # Print the result of the roll
                rand = random.randint(1, 6)
                slow_print(f"{rand}")
                time.sleep(0.5)
                
                rolls.append(rand)
                dice_total += rand
                counter = counter - 1
            return rolls, dice_total
        case "d12":
            counter = num_dice
            dice_total = 0
            # Print loading text
            roll_text = f"Rolling {num_dice}{dice_type}..."
            slow_print(roll_text, end='', flush=False)
            loading_animation(roll_text)
            print("\n")
            while counter > 0:
                # Print the result of the roll
                rand = random.randint(1, 6)
                slow_print(f"{rand}")
                time.sleep(0.5)
                    
                rolls.append(rand)
                dice_total += rand
                counter = counter - 1
            return rolls, dice_total
        case "d10":
            counter = num_dice
            dice_total = 0
            # Print loading text
            roll_text = f"Rolling {num_dice}{dice_type}..."
            slow_print(roll_text, end='', flush=False)
            loading_animation(roll_text)
            print("\n")
            while counter > 0:
                # Print the result of the roll
                rand = random.randint(1, 6)
                slow_print(f"{rand}")
                time.sleep(0.5)

                rolls.append(rand)
                dice_total += rand
                counter = counter - 1
            return rolls, dice_total
        case "d8":
            counter = num_dice
            dice_total = 0
            # Print loading text
            roll_text = f"Rolling {num_dice}{dice_type}..."
            slow_print(roll_text, end='', flush=False)
            loading_animation(roll_text)
            print("\n")
            while counter > 0:
                # Print the result of the roll
                rand = random.randint(1, 6)
                slow_print(f"{rand}")
                time.sleep(0.5)

                rolls.append(rand)
                dice_total += rand
                counter = counter - 1
            return rolls, dice_total
        case "d6":
            counter = num_dice
            dice_total = 0
            # Print loading text
            roll_text = f"Rolling {num_dice}{dice_type}..."
            slow_print(roll_text, end='', flush=False)
            loading_animation(roll_text)
            print("\n")
            while counter > 0:
                rand = random.randint(1, 6)
                slow_print(f"{rand}")
                time.sleep(0.5)
                    
                rolls.append(rand)
                dice_total += rand
                counter = counter - 1
            return rolls, dice_total
        case "d4":
            counter = num_dice
            dice_total = 0
            # Print loading text
            roll_text = f"Rolling {num_dice}{dice_type}..."
            slow_print(roll_text, end='', flush=False)
            loading_animation(roll_text)
            print("\n")
            while counter > 0:
                # Print the result of the roll
                rand = random.randint(1, 6)
                slow_print(f"{rand}")
                time.sleep(0.5)

                rolls.append(rand)
                dice_total += rand
                counter = counter - 1
            return rolls, dice_total


def roll_stats():
    stats = []
    while len(stats) < 6:
        total = 0
        result = roll_terminal(4, "d6")[0]
        result.remove(min(result))
        for num in result:
            total += num
        slow_print(f"\nStat {len(stats)} Total: {total}")
        stats.append(total)
    return stats


def attack_roll(hit_roll, hit_roll_mod, player, enemy):
    hit = False
    if hit_roll == 20 and hit_roll_mod >= enemy.ac:
        hit = True
        print("That's a CRITICAL HIT!!")
        dmg = roll(player.equipped["Weapon"].dmg_dice_num, player.equipped["Weapon"].damage_dice)
        damage = dmg[1] * 2
        if enemy.hp > damage:
            enemy.hp -= damage
            print("\n")
            print(f"You dealt {damage} critical damage!")
        else:
            enemy.hp -= damage
            print("\n")
            print(f"You decimated the {enemy.name}!")
    elif hit_roll != 20 and hit_roll_mod >= enemy.ac:
        hit = True
        dmg = roll(player.equipped["Weapon"].dmg_dice_num, player.equipped["Weapon"].damage_dice)
        damage = dmg[1]
        if enemy.hp > damage:
            enemy.hp -= damage
            print("\n")
            print(f"You dealt {damage} damage!")
        else:
            enemy.hp -= damage
            print("\n")
            print(f"You defeated the {enemy.name}!")
    else:
        print("\n")
        print("Your attack missed!")
    return hit


def enemy_attack_roll(hit_roll, hit_roll_mod, enemy, player):
    result = False
    if hit_roll == 20 and hit_roll_mod >= enemy.ac:
        print("That's a CRITICAL HIT!!")
        dmg = roll(enemy.equipped["Weapon"].dmg_dice_num, enemy.equipped["Weapon"].damage_dice)
        damage = dmg[1] * 2
        if player.hp > damage:
            player.hp -= damage
            print("\n")
            print(f"The {enemy.name} dealt {damage} critical damage!")
        else:
            player.hp -= damage
            print("\n")
            print(f"You were decimated by the {enemy.name}!")
            result = True
    elif hit_roll != 20 and hit_roll_mod >= enemy.ac:
        dmg = roll(enemy.equipped["Weapon"].dmg_dice_num, enemy.equipped["Weapon"].damage_dice)
        damage = dmg[1]
        if player.hp > damage:
            player.hp -= damage
            print("\n")
            print(f"The {enemy.name} dealt {damage} damage!")
        else:
            player.hp -= damage
            print("\n")
            print(f"You were defeated by the {enemy.name}!")
            result = True
    else:
        print("\n")
        print(f"The {enemy.name}'s attack missed!")
    return result
