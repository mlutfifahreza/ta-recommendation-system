import os, json

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

paths = [
  path_general,
  path_data,
  path_data_train,
  path_data_test,
  path_pop,
  path_word_sim,
  path_vector,
  path_fcm]

for path in paths:
  if not os.path.exists(path):
    os.makedirs(path)

# create params vars
params['vars'][f'{n_playlist}'] = {}
json.dump(params, open('parameters.json', 'w'), indent=2)