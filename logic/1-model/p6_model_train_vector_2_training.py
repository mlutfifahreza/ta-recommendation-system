from concurrent.futures import BrokenExecutor
import enum
import os, csv, time, json
import numpy as np
import matplotlib.pyplot as plt
from gensim.test.utils import datapath
from gensim.test.utils import common_texts
from gensim.models import FastText

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# Parameters
params = json.load(open('parameters.json'))
n_playlist = params['n_playlist']
size_embed = params['size_embed']
n_epoch = params['n_epoch']
div_cluster = params['div_cluster']
iter_max = params['iter_max']
change_threshold = params['change_threshold']
fuzzy_param = params['fuzzy_param']

# Paths
path_general = f'data/general'
path_data = f'data/data_all/playlist={n_playlist}'
path_data_train = f'data/data_train/playlist={n_playlist}'
path_data_test = f'data/data_test/playlist={n_playlist}'
path_pop = f'data/model/pop/playlist={n_playlist}'
path_word_sim = f'data/model/word_sim/playlist={n_playlist}'
path_vector = f'data/model/vector/playlist={n_playlist}-embed={size_embed}'
path_fcm = f'data/model/fcm/playlist={n_playlist}-embed={size_embed}'

# FastText - load data
print(PROCESS_FORMAT, 'Corpus Loading')
t_start = time.perf_counter()
corpus_file = datapath(f'{os.getcwd()}/{path_vector}/playlists_as_sentence.csv')  # absolute path to corpus
model = FastText(vector_size=size_embed, window=3, min_count=1)
model.build_vocab(corpus_file=corpus_file)  # scan over corpus to build the vocabulary
total_words = model.corpus_total_words  # number of words in the corpus
track_keys = model.wv.key_to_index.keys()
t_elapsed = time.perf_counter()-t_start
print(f'✅ Finished {t_elapsed:.3f}s')

# FastText - training
print(PROCESS_FORMAT, 'FastText Train')
t_start = time.perf_counter()
model.train(corpus_file=corpus_file, total_words=total_words, epochs=n_epoch)
t_elapsed = time.perf_counter()-t_start
print(f'✅ Finished {t_elapsed:.3f}s')

# Extract embeddings
path_csv = path_vector + '/track-vector.csv'
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
  # starting
  print(EXPORT_FORMAT, path_csv)
  n_done, n_total = 0, len(track_keys)
  t_start = time.perf_counter()
  # write header
  writer = csv.writer(f)
  header = ['track', 'vector']
  writer.writerow(header)
  # write content
  for i,key in enumerate(track_keys):
    vector = model.wv[key]
    vector = ' '.join([str(e) for e in vector])
    writer.writerow([key, vector])
    # progress stats
    n_done += 1
    t_elapsed = time.perf_counter()-t_start
    t_remaining = (n_total-n_done) / n_done * t_elapsed
    print(f'\r🟡 Progress: {n_done}/{n_total} '
      + f'Elapsed: {t_elapsed:.3f}s '
      + f'ETA: {t_remaining:.3f}s', end = ' ')
  # finishing
  print(f'\r✅ Done: {n_done}/{n_total} - '
    + f'Elapsed: {t_elapsed:.3f}s'
    + ' '*20)
