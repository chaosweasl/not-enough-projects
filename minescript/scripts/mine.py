# Filename: print_hand.py
import minescript

# Minecraft pickaxes and their max durability
PICKAXE_DURABILITY = {
    "minecraft:wooden_pickaxe": 59,
    "minecraft:stone_pickaxe": 131,
    "minecraft:iron_pickaxe": 250,
    "minecraft:golden_pickaxe": 32,
    "minecraft:diamond_pickaxe": 1561,
    "minecraft:netherite_pickaxe": 2031,
}

def main():
    # Get the items in the player's hands (main hand and off hand)
    hands = minescript.player_hand_items()
    main_hand = hands.main_hand  # This is an ItemStack object

    # Print out the item the player is holding in their main hand
    if main_hand and main_hand.item:
        item_id = main_hand.item
        damage = getattr(main_hand, "damage", None)
        durability = PICKAXE_DURABILITY.get(item_id)
        if durability is not None and damage is not None:
            if damage > durability - 5:
                minescript.echo(f"Warning: Your {item_id} is about to break! ({damage}/{durability})")
            else:
                minescript.echo(f"You are holding: {item_id} ({damage}/{durability})")
        else:
            minescript.echo(f"You are holding: {main_hand}")
    else:
        minescript.echo("You are not holding any item in your main hand.")

# Required to run the script
if __name__ == "__main__":
    main()
