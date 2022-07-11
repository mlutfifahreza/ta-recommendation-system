import os

RUNNING_STRING = '\033[33m' + "Running :" + '\033[0m'

files = [
    # PROCESS : DATA
    "logic/0-data/p1_data_preprocessing_200k_selection.py",  # p2_text_preprocessing_title_cleaning called here
    "logic/0-data/p3_data_split.py",

    # PROCESS : TRAINING Model CF Wordnet
    "logic/1-model/p4_model_train_cf_wordnet_1_tokens.py",
    "logic/1-model/p4_model_train_cf_wordnet_2_token-20tokens.py",
    "logic/1-model/p4_model_train_cf_wordnet_3_token-50tracks.py",

    # PROCESS : TRAINING Model CF Popularity
    "logic/1-model/p5_model_train_cf_popularity.py",

    # EXTRA
    # "logic/0-data/extract_playlist_titles.py",
    # "logic/0-data/extract_known_char.py",
    # "logic/0-data/extract_playlist_tokens.py",
]

for file in files:
    print('\n'+ RUNNING_STRING, file)
    os.system("python3 " + file)