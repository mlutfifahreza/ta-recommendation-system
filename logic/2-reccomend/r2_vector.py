import time, csv, sys, json
import numpy as np
import matplotlib.pyplot as plt
from gensim.models import FastText

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# General Variables
params = json.load(open('parameters.json'))
n_playlist = params['n_playlist']
path_data_test = f'data/data_test/playlist={n_playlist}'
path_data_train = f'data/data_train/playlist={n_playlist}'
path_vector = f'data/model/vector/playlist={n_playlist}'
# # # # # # # # # # # # # # # # # # # # # #


# read test playlists
playlists_test_path = path_data_test + '/playlists_test.json'
playlists_test = json.load(open(playlists_test_path))

# load track_list
path_json = path_data_train + '/track_list.json'
track_list = json.load(open(path_json))

# load best vector model
best_model_path = params['result'][str(n_playlist)]['best_model_path']
model = FastText.load(best_model_path)

# reccomend from n random data
n_list = params['n_list']
for n in n_list:
  print(SUBPROCESS_FORMAT, f'Get reccomend for {n} first track')
  playlists_reccomend= {}
  # init
  n_done = 0 
  n_total = len(playlists_test)
  t_start = time.perf_counter()
  t_elapsed = 0
  for pid, playlist_detail in playlists_test.items():
    reccomendation = {}
    track_ids = playlist_detail[str(n)]
    # start
    for id in track_ids:
      for train_id in track_list:
        if id == train_id : continue
        score = model.wv.similarity(id, train_id)
        reccomendation[train_id] = float(score)
    # get top 1000
    reccomendation = { 
      key:value for (key, value) in sorted(
        reccomendation.items(), 
        key=lambda x: x[1], 
        reverse=True)[:1000]}
    playlists_reccomend[pid] = reccomendation
    # Progress stats
    n_done += 1
    t_elapsed = time.perf_counter()-t_start
    t_remaining = (n_total-n_done)/n_done * t_elapsed
    print(f'\r🟡 Progress: {n_done}/{n_total} '
      + f'Elapsed: {t_elapsed:.3f}s '
      + f'ETA: {t_remaining:.3f}s', end = ' ')
  # end
  print(f'\r✅ Elapsed: {t_elapsed:.3f}s' + ' '*40)
  print(f'   - AVG: {t_elapsed/len(playlists_test):.3f}s per playlist')

  # save reccomendation
  path_export = path_data_test + f'/playlists_reccomend_{n}.json'
  print(EXPORT_FORMAT, path_export)
  json.dump(playlists_reccomend, open(path_export, 'w'), indent=2)
  print(f'✅ Finished')