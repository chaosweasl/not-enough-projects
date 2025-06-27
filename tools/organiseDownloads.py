# hi i made this as a script that organises my files based on their extensions

import os
import shutil
import time

downloadPath = r"C:\Users\virtu\Downloads"
sortedPath = r"D:\900_SORTED_DOWNLOADS"  # Destination for sorted files

folders = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Documents': ['.pdf', '.docx', '.txt'],
    'Music': ['.mp3', '.wav'],
    'Videos': ['.mp4', '.mov'],
    'Other': ['.zip'],
    # Add more as needed
}

while True:
    for filename in os.listdir(downloadPath):
        file_path = os.path.join(downloadPath, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            moved = False
            for folder, extensions in folders.items():
                if ext in extensions:
                    dest_folder = os.path.join(sortedPath, folder)
                    os.makedirs(dest_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(dest_folder, filename))
                    moved = True
                    break
            if not moved:
                other_folder = os.path.join(sortedPath, 'Other')
                os.makedirs(other_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(other_folder, filename))
    time.sleep(3600)  # Wait an hour before checking again