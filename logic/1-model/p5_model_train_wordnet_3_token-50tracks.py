import os, csv, time, sys

# From input arguments
n_playlist = int(sys.argv[1])
size_embed = int(sys.argv[2])
learn_rate = float(sys.argv[3])
n_epoch = int(sys.argv[4])

# General Variables
READING_STRING = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_STRING = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_STRING = '\033[35m' + 'Process:' + '\033[0m'
path_root = os.getcwd()
path_pop = f'/data/model/pop/playlist:{n_playlist}'
path_word_sim = f'/data/model/word_sim/playlist:{n_playlist}'
path_cbow = f'/data/model/cbow/embed:{size_embed}-playlist:{n_playlist}-rate:{learn_rate}'
path_fcm = f'/data/model/cbow/embed:{size_embed}-playlist:{n_playlist}'

# Reading track_count.csv dataset
track_count = {}
path_relative = path_pop + '/track-count.csv'
with open(path_root + path_relative) as csv_file:
    # starting
    print(READING_STRING, path_relative)
    t_start = time.time()
    # read and process
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        track_count[row['track_id']] = int(row['count'])
    # Finished
    print(f'✅ Finished: {time.time() - t_start:.3f}s')

# Reading token_tracks.csv dataset
token_tracks = {} # key = token, value = list of [track_id, count]
path_relative = path_word_sim + '/token-tracks.csv'
with open(path_root + path_relative) as csv_file:
    # starting
    print(READING_STRING, path_relative)
    n_done = 0
    t_start = time.time()
    # read and process
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        token = row['token']
        token_tracks[token] = []
        # add track_id and count for each track in token
        for id in row['track_ids'].split():
            id_count = track_count[id]
            token_tracks[token].append([id, id_count])
        # sort the tracks by count
        token_tracks[token].sort(key=lambda idx: (idx[1]), reverse=True)
        # trim to first 50 only
        token_tracks[token] = token_tracks[token][:50]
    # finishing
    print(f'✅ Finished: {time.time() - t_start:.3f}s')

# Writing to token-50tracks.csv
path_relative = path_word_sim + '/token-50tracks.csv'
with open(path_root + path_relative, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, path_relative)
    t_start = time.time()
    writer = csv.writer(f)
    # write header
    header = ['token', '50tracks']
    writer.writerow(header)
    # write content
    for token, track_count in token_tracks.items():
        track_ids = ''
        for value in track_count:
            track_ids += value[0] + ' '
        writer.writerow([token, track_ids])
    # Finished
    print(f'✅ Finished: {time.time() - t_start:.3f}s')

