import os, csv, time, json

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
path_pop = f'data/model/pop/playlist={n_playlist}'
# # # # # # # # # # # # # # # # # # # # # #


# Reading playlists.csv dataset
print(PROCESS_FORMAT, "Reading playlists data train")
path_csv = path_data_train + '/playlists_train.csv'
track_count = {}
with open(path_csv) as csv_file:
  print(READING_FORMAT, path_csv)
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    for id in row['track_ids'].split():
      if id in track_count: track_count[id] += 1
      else: track_count[id] = 1
  print(f'✅ Finished')

# Convert to list
track_count_list = []
for k,v in track_count.items():
  track_count_list.append([k,v])
# Sort with index 1: count value
track_count_list.sort(key=lambda row: (row[1]), reverse=True)
track_list = list(track_count.keys())

# Writing to track_count.csv
print(PROCESS_FORMAT, "Export popular tracks")
path_csv = path_pop + '/track-count.csv'
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
  print(EXPORT_FORMAT, path_csv)
  writer = csv.writer(f)
  header = ['track_id', 'count']
  writer.writerow(header)
  for item in track_count_list:
    writer.writerow(item)
  print(f'✅ Finished')

# Finishing
track_count = len(track_count_list)
print('   - Tracks count :', track_count)
print('   - Max count    :', track_count_list[0][1])
print('   - Min count    :', track_count_list[-1][1])

# update parameters values
params['result'][f'{n_playlist}']['n_track'] = track_count
json.dump(params, open('parameters.json', 'w'), indent=2)
path_export = path_data_train + '/track_list.json'
json.dump(track_list, open(path_export, 'w'))