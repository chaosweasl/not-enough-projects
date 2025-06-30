import minescript
import time
import re

# Minecraft pickaxes and their max durability
PICKAXE_DURABILITY = {
    "minecraft:wooden_pickaxe": 59,
    "minecraft:stone_pickaxe": 131,
    "minecraft:iron_pickaxe": 250,
    "minecraft:golden_pickaxe": 32,
    "minecraft:diamond_pickaxe": 1561,
    "minecraft:netherite_pickaxe": 2031,
}

def mine(value: bool):
    minescript.player_press_attack(value)

def get_main_hand_item():
    hands = minescript.player_hand_items()
    return hands.main_hand if hasattr(hands, "main_hand") else None

def get_damage_from_nbt(nbt_str):
    match = re.search(r'"minecraft:damage":(\d+)', nbt_str)
    if match:
        return int(match.group(1))
    return 0  # Assume undamaged if not found

def check_durability(main_hand):
    if main_hand and main_hand.item:
        item_id = main_hand.item
        nbt = getattr(main_hand, "nbt", "")
        damage = get_damage_from_nbt(nbt)
        durability = PICKAXE_DURABILITY.get(item_id)
        if durability is not None:
            if damage > durability - 5:
                minescript.echo(f"Warning: Your {item_id} is about to break! ({damage}/{durability})")
                return False
            else:
                # minescript.echo(f"You are holding: {item_id} ({damage}/{durability})")
                return True
        else:
            return True
    else:
        minescript.echo("You are not holding any item in your main hand.")
        return False

# this function exists to avoid AFK detection 
def move_a_little():
    minescript.player_press_left(True)
    time.sleep(1)
    minescript.player_press_left(False)
    minescript.player_press_right(True)
    time.sleep(1)
    minescript.player_press_right(False)

def main():
    mine(True)
    move_timer = 0
    try:
        while True:
            main_hand = get_main_hand_item()
            if not check_durability(main_hand):
                mine(False)
                break

            time.sleep(1)
            move_timer += 1
            if move_timer >= 60:
                move_a_little()
                move_timer = 0
    except KeyboardInterrupt:
        mine(False)
        minescript.echo("Mining stopped by user.")

# Required to run the script
if __name__ == "__main__":
    main()
