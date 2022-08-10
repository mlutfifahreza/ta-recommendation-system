import os, time, csv, sys
import numpy as np
import matplotlib.pyplot as plt

# From input arguments
n_playlist = int(sys.argv[1])
size_embed = int(sys.argv[2])
learn_rate = float(sys.argv[3])
n_epoch = int(sys.argv[4])
div_cluster = int(sys.argv[5])

# General Variables
READING_STRING = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_STRING = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_STRING = '\033[35m' + 'Process:' + '\033[0m'
path_root = os.getcwd()
path_pop = f'/data/model/pop/playlist:{n_playlist}'
path_word_sim = f'/data/model/word_sim/playlist:{n_playlist}'
path_cbow = f'/data/model/cbow/embed:{size_embed}-playlist:{n_playlist}-rate:{learn_rate}'
path_fcm = f'/data/model/fcm/embed:{size_embed}-playlist:{n_playlist}'

def square_dist(x, y):
    return np.sum(np.square(x - y))

def get_centroids(weights, inputs, p = 1.75):
    n_dimension = inputs.shape[1]
    centroids = np.zeros((n_clusters, n_dimension))
    for k in range(n_clusters):
        denom = 0
        for d in range(n_dimension):
            num = denom = 0
            for i in range(n_data):
                num += weights[i,k] * inputs[i,d]
                denom += weights[i,k]
            centroids[k,d] = num/denom
    return centroids

def update_weights(weights, inputs, centroids, p = 1.75):
    n_dimension = inputs.shape[1]
    new_weights = np.copy(weights)
    for k in range(n_clusters):
        for i in range(n_data):
            num = 0
            for d in range(n_dimension):
                num += square_dist(inputs[i,d], centroids[k,d])
            num = num ** (-1/(p-1))
            denom = 0
            for c in range(n_clusters):
                sub_denom = 0
                for d in range(n_dimension):
                    sub_denom += square_dist(inputs[i,d], centroids[c,d])
                denom += sub_denom ** (-1/(p-1))
            new_weights[i,k] = num/denom
    return new_weights

def SSE(weights, inputs, centroids, p = 1.75):
    sse = 0
    for k in range(n_clusters):
        for i in range(n_data):
            sse += (weights[i,k] ** p) * square_dist(inputs[i], centroids[k])
    return sse

# FCM: init inputs
# Getting embedding as inputs
inputs = []
path_relative =  path_cbow + '/embeddings.csv'
with open(path_root + path_relative) as csv_file:
    # starting
    print(READING_STRING, path_relative)
    t_start = time.perf_counter()
    # read and process
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        embed = [float(x) for x in row['vector'].split()]
        inputs.append(np.array(embed))
    # finishing
    inputs = np.array(inputs)
    print(f'✅ Finished: {time.perf_counter()-t_start:.3f}s')

# FCM: variables update
n_data = inputs.shape[0]
n_clusters = n_data//div_cluster
fuzzy_param = 1.8
max_iter = 20
threshold = 1e-6

# FCM: init weights, centroids
weights = np.random.rand(n_data, n_clusters)
centroids = None
# FCM: learn
print(PROCESS_STRING, 'FCM Learning')
print(f'Parameters:'
    + f'\n  data shape  = {inputs.shape} '
    + f'\n  fuzzy param = {fuzzy_param} '
    + f'\n  threshold   = {threshold} '
    + f'\n  n clusters  = {n_clusters}')
log_sse = []
last_sse = float('inf')
for i in range(max_iter):
    # For progress checking
    t_start = time.perf_counter()
    print(f'Iteration: {i+1}/{max_iter} Status: computing...', end ='\r')
    # learn
    new_centroids = get_centroids(weights, inputs, fuzzy_param)
    new_weights = update_weights(weights, inputs, new_centroids, fuzzy_param)
    new_sse = SSE(new_weights, inputs, new_centroids, fuzzy_param)
    sse_diff = last_sse - new_sse
    if (sse_diff) > threshold:
        weights = new_weights
        centroids = new_centroids
        last_sse = new_sse
        log_sse.append(new_sse)
        # progress stats
        t_elapsed = time.perf_counter()-t_start
        print(f'\rIteration: {i+1}/{max_iter} Status: - '
            + f'Elapsed = {t_elapsed:.3f}s E = {new_sse} dE = {sse_diff}')
    elif sse_diff > 0:
        weights = new_weights
        centroids = new_centroids
        last_sse = new_sse
        log_sse.append(new_sse)
        # progress stats
        t_elapsed = time.perf_counter()-t_start
        print(f'\rIteration: {i+1}/{max_iter} Status: - '
            + f'Elapsed = {t_elapsed:.3f}s E = {new_sse} dE = {sse_diff}'
            + f'\nStopping: 0 < change of error < threshold')
        break
    else:
        print(f'\tIteration: {i+1}/{max_iter} Status: - '
            + f'Stopping: change of error < 0')
        break

# Creating saving directory path
if not os.path.exists(path_root + path_fcm):
    os.makedirs(path_root + path_fcm)

# Save learning logs
print('sse =')
for sse in log_sse:
    print(f'  {sse}')
plt.plot(list(range(1,len(log_sse)+1)), log_sse)
plt.ylabel('Sum of squared error (SSE)')
plt.xlabel('Iteration')
plt.title('FCM - Error Learning Logs')
path_save = path_root + path_fcm + '/sse_loss.png'
plt.savefig(
    path_save,
    bbox_inches='tight')
os.system('open ' + f'{path_save}'.replace(' ','\ '))

# Save track-cluster
header =  ['track_index', 'cluster_memval']
# clusters_10 = '{cluster_index}:{mem_value}'
path_relative = path_fcm + '/track-cluster.csv'
with open(path_root + path_relative, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, path_relative)
    t_start = time.perf_counter()
    writer = csv.writer(f)
    # write header
    writer.writerow(header)
    # write content
    for i in range(n_data):
        memvals = []
        for j in range(n_clusters):
            memvals.append((j, weights[i,j]))
        memvals = np.array(
            memvals,
            dtype=[('cluster_index', np.int32), ('memval', np.float32)])
        memvals[::-1].sort(order='memval')
        memvals.resize(10)
        memvals = [f'{index}:{memval}' for index, memval in memvals]
        writer.writerow([j, ' '.join(memvals)])
    # finishing
    print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')


# Save cluster-100tracks
header =  ['cluster_index', 'track_100']
# track_100 = '{index}:{mem_value}'
path_relative = path_fcm + '/cluster-100tracks.csv'
with open(path_root + path_relative, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, path_relative)
    t_start = time.perf_counter()
    writer = csv.writer(f)
    # write header
    writer.writerow(header)
    # write content
    for j in range(n_clusters):
        memvals = []
        for i in range(n_data):
            memvals.append((i, weights[i,j]))
        memvals = np.array(
            memvals, 
            dtype=[('track_index', np.int32), ('memval', np.float32)])
        memvals[::-1].sort(order='memval')
        memvals.resize(100)
        memvals = [f'{index}:{memval}' for index, memval in memvals]
        writer.writerow([j, ' '.join(memvals)])
    # finishing
    print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')

# Save weights
path_relative = path_fcm + '/weights.csv'
with open(path_root + path_relative, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, path_relative)
    t_start = time.perf_counter()
    writer = csv.writer(f)
    # write content
    for w in weights:
        writer.writerow(w)
    # finishing
    print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')

# Save sorted weights
path_relative = path_fcm + '/sorted_weights.csv'
with open(path_root + path_relative, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, path_relative)
    t_start = time.perf_counter()
    writer = csv.writer(f)
    # write content
    for w in weights:
        sorted_weights = np.sort(w)
        writer.writerow(sorted_weights)
    # finishing
    print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')