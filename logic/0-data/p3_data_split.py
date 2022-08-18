import csv, time, json
import random

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

def write_split_data(path, playlist):
  with open(path, 'a+', encoding = 'UTF8', newline = '') as f:
    csv.writer(f).writerow(playlist)

# Variables
n_total = n_playlist
n_done = n_train = n_test = 0
r_train = 0.9
r_test = 0.1
n_total_train = n_total * r_train
n_total_test = n_total * r_test

# Reading playlists.csv dataset
path_csv = 'data/data-all/playlists.csv'
path_train =  'data/data-training/playlists.csv'
path_test = 'data/data-testing/playlists.csv'
with open(path_csv) as csv_file:
  # starting
  print(READING_FORMAT, path_csv)
  t_start = time.perf_counter()
  csv_reader = csv.reader(csv_file)
  is_at_header = True
  for row in csv_reader:
    # write header for each file
    if is_at_header:
      for path_w in [path_train, path_test]:
        with open(path_w, 'w', encoding = 'UTF8', newline = '') as f:
          csv.writer(f).writerow(row)
      is_at_header = False
    else:
      x = random.random()
      if (x <= r_train and n_train < n_total_train): 
        write_split_data(path_train, row)
        n_train += 1
      elif (n_test < n_total_test): 
        write_split_data(path_test, row)
        n_test += 1
      else: 
        write_split_data(path_train, row)
        n_train += 1
      # Progress stats
      n_done += 1
      t_elapsed = time.perf_counter()-t_start
      t_remaining = (n_total-n_done)/n_done * t_elapsed
      print(f'\r🟡 Done: {n_done}/{n_total} '
        + f'Elapsed: {t_elapsed:.3f}s '
        + f'ETA: {t_remaining:.3f}s', end = ' ')
  # Finishing
  print(f'\r✅ Done: {n_done}/{n_total} - '
    + f'Elapsed: {t_elapsed:.3f}s'
    + ' '*20)

# Finishing
print('   - All Playlist :', n_done)
print('   - Training   :', n_train)
print('   - Testing    :', n_test)
