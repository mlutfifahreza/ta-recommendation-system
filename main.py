import os

RUNNING_STRING = '\033[33m' + "Running :" + '\033[0m'

files = [
    "logic/0-data/p1_data_preprocessing_200k_selection.py", 
    # p2_text_preprocessing_title_cleaning triggered inside p1
    "logic/0-data/p3_data_split.py",
    # "logic/0-data/extract_playlist_titles.py",
    # "logic/0-data/extract_known_char.py",
    # "logic/0-data/extract_playlist_tokens.py",
]

for file in files:
    print('\n'+ RUNNING_STRING, file)
    os.system("python3 " + file)