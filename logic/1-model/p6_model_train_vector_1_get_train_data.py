import os, csv, time, json

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

# Creating saving directory path
if not os.path.exists(path_vector):
  os.makedirs(path_vector)

# Getting data training :
def create_file(path_csv):
  # writing header
  print(EXPORT_FORMAT, path_csv)
  with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
    pass

def add_new_data(path_csv, new_corpus):
  with open(path_csv, 'a+', encoding = 'UTF8', newline = '') as f:
    csv.writer(f).writerow([new_corpus])

# (new) set 2 closest as neighbors
print(PROCESS_FORMAT, 'Generating Vector data train')
path_csv = 'data/data-training/playlists.csv'
with open(path_csv) as csv_file:
  # init
  print(READING_FORMAT, path_csv)
  n_done = 0 
  # n_data_train = 0
  n_total = int(n_playlist * 0.9)
  t_start = time.perf_counter()
  t_elapsed = 0
  # init export file
  path_csv_export = path_vector + '/vector_texts.csv'
  create_file(path_csv_export)
  # read and process
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    track_ids = row['track_ids']
    add_new_data(path_csv_export, track_ids)
    # Progress stats
    n_done += 1
    # n_data_train += 1
    t_elapsed = time.perf_counter()-t_start
    t_remaining = (n_total-n_done)/n_done * t_elapsed
    print(f'\r🟡 Progress: {(n_done*100/n_total):.2f}% '
      + f'Elapsed: {t_elapsed:.3f}s '
      + f'ETA: {t_remaining:.3f}s', end = ' ')
  # end
  print(f'\r✅ Done: 100% '
    + f'Elapsed: {t_elapsed:.3f}s'
    + ' '*20)

# # update parameters values
# params['vars'][f'{n_playlist}']['n_data_train'] = n_data_train
# json.dump(params, open('parameters.json', 'w'), indent=2)