import json

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# General Variables
params = json.load(open('parameters.json'))
n_playlist = params['n_playlist']
path_data_test = f'data/data_test/playlist={n_playlist}'
playlists_test_path = path_data_test + '/playlists_test.json'
playlists_test = json.load(open(playlists_test_path))
# # # # # # # # # # # # # # # # # # # # # #

# reccomend from n random data
playlists_reccomend = {}
playlists_reccomend_title = json.load(open(path_data_test + '/playlists_reccomend_title.json'))
n_list = params['n_list']
for n in n_list:
  print(SUBPROCESS_FORMAT, f'Get reccomend for title + {n} first track')
  playlists_reccomend_n = json.load(open(path_data_test + f'/playlists_reccomend_{n}.json'))
  # Combine
  for pid in playlists_test.keys():
    reccomendation = {}
    # start
    for k,v in playlists_reccomend_n[pid].items():
      reccomendation[k] = v
    for k,v in playlists_reccomend_title[pid].items():
      if k in reccomendation:
        reccomendation[k] += v
      else:
        reccomendation[k] = v
    # get top 1000
    reccomendation = { 
      key:value for (key, value) in sorted(
        reccomendation.items(), 
        key=lambda x: x[1], 
        reverse=True)[:1000]}
    playlists_reccomend[pid] = reccomendation
  # save reccomendation
  path_export = path_data_test + f'/playlists_reccomend_title+{n}.json'
  print(EXPORT_FORMAT, path_export)
  json.dump(playlists_reccomend, open(path_export, 'w'), indent=2)
  print(f'✅ Finished')