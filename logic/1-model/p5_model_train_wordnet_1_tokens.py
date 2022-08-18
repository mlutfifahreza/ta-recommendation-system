import os, csv, time, sys, json
csv.field_size_limit(sys.maxsize)

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

# Creating saving directory path
path_dir = f'data/model/word_sim/playlist={n_playlist}'
if not os.path.exists(path_dir):
  os.makedirs(path_dir)

# Get token - tracks relationship
print(PROCESS_FORMAT, "Get token-tracks relationship")
token_tracks = {}
path_csv = 'data/data-training/playlists.csv'
with open(path_csv) as csv_file:
  # starting
  print(READING_FORMAT, path_csv)
  n_total = int(n_playlist * 0.9)
  n_done = 0
  t_start = time.perf_counter()
  # read and process
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    title = row['title']
    track_ids = row['track_ids'].split()
    for token in title.split():
      # add track_ids without duplicate
      if token in token_tracks.keys(): 
        token_tracks[token] = list(set(token_tracks[token] + track_ids))
      else: token_tracks[token] = track_ids
    # progress stats
    n_done += 1
    t_elapsed = time.perf_counter()-t_start
    t_remaining = (n_total-n_done)/n_done * t_elapsed
    print(f'\r🟡 Done: {n_done}/{n_total} '
      + f'Elapsed: {t_elapsed:.3f}s '
      + f'ETA: {t_remaining:.3f}s', end = ' ')
  print(f'\r✅ Done: {n_done}/{n_total} - '
    + f'Elapsed: {t_elapsed:.3f}s'
    + ' '*20)


# Writing to token_tracks.csv
path_csv = path_dir + '/token-tracks.csv'
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
  # starting
  print(EXPORT_FORMAT, path_csv)
  t_start = time.perf_counter()
  writer = csv.writer(f)
  # write header
  header = ['token','track_ids']
  writer.writerow(header)
  # write content
  for key, value in token_tracks.items():
    writer.writerow([key, ' '.join(value)])
  t_elapsed = '{:.3f}'.format(time.perf_counter()-t_start)
  print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')

# Finishing
print('   - Unique tokens:', len(token_tracks))