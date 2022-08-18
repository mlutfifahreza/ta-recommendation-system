import os, csv, time, json

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'

# Parameters
params = json.load(open('parameters.json'))
n_playlist = params['n_playlist']
n_vocab = params['n_vocab']
n_data_train = params['n_data_train']
n_data_batch = params['n_data_batch']
size_embed = params['size_embed']
learn_rate = params['learn_rate']
n_epoch = params['n_epoch']

# Paths
path_pop = f'data/model/pop/playlist={n_playlist}'
path_word_sim = f'data/model/word_sim/playlist={n_playlist}'
path_vector = f'data/model/vector/embed={size_embed}-playlist={n_playlist}-rate={learn_rate}'
path_fcm = f'data/model/fcm/embed={size_embed}-playlist={n_playlist}'

# Creating saving directory path
if not os.path.exists(path_vector):
    os.makedirs(path_vector)

# Getting vocabularies: labels & neighbors
vocabs_index = {} # key is track_id, value is index
path_csv = path_pop + '/track-count.csv'
with open(path_csv) as csv_file:
    # starting
    print(READING_FORMAT, path_csv)
    t_start = time.perf_counter()
    # read and process
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        vocabs_index[row['track_id']] = None
    # finishing
    print(f'✅ {(time.perf_counter()-t_start):.3f}s')
# update parameters.json
n_vocab = len(vocabs_index)
print('n_vocab =', n_vocab)

# Get one hot encoding index + export
print(PROCESS_FORMAT, 'Get one hot encoding index')
path_csv = path_vector + '/track-one_hot_index.csv'
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
    # init
    print(EXPORT_FORMAT, path_csv)
    n_total = n_vocab
    n_done = 0
    t_start = time.perf_counter()
    writer = csv.writer(f)
    # write header
    header = ['track_id', 'one_hot_index']
    writer.writerow(header)
    # write content
    for i, key in enumerate(vocabs_index):
        vocabs_index[key] = i
        writer.writerow([key, i])
        # progress stats
        n_done += 1
        t_elapsed = time.perf_counter()-t_start
        t_remaining = (n_total-n_done) / n_done * t_elapsed
        print(f'\r🟡 Done: {n_done}/{n_total} '
            + f'Elapsed: {t_elapsed:.3f}s '
            + f'ETA: {t_remaining:.3f}s', end = ' ')
    # end
    print(f'\r✅ Done: {n_done}/{n_total} - '
        + f'Elapsed: {t_elapsed:.3f}s'
        + ' '*20)

# Getting data training :
def create_data_train_file(path_csv):
    # writing header
    print(EXPORT_FORMAT, path_csv)
    with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
        csv.writer(f).writerow(['input', 'target'])

def add_new_data(path_csv, new_input, new_target):
    with open(path_csv, 'a+', encoding = 'UTF8', newline = '') as f:
        csv.writer(f).writerow([new_input, new_target])

# (new) set 2 closest as neighbors
print(PROCESS_FORMAT, 'Generating CBOW data train')
k = 1
path_csv = 'data/data-training/playlists.csv'
with open(path_csv) as csv_file:
    # init
    print(READING_FORMAT, path_csv)
    n_done = 0 
    n_data_train = 0
    n_total = int(n_playlist * 0.9)
    t_start = time.perf_counter()
    t_elapsed = 0
    # init export file
    path_csv_export = path_vector + '/train=input-target.csv'
    create_data_train_file(path_csv_export)
    # read and process
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        track_ids = row['track_ids'].split()
        n_track = len(track_ids)
        for i in range(n_track):
            # for j in range(i-k, i+k+1):
            #     # label -> target
            #     new_target = f'{vocabs_index[track_ids[i]]}'
            #     if (0 <= j < n_track):
            #         # label's neighbor -> inputs (one hot)
            #         new_input = f'{vocabs_index[track_ids[j]]}'
            #         add_new_data(path_csv_export, new_input, new_target)
            #         n_data_train += 1
            a,b = i-1, i+1
            if (0 <= a < n_track) and (0 <= b < n_track):
                # label -> target
                new_target = f'{vocabs_index[track_ids[i]]}'
                # label's neighbor -> inputs (one hot)
                new_input = f'{vocabs_index[track_ids[a]]} {vocabs_index[track_ids[b]]}'
                add_new_data(path_csv_export, new_input, new_target)
                n_data_train += 1
        # Progress stats
        n_done += 1
        t_elapsed = time.perf_counter()-t_start
        t_remaining = (n_total-n_done)/n_done * t_elapsed
        print(f'\r🟡 Done: {(n_done*100/n_total):.2f}% '
            + f'Elapsed: {t_elapsed:.3f}s '
            + f'ETA: {t_remaining:.3f}s', end = ' ')
    # end
    print(f'\r✅ Done: 100% '
        + f'Elapsed: {t_elapsed:.3f}s'
        + ' '*20)

# update parameters values
params['n_vocab'] = n_vocab
params['n_data_train'] = n_data_train
json.dump(params, open('parameters.json', 'w'), indent=4)