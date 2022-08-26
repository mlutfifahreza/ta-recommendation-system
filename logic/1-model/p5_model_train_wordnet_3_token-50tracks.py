import os, csv, time, sys, json
csv.field_size_limit(sys.maxsize)

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

# Reading track_count.csv dataset
track_count = {}
path_csv = path_pop + '/track-count.csv'
with open(path_csv) as csv_file:
  # starting
  print(READING_FORMAT, path_csv)
  t_start = time.perf_counter()
  # read and process
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    track_count[row['track_id']] = int(row['count'])
  # Finished
  print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')

# Reading token_tracks.csv dataset
token_tracks = {} # key = token, value = list of [track_id, count]
path_csv = path_word_sim + '/token-tracks.csv'
with open(path_csv) as csv_file:
  # starting
  print(READING_FORMAT, path_csv)
  n_done = 0
  t_start = time.perf_counter()
  # read and process
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    token = row['token']
    token_tracks[token] = []
    # add track_id and count for each track in token
    for id in row['track_ids'].split():
      id_count = track_count[id]
      token_tracks[token].append([id, id_count])
    # sort the tracks by count
    token_tracks[token].sort(key=lambda idx: (idx[1]), reverse=True)
    # trim to first 50 only
    token_tracks[token] = token_tracks[token][:50]
  # finishing
  print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')

# Writing to token-50tracks.csv
path_csv = path_word_sim + '/token-50tracks.csv'
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
  # starting
  print(EXPORT_FORMAT, path_csv)
  t_start = time.perf_counter()
  writer = csv.writer(f)
  # write header
  header = ['token', '50tracks']
  writer.writerow(header)
  # write content
  for token, track_count in token_tracks.items():
    track_ids = ''
    for value in track_count:
      track_ids += value[0] + ' '
    writer.writerow([token, track_ids])
  # Finished
  print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')

