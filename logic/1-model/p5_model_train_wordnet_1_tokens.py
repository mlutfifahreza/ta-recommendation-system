import os, csv, time, sys

# General Variables
READING_STRING = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_STRING = '\033[92m' + 'Export:' + '\033[0m'
root_path = os.getcwd()
token_tracks = {}
PLAYLIST_TOTAL = int(sys.argv[1]) if (len(sys.argv) > 1) else 200000

# Reading playlists.csv dataset
rel_path = '/data/data-training/playlists.csv'
with open(root_path + rel_path) as csv_file:
    # starting
    print(READING_STRING, rel_path)
    total_count = int(PLAYLIST_TOTAL * 0.9)
    processed_count = 0
    t_start = time.time()
    # read and process
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        title = row['title']
        track_ids = row['track_ids'].split()
        for token in title.split():
            # add track_ids without duplicate
            if token in token_tracks.keys(): 
                token_tracks[token] = list(set(token_tracks[token] + track_ids))
            else: token_tracks[token] = track_ids
        # progress stats
        processed_count += 1
        t_elapsed = time.time()-t_start
        t_remaining = (total_count-processed_count)/processed_count * t_elapsed
        print(f'\rProgress: {processed_count}/{total_count} '
            + f'Elapsed: {t_elapsed:.3f}s '
            + f'Remaining: {t_remaining:.3f}s', end = ' ')
    print(f'\n✅ Finished: {time.time() - t_start:.3f}s')

# Writing to token_tracks.csv
rel_path = '/data/data-training/token-tracks.csv'
with open(root_path + rel_path, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, rel_path)
    t_start = time.time()
    writer = csv.writer(f)
    # write header
    header = ['token','track_ids']
    writer.writerow(header)
    # write content
    for key, value in token_tracks.items():
        writer.writerow([key, ' '.join(value)])
    t_elapsed = '{:.2f}'.format(time.time()-t_start)
    print(f'✅ Finished: {time.time() - t_start:.3f}s')

# Finishing
print('ℹ️  Unique tokens:', len(token_tracks))