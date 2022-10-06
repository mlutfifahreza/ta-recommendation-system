import os, json

# params
params = json.load(open('params.json'))
n_playlist = params['n_playlist']

# Paths
paths = [
  f'data/general',
  f'data/data_all/playlist={n_playlist}',
  f'data/data_train/playlist={n_playlist}',
  f'data/data_valid/playlist={n_playlist}',
  f'data/data_test/playlist={n_playlist}',
  f'data/model/pop/playlist={n_playlist}',
  f'data/model/token_sim/playlist={n_playlist}',
  f'data/model/track_sim/playlist={n_playlist}',]

for path in paths:
  if not os.path.exists(path):
    os.makedirs(path)

# create params vars
if f'{n_playlist}' not in params['result']:
  params['result'][f'{n_playlist}'] = {}
json.dump(params, open('params.json', 'w'), indent=2)