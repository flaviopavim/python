# This code moves files to another folder
# Use it to organize your files and folders

import os
import shutil

SOURCE_FOLDER = r"D:\Pictures"
DESTINATION_FOLDER = r"D:\Videos"

EXTENSIONS = {
    ".mp4",
    #".mkv",
    ".avi",
    ".mov",
    ".wmv",
    #".flv",
    #".webm",
    #".m4v",
    ".mpeg",
    ".mpg",
    ".3gp",
    #".ts",
    #".mts",
    #".m2ts"
}


def move_videos():
    moved = 0

    for root, _, files in os.walk(SOURCE_FOLDER):
        for filename in files:
            extension = os.path.splitext(filename)[1].lower()

            if extension not in EXTENSIONS:
                continue

            source_file = os.path.join(root, filename)

            relative_path = os.path.relpath(
                root,
                SOURCE_FOLDER
            )

            destination_folder = os.path.join(
                DESTINATION_FOLDER,
                relative_path
            )

            os.makedirs(destination_folder, exist_ok=True)

            destination_file = os.path.join(
                destination_folder,
                filename
            )

            if os.path.exists(destination_file):
                print(f"[SKIP] Já existe: {destination_file}")
                continue

            print(f"[MOVE] {source_file}")
            print(f"     -> {destination_file}")

            shutil.move(source_file, destination_file)

            moved += 1

    print()
    print(f"{moved} vídeo(s) movido(s).")


if __name__ == "__main__":
    move_videos()