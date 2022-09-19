import os, json, csv, time, sys
from operator import itemgetter
import d2_text_preprocess as text_preprocess

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# General Variables
params = json.load(open('parameters.json'))
n_playlist = params['n_playlist']
path_general = f'data/general'
path_data_all = f'data/data_all/playlist={n_playlist}'
path_data_train = f'data/data_train/playlist={n_playlist}'
path_data_valid = f'data/data_valid/playlist={n_playlist}'
path_data_test = f'data/data_test/playlist={n_playlist}'
# # # # # # # # # # # # # # # # # # # # # #


# Prepare characters mapping
characters_mapping = {}
with open(path_general + '/characters-mapping.csv') as csv_file:
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    characters_mapping[row['char']] = row['map']

# Prepare mpd file names
mpd_file_names = []
n_mpd_file = 1000 # number of files inside mpd data
n_mpd_file_playlist = 1000 # count of playlist inside each file
for i in range(n_mpd_file):
  start = i*n_mpd_file_playlist
  end = start+(n_mpd_file_playlist-1)
  mpd_file_names.append(f'mpd.slice.{start}-{end}.json')

# Read all mpd files -> create playlists.csv
print(PROCESS_FORMAT, f'Selection of {n_playlist} playlists')
mpd_path = 'data/mpd/spotify_million_playlist_dataset/data/'
path_csv = path_data_all + '/playlists_all.csv'
tracks = {}
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
  # starting
  n_done = 0
  n_total = n_playlist
  t_start = time.perf_counter()
  print(EXPORT_FORMAT, path_csv)
  writer = csv.writer(f)
  # write header
  header = ['playlist_id','title','track_ids']
  writer.writerow(header)
  # read from mpd -> write content
  for i in range(n_mpd_file):
    opened_file = open(mpd_path+mpd_file_names[i])
    playlists_bacth_i = json.load(opened_file)['playlists']
    # scanning each playlist
    for playlist in playlists_bacth_i:
      if (n_done == n_total): break
      # validate condition -> write
      if (
        playlist['num_tracks'] >= 51 
        and playlist['num_tracks'] <= 100 
        and playlist['num_tracks'] == len(playlist['tracks'])
      ):
        track_ids = ''
        for track in playlist['tracks']:
          track_id = track['track_uri'].replace('spotify:track:','')
          track_name = track['track_name']
          artist_id = track['artist_uri'].replace('spotify:artist:','')
          artist_name = track['artist_name']
          track_ids += track_id + ' '
          if track_id in tracks: continue
          else:
            tracks[track_id] = {
              'track_id': track_id,
              'track_name': track_name,
              'artist_id': artist_id,
              'artist_name': artist_name,
            }
        writer.writerow([
          playlist['pid'],
          text_preprocess.clean(
            playlist['name'], characters_mapping),
          track_ids
        ])
        # progress stats
        n_done += 1
        t_elapsed = time.perf_counter()-t_start
        t_remaining = (n_total-n_done)/n_done * t_elapsed
        print(f'\r🟡 {n_done}/{n_total} '
          + f'Elapsed: {t_elapsed:.3f}s '
          + f'ETA: {t_remaining:.3f}s', end = ' ')
    # break condition
    if (n_done == n_total): break
  print(f'\r✅ {n_done}/{n_total} - '
    + f'Elapsed: {t_elapsed:.3f}s'
    + ' '*40)

# Writing tracks.csv sort by id
path_csv = path_data_all + '/track_detail_all.csv'
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
  print(EXPORT_FORMAT, path_csv)
  writer = csv.writer(f)
  t_start = time.perf_counter()
  header = ['track_id','track_name','artist_id','artist_name']
  writer.writerow(header)
  # returns list of sorted track detail
  tracks_sorted = sorted(tracks.values(), key=itemgetter('track_id'))
  for track in tracks_sorted:
    writer.writerow([
      track['track_id'],
      track['track_name'],
      track['artist_id'],
      track['artist_name'],
    ])
  print(f'✅ Finished: {time.perf_counter()-t_start:.3f}s')

# Finishing
print('   - Unique tracks:', len(tracks))