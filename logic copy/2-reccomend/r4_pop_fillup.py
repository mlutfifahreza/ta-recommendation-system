import csv, json
from math import log2, floor

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# General Variables
params = json.load(open('params.json'))
n_playlist = params['n_playlist']
n_recc = params['n_recc']
path_data_test = f'data/data_test/playlist={n_playlist}'
path_pop = f'data/model/pop/playlist={n_playlist}'
# # # # # # # # # # # # # # # # # # # # # #

# Reading track-count.csv
pop_n_recc = []
print(PROCESS_FORMAT, "Reading playlists data train")
path_csv = path_pop + '/track-count.csv'
with open(path_csv) as csv_file:
  print(READING_FORMAT, path_csv)
  csv_reader = csv.DictReader(csv_file)
  count = 0
  for row in csv_reader:
    if count == n_recc: 
      break
    else: 
      pop_n_recc.append(row['track_id'])
      count += 1
  print(f'✅ Finished')

def pop_fillup(playlists_reccomend):
  playlists_reccomend_copy = playlists_reccomend.copy()
  for pid, track_value in playlists_reccomend_copy.items():
    count = len(track_value)
    i = 0
    while count<n_recc:
      new_id = pop_n_recc[i]
      i += 1
      if new_id not in track_value:
        playlists_reccomend[pid][new_id] = 0
        count += 1

# title only
path_playlists_reccomend = path_data_test + '/playlists_reccomend_title.json'
playlists_reccomend = json.load(open(path_playlists_reccomend))
pop_fillup(playlists_reccomend)
json.dump(playlists_reccomend, open(path_playlists_reccomend, 'w'), indent=2)

n_list = params['n_list']
for n in n_list:
  # track only
  path_playlists_reccomend = path_data_test + f'/playlists_reccomend_{n}.json'
  playlists_reccomend = json.load(open(path_playlists_reccomend))
  pop_fillup(playlists_reccomend)
  json.dump(playlists_reccomend, open(path_playlists_reccomend, 'w'), indent=2)
  # title + track
  path_playlists_reccomend = path_data_test + f'/playlists_reccomend_title+{n}.json'
  playlists_reccomend = json.load(open(path_playlists_reccomend))
  pop_fillup(playlists_reccomend)
  json.dump(playlists_reccomend, open(path_playlists_reccomend, 'w'), indent=2)