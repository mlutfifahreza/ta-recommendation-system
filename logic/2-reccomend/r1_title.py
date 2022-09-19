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
path_word_sim = f'data/model/word_sim/playlist={n_playlist}'
# # # # # # # # # # # # # # # # # # # # # #


# read test playlists
playlists_test_path = path_data_test + '/playlists_test.json'
playlists_test = json.load(open(playlists_test_path))

# reccomend from title data
token_20tokens = json.load(open(path_word_sim + '/token_20tokens.json'))
token_100tracks = json.load(open(path_word_sim + '/token_100tracks.json'))
playlists_reccomend_title= {}
for pid, playlist_detail in playlists_test.items():
  reccomendation = {}
  tokens = playlist_detail['title'].split()
  for token in tokens:
    try:
      similar_tokens = token_20tokens[token]
      for similar_token, sim_value in similar_tokens.items():
        for track in token_100tracks[similar_token]:
          if track in reccomendation:
            reccomendation[track] += sim_value
          else:
            reccomendation[track] = sim_value
      # get top 1000 reccomendation
      reccomendation = { 
        key:value for (key, value) in sorted(
          reccomendation.items(), 
          key=lambda x: x[1], 
          reverse=True)[:1000]}
    except:
      pass
  playlists_reccomend_title[pid] = reccomendation

# save reccomendation
path_export = path_data_test + '/playlists_reccomend_title.json'
print(EXPORT_FORMAT, path_export)
json.dump(playlists_reccomend_title, open(path_export, 'w'), indent=2)
print(f'✅ Finished')