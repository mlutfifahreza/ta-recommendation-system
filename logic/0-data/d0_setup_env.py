import os, json

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# Parameters
params = json.load(open('parameters.json'))
n_playlist = params['n_playlist']

# Paths
path_general = f'data/general'
path_data_all = f'data/data_all/playlist={n_playlist}'
path_data_train = f'data/data_train/playlist={n_playlist}'
path_data_valid = f'data/data_valid/playlist={n_playlist}'
path_data_test = f'data/data_test/playlist={n_playlist}'
path_pop = f'data/model/pop/playlist={n_playlist}'
path_word_sim = f'data/model/word_sim/playlist={n_playlist}'
path_vector = f'data/model/vector/playlist={n_playlist}'
path_vector_1 = f'data/model/vector_1/playlist={n_playlist}'
path_vector_2 = f'data/model/vector_2/playlist={n_playlist}'
path_vector_3 = f'data/model/vector_3/playlist={n_playlist}'

paths = [
  path_general,
  path_data_all,
  path_data_train,
  path_data_valid,
  path_data_test,
  path_pop,
  path_word_sim,
  path_vector,
  path_vector_1,
  path_vector_2,
  path_vector_3,
  ]

for path in paths:
  if not os.path.exists(path):
    os.makedirs(path)

# create params vars
if f'{n_playlist}' not in params['result']:
  params['result'][f'{n_playlist}'] = {}
json.dump(params, open('parameters.json', 'w'), indent=2)