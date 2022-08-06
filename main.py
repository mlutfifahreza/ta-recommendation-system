import os

RUNNING_STRING = '\033[33m' + 'Running:' + '\033[0m'
n_playlist = 10 * 1000
size_embed = 10
learn_rate = 0.0001
n_epoch = 100
n_cluster = 100

arguments = f'{n_playlist} {size_embed} {learn_rate} {n_epoch} {n_cluster}'

commands = [
    # PROCESS: DATA
    f'python3 logic/0-data/p1_data_preprocessing_playlist_selection.py {arguments}', 
    # p2_text_preprocessing_title_cleaning called here
    f'python3 logic/0-data/p3_data_split.py {arguments}',

    # PROCESS: TRAINING Model Popularity
    f'python3 logic/1-model/p4_model_train_popularity.py  {arguments}',
    
    # PROCESS: TRAINING Model Wordnet
    f'python3 logic/1-model/p5_model_train_wordnet_1_tokens.py {arguments}',
    f'python3 logic/1-model/p5_model_train_wordnet_2_token-20tokens.py {arguments}',
    f'python3 logic/1-model/p5_model_train_wordnet_3_token-50tracks.py {arguments}',

    # PROCESS: TRAINING Model Word2Vec Continuous Bag of Word (CBOW)
    f'python3 logic/1-model/p6_model_train_cbow.py {arguments}',

    # PROCESS: TRAINING Model Fuzzy C-Means Clustering (FCM)
    # f'python3 logic/1-model/p7_model_train_fcm.py {arguments}',
]

for command in commands:
    print(RUNNING_STRING, command)
    os.system(command)
    print()