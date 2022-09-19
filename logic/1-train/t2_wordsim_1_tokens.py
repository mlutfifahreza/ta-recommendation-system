import os, csv, time, sys, json
csv.field_size_limit(sys.maxsize)

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# General Variables
params = json.load(open('parameters.json'))
n_playlist = params['n_playlist']
path_general = f'data/general'
path_data_train = f'data/data_train/playlist={n_playlist}'
path_word_sim = f'data/model/word_sim/playlist={n_playlist}'
# # # # # # # # # # # # # # # # # # # # # #


# Get token - tracks relationship
print(PROCESS_FORMAT, "Get token-tracks relationship")
token_tracks = {}
path_csv = path_data_train + '/playlists_train.csv'
with open(path_csv) as csv_file:
  print(READING_FORMAT, path_csv)
  n_done, n_total = 0, int(n_playlist * 0.9)
  t_start, t_elapsed = time.perf_counter(), 0
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    title = row['title']
    track_ids = row['track_ids'].split()
    for token in title.split():
      # add track_ids without duplicate
      if token in token_tracks.keys(): 
        token_tracks[token] = list(set(token_tracks[token] + track_ids))
      else: token_tracks[token] = track_ids
    n_done += 1
    t_elapsed = time.perf_counter()-t_start
    t_remaining = (n_total-n_done)/n_done * t_elapsed
    print(f'\r🟡 {n_done}/{n_total} - Elapsed: {t_elapsed:.3f}s '
      + f'ETA: {t_remaining:.3f}s', end = ' ')
  print(f'\r✅ {n_done}/{n_total} - '
    + f'Elapsed: {t_elapsed:.3f}s' + ' '*40)

# Writing to token_tracks.csv
path_csv = path_word_sim + '/token-tracks.csv'
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
  print(EXPORT_FORMAT, path_csv)
  writer = csv.writer(f)
  header = ['token','track_ids']
  writer.writerow(header)
  for key, value in token_tracks.items():
    writer.writerow([key, ' '.join(value)])
  print(f'✅ Finished')

# Finishing
n_token = len(token_tracks)
print('   - Unique tokens:', n_token)

# update parameters values
params['result'][str(n_playlist)]['n_token'] = n_token
json.dump(params, open('parameters.json', 'w'), indent=2)