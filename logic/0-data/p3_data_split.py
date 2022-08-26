import csv, time, json
import random

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

# Variables
n_total = n_playlist
n_done = n_train = n_test = 0
r_train = 0.9
r_test = 0.1
n_total_train = n_total * r_train
n_total_test = n_total * r_test

def write_split_data(path, playlist):
  with open(path, 'a+', encoding = 'UTF8', newline = '') as f:
    csv.writer(f).writerow(playlist)

# Reading playlists.csv dataset
path_csv = path_data + '/playlists_all.csv'
path_data_train_file =  path_data_train + '/playlists_train.csv'
path_data_test_file = path_data_test + '/playlists_test.csv'
with open(path_csv) as csv_file:
  # starting
  print(READING_FORMAT, path_csv)
  t_start = time.perf_counter()
  csv_reader = csv.reader(csv_file)
  is_at_header = True
  for row in csv_reader:
    # write header for each file
    if is_at_header:
      for path_w in [path_data_train_file, path_data_test_file]:
        with open(path_w, 'w', encoding = 'UTF8', newline = '') as f:
          csv.writer(f).writerow(row)
      is_at_header = False
    else:
      x = random.random()
      if (x <= r_train and n_train < n_total_train): 
        write_split_data(path_data_train_file, row)
        n_train += 1
      elif (n_test < n_total_test): 
        write_split_data(path_data_test_file, row)
        n_test += 1
      else: 
        write_split_data(path_data_train_file, row)
        n_train += 1
      # Progress stats
      n_done += 1
      t_elapsed = time.perf_counter()-t_start
      t_remaining = (n_total-n_done)/n_done * t_elapsed
      print(f'\r🟡 Progress: {n_done}/{n_total} '
        + f'Elapsed: {t_elapsed:.3f}s '
        + f'ETA: {t_remaining:.3f}s', end = ' ')
  # Finishing
  print(f'\r✅ Done: {n_done}/{n_total} - '
    + f'Elapsed: {t_elapsed:.3f}s'
    + ' '*20)

# Finishing
print('   - All Playlist :', n_done)
print('   - Training     :', n_train)
print('   - Testing      :', n_test)
