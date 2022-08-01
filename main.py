import os

RUNNING_STRING = '\033[33m' + "Running :" + '\033[0m'
n_playlist = 10

commands = [
    # PROCESS : DATA
    f"python3 logic/0-data/p1_data_preprocessing_playlist_selection.py {n_playlist}", 
    # p2_text_preprocessing_title_cleaning called here
    f"python3 logic/0-data/p3_data_split.py {n_playlist}",

    # PROCESS : TRAINING Model CF Popularity
    "python3 logic/1-model/p4_model_train_popularity.py",
    
    # PROCESS : TRAINING Model CF Wordnet
    f"python3 logic/1-model/p5_model_train_wordnet_1_tokens.py {n_playlist}",
    f"python3 logic/1-model/p5_model_train_wordnet_2_token-20tokens.py {n_playlist}",
    f"python3 logic/1-model/p5_model_train_wordnet_3_token-50tracks.py {n_playlist}",

    # PROCESS : TRAINING Model CBF Word2Vec Continuous Bag of Word (CBOW)
    "python3 logic/1-model/p6_model_train_cbow.py",

    # EXTRA
    # "python3 logic/0-data/extract_playlist_titles.py",
    # "python3 logic/0-data/extract_known_char.py",
    # "python3 logic/0-data/extract_playlist_tokens.py",
]

for command in commands:
    print(RUNNING_STRING, command)
    os.system(command)
    print()