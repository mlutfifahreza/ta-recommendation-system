import os, csv, time, sys

# General Variables
READING_STRING = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_STRING = '\033[92m' + 'Export:' + '\033[0m'
root_path = os.getcwd()
PLAYLIST_TOTAL = int(sys.argv[1]) if (len(sys.argv) > 1) else 200000

# Reading track_count.csv dataset
track_count = {}
rel_path = '/data/data-training/track-count.csv'

with open(root_path + rel_path) as csv_file:
    # starting
    print(READING_STRING, rel_path)
    t_start = time.time()
    # read and process
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        track_count[row['track_id']] = int(row['count'])
    # Finished
    print(f'✅ Finished: {time.time() - t_start:.3f}s')

# Reading token_tracks.csv dataset
token_tracks = {} # key = token, value = list of [track_id, count]
rel_path = '/data/data-training/token-tracks.csv'
with open(root_path + rel_path) as csv_file:
    # starting
    print(READING_STRING, rel_path)
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
rel_path = '/data/data-training/token-50tracks.csv'
with open(root_path + rel_path, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, rel_path)
    t_start = time.time()
    writer = csv.writer(f)
    # write header
    header = ['token', '50tracks']
    writer.writerow(header)
    # write content
    for key, value in token_tracks.items():
        ids = []
        for v in value:
            ids.append(v[0]) # v[0] = track id
        writer.writerow([key] + ids)
    # Finished
    print(f'✅ Finished: {time.time() - t_start:.3f}s')

