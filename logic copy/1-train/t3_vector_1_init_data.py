import csv, time, json, random

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# General Variables
params = json.load(open('params.json'))
n_playlist = params['n_playlist']
window_size = params['window_size']
path_data_train = f'data/data_train/playlist={n_playlist}'
path_data_valid = f'data/data_valid/playlist={n_playlist}'
path_track_sim = f'data/model/track_sim/playlist={n_playlist}'

# # # # # # # # # # # # # # # # # # # # # #


# Variables
path_corpus_train = path_track_sim + '/playlists_corpus_train.csv'
def create_csv_file(path_csv):
  print(EXPORT_FORMAT, path_csv)
  with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
    pass

def csv_add_new_data(path_csv, new_corpus):
  with open(path_csv, 'a+', encoding = 'UTF8', newline = '') as f:
    csv.writer(f).writerow([new_corpus])

# Generating data train (Corpus)
print(PROCESS_FORMAT, 'Generating data train (Corpus)')
path_csv = path_data_train + '/playlists_train.csv'
with open(path_csv) as csv_file:
  ...
  create_csv_file(path_corpus_train)
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    track_ids = row['track_ids']
    csv_add_new_data(path_corpus_train, track_ids)
  ...

# Extracting neighbors
track_neighbors = {}
path_csv = path_data_valid + '/playlists_valid.csv'
with open(path_csv) as csv_file:
  ...
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    track_ids = row['track_ids']
    track_ids = track_ids.split()
    n_track_ids = len(track_ids)
    for i in range(n_track_ids):
      for neighbor_index in (i-window_size, i+window_size):
        if (
          neighbor_index != i
          and neighbor_index > 0 
          and neighbor_index < n_track_ids
        ):
          id1, id2 = track_ids[i], track_ids[neighbor_index]
          # add id1 neighbors
          if id1 not in track_neighbors: track_neighbors[id1] = [id2]
          else: track_neighbors[id1].append(id2)
          # add id2 neighbors
          if id2 not in track_neighbors: track_neighbors[id2] = [id1]
          else: track_neighbors[id2].append(id1)
    ...

# Random pick neighbors
print(PROCESS_FORMAT, 'Random pick neighbors')
unique_track_ids = list(track_neighbors.keys())
data_valid = {
  'header' : ['id1', 'id2', 'is_neighbor'],
  'value' : []
}
for key, val in track_neighbors.items():
  for neighbor in val:
    if (random.random() < 0.25):
      data_valid['value'].append([key, neighbor, 1])

# Save vector data validation
path_export = path_track_sim + '/data_valid.json'
json.dump(data_valid, open(path_export, 'w'))