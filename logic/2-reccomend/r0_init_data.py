import csv, json

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# General Variables
params = json.load(open('parameters.json'))
n_playlist = params['n_playlist']
path_data_test = f'data/data_test/playlist={n_playlist}'
# # # # # # # # # # # # # # # # # # # # # #

# Variables
playlists_test = {}
pid_list = []

# FCM: init inputs
path_csv =  path_data_test + '/playlists_test.csv'
with open(path_csv) as csv_file:
  # starting
  print(READING_FORMAT, path_csv)
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    playlist_id = row['playlist_id']
    title = row['title']
    track_ids = row['track_ids'].split()
    new_playlist = {}
    # 0 title only
    new_playlist['title'] = title
    n_list = params['n_list']
    for n in n_list:
      # 1 track_id
      new_playlist[str(n)] = track_ids[:n]
    # full playlist
    new_playlist['all'] = track_ids
    # add to json dict
    playlists_test[playlist_id] = new_playlist
  print(f'✅ Finished')

# Save vector data validation
path_export = path_data_test + '/playlists_test.json'
json.dump(playlists_test, open(path_export, 'w'), indent=2)