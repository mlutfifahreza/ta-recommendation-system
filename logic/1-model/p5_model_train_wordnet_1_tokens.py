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

# Get token - tracks relationship
token_tracks = {}
path_relative = '/data/data-training/playlists.csv'
with open(path_root + path_relative) as csv_file:
    # starting
    print(READING_STRING, path_relative)
    n_total = int(n_playlist * 0.9)
    n_done = 0
    t_start = time.time()
    # read and process
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        title = row['title']
        track_ids = row['track_ids'].split()
        for token in title.split():
            # add track_ids without duplicate
            if token in token_tracks.keys(): 
                token_tracks[token] = list(set(token_tracks[token] + track_ids))
            else: token_tracks[token] = track_ids
        # progress stats
        n_done += 1
        t_elapsed = time.time()-t_start
        t_remaining = (n_total-n_done)/n_done * t_elapsed
        print(f'\rProgress: {n_done}/{n_total} '
            + f'Elapsed: {t_elapsed:.3f}s '
            + f'Remaining: {t_remaining:.3f}s', end = ' ')
    print(f'\n✅ Finished: {time.time() - t_start:.3f}s')

# Creating saving directory path
path_dir = f'/data/model/word_sim/playlist:{n_playlist}'
if not os.path.exists(path_root + path_dir):
    os.makedirs(path_root + path_dir)

# Writing to token_tracks.csv
path_relative = path_dir + '/token-tracks.csv'
with open(path_root + path_relative, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, path_relative)
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