import os, time

RUNNING_FORMAT = '\n\033[33m' + 'RUNNING:' + '\033[0m'

paths = [
    # # PROCESS: DATA
    # f'logic/0-data/p1_data_preprocessing_playlist_selection.py', 
    # # p2_text_preprocessing_title_cleaning called in p1
    # f'logic/0-data/p3_data_split.py',

    # # PROCESS: TRAINING Model Popularity
    # f'logic/1-model/p4_model_train_popularity.py ',
    
    # # PROCESS: TRAINING Model Wordnet
    # f'logic/1-model/p5_model_train_wordnet_1_tokens.py',
    # f'logic/1-model/p5_model_train_wordnet_2_token-20tokens.py',
    # f'logic/1-model/p5_model_train_wordnet_3_token-50tracks.py',

    # # PROCESS: TRAINING Model Word2Vec Continuous Bag of Word (CBOW)
    f'logic/1-model/p6_model_train_cbow_1_get_train_data.py',
    f'logic/1-model/p6_model_train_cbow_2_training.py',

    # PROCESS: TRAINING Model Fuzzy C-Means Clustering (FCM)
    # f'logic/1-model/p7_model_train_fcm.py',
]

for path in paths:
    print(RUNNING_FORMAT, path)
    os.system(f'python3 {path}')