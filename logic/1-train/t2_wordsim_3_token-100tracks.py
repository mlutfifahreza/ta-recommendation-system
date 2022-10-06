import csv, time, sys, json
csv.field_size_limit(sys.maxsize)

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# General Variables
params = json.load(open('parameters.json'))
n_playlist = params['n_playlist']
path_pop = f'data/model/pop/playlist={n_playlist}'
path_word_sim = f'data/model/word_sim/playlist={n_playlist}'
# # # # # # # # # # # # # # # # # # # # # #


# Reading track_count.csv dataset
track_count = {}
path_csv = path_pop + '/track-count.csv'
with open(path_csv) as csv_file:
  print(READING_FORMAT, path_csv)
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    track_count[row['track_id']] = int(row['count'])
  print(f'✅ Done')

# Reading token_tracks.csv dataset
token_tracks = {} # key = token, value = list of [track_id, count]
token_100tracks = {}
path_csv = path_word_sim + '/token-tracks.csv'
with open(path_csv) as csv_file:
  print(READING_FORMAT, path_csv)
  t_start = time.perf_counter()
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    token = row['token']
    token_tracks[token] = []
    # add track_id and count for each track in token
    for id in row['track_ids'].split():
      id_count = track_count[id]
      token_tracks[token].append([id, id_count])
    # sort the tracks by count
    token_tracks[token].sort(key=lambda idx: (idx[1]), reverse=True)
    # trim to first 100 only
    token_100tracks[token] = []
    for item in token_tracks[token][:100]:
      token_100tracks[token].append(item[0])
  print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')

# Writing to token_100tracks.csv
path_export = path_word_sim + '/token_100tracks.json'
print(EXPORT_FORMAT, path_export)
json.dump(token_100tracks, open(path_export, 'w'), indent=2)
print(f'✅ Finished')
