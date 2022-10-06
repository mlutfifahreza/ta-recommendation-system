import csv, time, json
import random

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# General Variables
params = json.load(open('params.json'))
n_playlist = params['n_playlist']
path_data_all = f'data/data_all/playlist={n_playlist}'
path_data_train = f'data/data_train/playlist={n_playlist}'
path_data_valid = f'data/data_valid/playlist={n_playlist}'
path_data_test = f'data/data_test/playlist={n_playlist}'
# # # # # # # # # # # # # # # # # # # # # #


# Variables
n_total = n_playlist
n_done = n_train = n_valid = n_test = 0
r_train, r_valid, r_test = 0.9, 0.05, 0.05
n_total_train = n_total * r_train
n_total_valid = n_total * r_valid
n_total_test = n_total * r_test

def write_split_data(path, playlist):
  with open(path, 'a+', encoding = 'UTF8', newline = '') as f:
    csv.writer(f).writerow(playlist)

# Reading playlists.csv dataset
path_csv = path_data_all + '/playlists_all.csv'
path_data_train_file =  path_data_train + '/playlists_train.csv'
path_data_valid_file = path_data_valid + '/playlists_valid.csv'
path_data_test_file = path_data_test + '/playlists_test.csv'
path_playlists = [
  path_data_train_file,
  path_data_valid_file,
  path_data_test_file
]
with open(path_csv) as csv_file:
  # starting
  print(READING_FORMAT, path_csv)
  t_start = time.perf_counter()
  csv_reader = csv.reader(csv_file)
  is_at_header = True
  for row in csv_reader:
    # write header for each file
    if is_at_header:
      for path_w in path_playlists:
        with open(path_w, 'w', encoding = 'UTF8', newline = '') as f:
          csv.writer(f).writerow(row)
      is_at_header = False
    else:
      x = random.random()
      if (x <= r_train and n_train < n_total_train): 
        write_split_data(path_data_train_file, row)
        n_train += 1
      elif (r_train < x <= r_train+r_valid and n_valid < n_total_valid): 
        write_split_data(path_data_valid_file, row)
        n_valid += 1
      elif n_test < n_total_test:
        write_split_data(path_data_test_file, row)
        n_test += 1
      elif n_train < n_total_train: 
        write_split_data(path_data_train_file, row)
        n_train += 1
      else:
        write_split_data(path_data_valid_file, row)
        n_valid += 1
      # Progress stats
      n_done += 1
      t_elapsed = time.perf_counter()-t_start
      t_remaining = (n_total-n_done)/n_done * t_elapsed
      print(f'\r🟡 {n_done}/{n_total} '
        + f'Elapsed: {t_elapsed:.3f}s '
        + f'ETA: {t_remaining:.3f}s', end = ' ')
  # Finishing
  print(f'\r✅ {n_done}/{n_total} - '
    + f'Elapsed: {t_elapsed:.3f}s'
    + ' '*40)

# Finishing
print('   - All   :', n_done)
print('   - Train :', n_train)
print('   - Valid :', n_valid)
print('   - Test  :', n_test)
