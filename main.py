import os

os.system("python3 logic/data/extract_data-200.py ")
os.system("python3 logic/data/extract_playlist_titles.py")
os.system("python3 logic/data/extract_known_char.py")
# Manual operation : write known_characters_mapping.csv