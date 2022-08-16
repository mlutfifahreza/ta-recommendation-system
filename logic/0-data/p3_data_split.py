import os, csv, time, sys
import random

# Template variables
n_playlist = int(sys.argv[1])
size_embed = int(sys.argv[2])
learn_rate = float(sys.argv[3])
n_epoch = int(sys.argv[4])
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\033[35m' + 'Process:' + '\033[0m'
path_root = os.getcwd()
path_pop = f'/data/model/pop/playlist:{n_playlist}'
path_word_sim = f'/data/model/word_sim/playlist:{n_playlist}'
path_cbow = f'/data/model/cbow/embed:{size_embed}-playlist:{n_playlist}-rate:{learn_rate}'
path_fcm = f'/data/model/cbow/embed:{size_embed}-playlist:{n_playlist}'

n_total = n_playlist
n_done = n_train = n_test = 0
r_train = 0.9
r_test = 0.1
n_total_train = n_total * r_train
n_total_test = n_total * r_test

def write_split_data(path, playlist):
    with open(path, 'a+', encoding = 'UTF8', newline = '') as f:
        csv.writer(f).writerow(playlist)

# Reading playlists.csv dataset
path_relative = '/data/data-all/playlists.csv'
path_train =  path_root + '/data/data-training/playlists.csv'
path_test = path_root + '/data/data-testing/playlists.csv'
with open(path_root + path_relative) as csv_file:
    # starting
    print(READING_FORMAT, path_relative)
    t_start = time.perf_counter()
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        # write header for each file
        if is_at_header:
            for path_w in [path_train, path_test]:
                with open(path_w, 'w', encoding = 'UTF8', newline = '') as f:
                    csv.writer(f).writerow(row)
            is_at_header = False
        else:
            x = random.random()
            if (x <= r_train and n_train < n_total_train): 
                write_split_data(path_train, row)
                n_train += 1
            elif (n_test < n_total_test): 
                write_split_data(path_test, row)
                n_test += 1
            else: 
                write_split_data(path_train, row)
                n_train += 1
            # Progress stats
            n_done += 1
            t_elapsed = time.perf_counter()-t_start
            t_remaining = (n_total-n_done)/n_done * t_elapsed
            print(f'\r🟡 Done: {n_done}/{n_total} '
                + f'Elapsed: {t_elapsed:.3f}s '
                + f'Est.: {t_remaining:.3f}s', end = ' ')
    # Finishing
    print(f'\r✅ Done: {n_done}/{n_total} - '
        + f'Elapsed: {t_elapsed:.3f}s'
        + ' '*20)

# Finishing
print('   - All Playlist :', n_done)
print('   - Training     :', n_train)
print('   - Testing      :', n_test)
