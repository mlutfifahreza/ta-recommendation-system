import os

RUNNING_STRING = '\033[33m' + "Running :" + '\033[0m'
TOTAL_PLAYLIST = 50000

files = [
    # PROCESS : DATA
    "logic/0-data/p1_data_preprocessing_200k_selection.py "+ str(TOTAL_PLAYLIST),  # p2_text_preprocessing_title_cleaning called here
    "logic/0-data/p3_data_split.py "+ str(TOTAL_PLAYLIST),

    # PROCESS : TRAINING Model CF Wordnet
    "logic/1-model/p4_model_train_cf_wordnet_1_tokens.py "+ str(TOTAL_PLAYLIST),
    "logic/1-model/p4_model_train_cf_wordnet_2_token-20tokens.py "+ str(TOTAL_PLAYLIST),
    "logic/1-model/p4_model_train_cf_wordnet_3_token-50tracks.py "+ str(TOTAL_PLAYLIST),

    # PROCESS : TRAINING Model CF Popularity
    "logic/1-model/p5_model_train_cf_popularity.py",

    # PROCESS : TRAINING Model CBF Word2Vec Continuous Bag of Word (CBOW)
    # "logic/1-model/p6_model_train_cbf_cbow.py",

    # EXTRA
    # "logic/0-data/extract_playlist_titles.py",
    # "logic/0-data/extract_known_char.py",
    # "logic/0-data/extract_playlist_tokens.py",
]

for file in files:
    print('\n'+ RUNNING_STRING, file)
    os.system("python3 " + file)