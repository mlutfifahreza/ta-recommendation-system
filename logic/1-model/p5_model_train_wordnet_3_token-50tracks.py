import os, csv, time, sys, json
csv.field_size_limit(sys.maxsize)

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'

# Parameters
params = json.load(open('parameters.json'))
n_playlist = params['n_playlist']
n_vocab = params['vars'][f'{n_playlist}']['n_vocab']
n_data_train = params['vars'][f'{n_playlist}']['n_data_train']
n_data_batch = params['n_data_batch']
size_embed = params['size_embed']
learn_rate = params['learn_rate']
n_epoch = params['n_epoch']

# Paths
path_pop = f'data/model/pop/playlist={n_playlist}'
path_word_sim = f'data/model/word_sim/playlist={n_playlist}'
path_vector = f'data/model/vector/embed={size_embed}-playlist={n_playlist}-rate={learn_rate}'
path_fcm = f'data/model/fcm/embed={size_embed}-playlist={n_playlist}'

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

