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

# Reading playlists.csv dataset
track_count = []
path_relative = '/data/data-training/playlists.csv'
track_count = {}
with open(path_root + path_relative) as csv_file:
    # starting
    print(READING_STRING, path_relative)
    t_start = time.perf_counter()
    # read and process
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        for id in row['track_ids'].split():
            if id in track_count: track_count[id] += 1
            else: track_count[id] = 1
    # Finished
    print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')

# Convert to list
track_count_list = []
for k,v in track_count.items():
    track_count_list.append([k,v])
# Sort with index 1: count value
track_count_list.sort(key=lambda row: (row[1]), reverse=True)

# Creating saving directory path
if not os.path.exists(path_root + path_pop):
    os.makedirs(path_root + path_pop)

# Writing to track_count.csv
path_relative = path_pop + '/track-count.csv'
with open(path_root + path_relative, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, path_relative)
    t_start = time.perf_counter()
    writer = csv.writer(f)
    # write header
    header = ['track_id', 'count']
    writer.writerow(header)
    # write content
    for item in track_count_list:
        writer.writerow(item)
    # finishing
    print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')

# Finishing
print('   - Tracks count :', len(track_count_list))
print('   - Max count    :', track_count_list[0][1])
print('   - Min count    :', track_count_list[-1][1])