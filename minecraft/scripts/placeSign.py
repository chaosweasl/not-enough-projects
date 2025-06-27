# this script uses the minescript mod to place a random sign where the player is standing and place random text 

from minescript import (echo, execute, getblock, player)
import sys, urllib.request, json, random

MAX_LINE_LENGTH = 15
MAX_LINES = 4

def split_text_to_lines(text):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # If word is longer than max length, split it directly
        if len(word) > MAX_LINE_LENGTH:
            # Flush current line if not empty
            if current_line:
                lines.append(current_line)
                current_line = ""
            # Split long word into chunks of MAX_LINE_LENGTH
            for i in range(0, len(word), MAX_LINE_LENGTH):
                lines.append(word[i:i+MAX_LINE_LENGTH])
        else:
            # Check if adding the word exceeds the line length
            if len(current_line) + len(word) + (1 if current_line else 0) <= MAX_LINE_LENGTH:
                # Add space if line not empty
                current_line += (' ' if current_line else '') + word
            else:
                # Line full, push it and start new line
                lines.append(current_line)
                current_line = word

    # Add last line if not empty
    if current_line:
        lines.append(current_line)

    # Limit to MAX_LINES
    lines = lines[:MAX_LINES]

    # Fill remaining lines with empty strings if less than MAX_LINES
    while len(lines) < MAX_LINES:
        lines.append("")

    return lines

def get_public_ipv4():
    return urllib.request.urlopen('https://v4.ident.me/').read().decode('utf-8')

text = [
   get_public_ipv4(),
   "poop",
   "I'm watching you.",
   "Turn around",
   "null.error",
   "10"
]

sign_text = random.choice(text)

# Get the player's position, rounded to the nearest integer:
x, y, z = [round(p) for p in player().position]

# Get the type of block directly beneath the player:
block_type = getblock(x, y - 1, z)
block_type = block_type.replace("minecraft:", "").split("[")[0]

rotation = 0

execute(f"/setblock {x} {y} {z} minecraft:birch_sign[rotation={rotation}]")

# Split sign_text into lines with max length 15:
lines = split_text_to_lines(sign_text)

# Prepare JSON for sign text properly using json.dumps:
json_data = {
    "front_text": {
        "messages": [{"text": line} for line in lines]
    }
}

json_str = json.dumps(json_data)

execute(f"/data merge block {x} {y} {z} {json_str}")
