import os, csv, time, json

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

# Reading playlists.csv dataset
print(PROCESS_FORMAT, "Reading playlists data train")
track_count = []
path_csv = 'data/data-training/playlists.csv'
track_count = {}
with open(path_csv) as csv_file:
  # starting
  print(READING_FORMAT, path_csv)
  t_start = time.perf_counter()
  # read and process
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    for id in row['track_ids'].split():
      if id in track_count: track_count[id] += 1
      else: track_count[id] = 1
  # Finished
  print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')

# Convert to list
track_count_list = []
for k,v in track_count.items():
  track_count_list.append([k,v])
# Sort with index 1: count value
track_count_list.sort(key=lambda row: (row[1]), reverse=True)

# Creating saving directory path
if not os.path.exists(path_pop):
  os.makedirs(path_pop)

# Writing to track_count.csv
print(PROCESS_FORMAT, "Export popular tracks")
path_csv = path_pop + '/track-count.csv'
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
  # starting
  print(EXPORT_FORMAT, path_csv)
  t_start = time.perf_counter()
  writer = csv.writer(f)
  # write header
  header = ['track_id', 'count']
  writer.writerow(header)
  # write content
  for item in track_count_list:
    writer.writerow(item)
  # finishing
  print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')

# Finishing
track_count = len(track_count_list)
print('   - Tracks count :', track_count)
print('   - Max count  :', track_count_list[0][1])
print('   - Min count  :', track_count_list[-1][1])

# update parameters values
params['n_vocab'] = track_count
json.dump(params, open('parameters.json', 'w'), indent=2)