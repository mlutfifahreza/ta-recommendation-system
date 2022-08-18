import time, csv, sys, json
import numpy as np
import matplotlib.pyplot as plt

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'

# Parameters
params = json.load(open('parameters.json'))
n_playlist = params['n_playlist']
n_vocab = params['n_vocab']
n_data_train = params['n_data_train']
n_data_batch = params['n_data_batch']
size_embed = params['size_embed']
learn_rate = params['learn_rate']
n_epoch = params['n_epoch']

# Paths
path_pop = f'data/model/pop/playlist={n_playlist}'
path_word_sim = f'data/model/word_sim/playlist={n_playlist}'
path_vector = f'data/model/vector/embed={size_embed}-playlist={n_playlist}-rate={learn_rate}'
path_fcm = f'data/model/fcm/embed={size_embed}-playlist={n_playlist}'