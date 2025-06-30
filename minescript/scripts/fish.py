import minescript
import random
import time

# multiple fishing positions to avoid detection
fishingPositions = [
    (3, 56, -12),
    (2, 56, -7),
    (-1, 56, -5)
]

def look_at_position(pos):
    x, y, z = pos
    minescript.player_look_at(x, y, z)
    time.sleep(0.02)  # allow time for the player to turn

def cast_rod():
    minescript.player_press_use(True)
    time.sleep(0.05)
    minescript.player_press_use(False)

def get_fishing_bobber():
    entities = minescript.get_entities()
    for entity in entities:
        # Print all entities for debugging
        minescript.echo(str(entity))
        if getattr(entity, "name", "") == "Fishing Bobber" or getattr(entity, "type", "") == "entity.minecraft.fishing_bobber":
            return entity
    return None

def wait_for_fish(bobber):
    last_y = getattr(bobber, "position", [None, None, None])[1]
    while True:
        entities = minescript.get_entities()
        for entity in entities:
            if getattr(entity, "type", "") == "entity.minecraft.fishing_bobber":
                pos = getattr(entity, "position", [None, None, None])
                y = pos[1] if pos and len(pos) > 1 else None
                minescript.echo(f"Bobber y: {y}")
                if last_y is not None and y is not None:
                    # Detect sudden drop in y (splash)
                    if y < last_y - 0.3:
                        minescript.echo("Fish detected! Reel in!")
                        return
                last_y = y
        time.sleep(0.1)

def main():
    while True:
        pos = random.choice(fishingPositions)
        look_at_position(pos)
        cast_rod()
        time.sleep(1)  # Give time for bobber to spawn
        bobber = get_fishing_bobber()
        if bobber:
            wait_for_fish(bobber)
        else:
            minescript.echo("No fishing bobber found!")
            time.sleep(2)
        cast_rod()
        time.sleep(0.1)

if __name__ == "__main__":
    main()
