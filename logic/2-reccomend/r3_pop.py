import time, csv, sys, json
from turtle import right
import numpy as np
import matplotlib.pyplot as plt

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# General Variables
params = json.load(open('parameters.json'))
n_playlist = params['n_playlist']
path_data_test = f'data/data_test/playlist={n_playlist}'
path_pop = f'data/model/pop/playlist={n_playlist}'
# # # # # # # # # # # # # # # # # # # # # #


# read test playlists
playlists_test_path = path_data_test + '/playlists_test.json'
playlists_test = json.load(open(playlists_test_path))

# reading top tracks
track_count = {}
path_csv = path_pop + '/track-count.csv'
with open(path_csv) as csv_file:
  print(READING_FORMAT, path_csv)
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    track_count[row['track_id']] = row['count']
  print(f'✅ Finished')

# reccomend from 5 random data
playlists_reccomend_pop= {}
for pid, playlist_detail in playlists_test.items():
  reccomendation = track_count
  # get top 1000 reccomendation
  reccomendation = { 
    key:value for (key, value) in sorted(
      reccomendation.items(), 
      key=lambda x: x[1], 
      reverse=True)[:1000]}
  playlists_reccomend_pop[pid] = reccomendation

# save reccomendation
path_export = path_data_test + '/playlists_reccomend_pop.json'
print(EXPORT_FORMAT, path_export)
json.dump(playlists_reccomend_pop, open(path_export, 'w'), indent=2)
print(f'✅ Finished')