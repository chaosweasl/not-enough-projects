import minescript
import time

"""
a mining script

MAIN:
- start by making the player hold down left click
- while true, make the script check durability
- if the left click is interrupted, make the script stop and execute \killjob 1
- else, continue forever

CHECK DURABILITY: 
- n = 0 (or 1, idk which is the first item in the tool slot)
- if the tool that the player is holding suddenly becomes an empty hand, switch to (n+1) slot
- stop the script if the current item breaks and n+1 is an empty hand
- also stop the script after the current item breaks and n+1 is 8 (or 9) (the last one is a compass for navigation, not a tool)
"""

def main():
    # Start mining by holding down left click
    minescript.player_press_attack(True)
    try:
        current_slot = 0  # Hotbar slots: 0-8
        while True:
            # Check if left click is still held (simulate interruption detection)
            # (No direct API for this, so we assume script control)
            hand_items = minescript.player_hand_items()
            main_hand = hand_items.main_hand
            if main_hand is None or main_hand.item != "minecraft:stone_pickaxe":
                # Tool broke or empty hand, try next slot
                current_slot += 1
                if current_slot >= 8:  # Slot 8 is last tool slot (slot 9 is compass)
                    minescript.echo("No more tools, stopping script.")
                    break
                minescript.player_inventory_select_slot(current_slot)
                time.sleep(0.2)  # Wait for slot switch
                # Check if new slot is also empty
                hand_items = minescript.player_hand_items()
                main_hand = hand_items.main_hand
                if main_hand is None or main_hand.item == "minecraft:air":
                    minescript.echo("No tool in next slot, stopping script.")
                    break
            time.sleep(0.1)  # Polling interval
    finally:
        # Always release left click before stopping the script
        minescript.player_press_attack(False)
        time.sleep(0.1)  # Ensure the key release is registered
        minescript.execute("\\killjob 1")

if __name__ == "__main__":
    main()
