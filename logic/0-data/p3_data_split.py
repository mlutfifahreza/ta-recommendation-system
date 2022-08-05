import os, csv, time, sys
import random

# General Variables
READING_STRING = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_STRING = '\033[92m' + 'Export:' + '\033[0m'
TIME_START = time.time()
root_path = os.getcwd()

n_total = int(sys.argv[1]) if (len(sys.argv) > 1) else 200000
n_done = n_train = n_test = 0
r_train = 0.9
r_test = 0.1
n_total_train = n_total * r_train
n_total_test = n_total * r_test

path_train =  root_path + '/data/data-training/playlists.csv'
path_test = root_path + '/data/data-testing/playlists.csv'

def write_split_data(path, playlist):
    with open(path, 'a+', encoding = 'UTF8', newline = '') as f:
        csv.writer(f).writerow(playlist)

# Reading playlists.csv dataset
rel_path = '/data/data-all/playlists.csv'

with open(root_path + rel_path) as csv_file:
    # starting
    print(READING_STRING, rel_path)
    t_start = time.time()
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
            n_done += 1
            # Progress stats
            t_elapsed = time.time()-t_start
            t_remaining = (n_total-n_done)/n_done * t_elapsed
            print(f'\rProgress: {n_done}/{n_total} '
                + f'Elapsed: {t_elapsed:.3f}s '
                + f'Remaining: {t_remaining:.3f}s', end = ' ')
    # Finishing
    print()
    print(f'✅ Finished {time.time()-t_start:.3f}s')

# Finishing
print('ℹ️  All Playlist :', n_done)
print('ℹ️  Training     :', n_train)
print('ℹ️  Testing      :', n_test)
