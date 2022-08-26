import os, time, csv, sys, json
import numpy as np
import matplotlib.pyplot as plt

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# Parameters
params = json.load(open('parameters.json'))
n_playlist = params['n_playlist']
size_embed = params['size_embed']
n_epoch = params['n_epoch']
div_cluster = params['div_cluster']
iter_max = params['iter_max']
iter_patience = params['iter_patience']
change_threshold = params['change_threshold']
fuzzy_param = params['fuzzy_param']

# Paths
path_general = f'data/general'
path_data = f'data/data_all/playlist={n_playlist}'
path_data_train = f'data/data_train/playlist={n_playlist}'
path_data_test = f'data/data_test/playlist={n_playlist}'
path_pop = f'data/model/pop/playlist={n_playlist}'
path_word_sim = f'data/model/word_sim/playlist={n_playlist}'
path_vector = f'data/model/vector/playlist={n_playlist}-embed={size_embed}'
path_fcm = f'data/model/fcm/playlist={n_playlist}-embed={size_embed}'

def square_dist(x, y):
  return np.sum(np.square(x - y))

def get_centroids(weights, inputs, p = 1.75):
  n_dimension = inputs.shape[1]
  centroids = np.zeros((n_clusters, n_dimension))
  # starting
  print(SUBPROCESS_FORMAT, "get_centroids")
  n_total = n_clusters * n_dimension
  n_done = 0
  t_start = time.perf_counter()

  for k in range(n_clusters):
    denom = 0
    for d in range(n_dimension):
      num = denom = 0
      for i in range(n_data):
        num += weights[i,k] * inputs[i,d]
        denom += weights[i,k]
      centroids[k,d] = num/denom
      # progress stats
      n_done = (k * n_dimension) + d + 1
      t_elapsed = time.perf_counter()-t_start
      t_remaining = (n_total-n_done) / n_done * t_elapsed
      print(f'\r🟡 Progress: {n_done}/{n_total} '
        + f'Elapsed: {t_elapsed:.3f}s '
        + f'ETA: {t_remaining:.3f}s', end = '')
  print(f'\r✅ Done: {n_done}/{n_total} - '
    + f'Elapsed: {t_elapsed:.3f}s'
    + ' '*20)
  return centroids

def update_weights(weights, inputs, centroids, p = 1.75):
  n_dimension = inputs.shape[1]
  new_weights = np.copy(weights)
  # starting
  print(SUBPROCESS_FORMAT, "update_weights")
  n_total = n_clusters * n_data
  n_done = 0
  t_start = time.perf_counter()
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
      # progress stats
      n_done = k * n_data + i + 1
      t_elapsed = time.perf_counter()-t_start
      t_remaining = (n_total-n_done) / n_done * t_elapsed
      print(f'\r🟡 Progress: {n_done}/{n_total} '
        + f'Elapsed: {t_elapsed:.3f}s '
        + f'ETA: {t_remaining:.3f}s', end = '')
  print(f'\r✅ Done: {n_done}/{n_total} - '
    + f'Elapsed: {t_elapsed:.3f}s'
    + ' '*20)
  return new_weights

def SSE(weights, inputs, centroids, p = 1.75):
  # starting
  print(SUBPROCESS_FORMAT, "SSE")
  n_total = n_clusters * n_data
  n_done = 0
  t_start = time.perf_counter()

  SSE = 0
  for k in range(n_clusters):
    for i in range(n_data):
      SSE += (weights[i,k] ** p) * square_dist(inputs[i], centroids[k])
  
  print(f'✅ Finished {(time.perf_counter()-t_start):.3f}s')
  return SSE

# FCM: init inputs
# Getting embedding as inputs
inputs = []
track_index = []
path_csv =  path_vector + '/track-vector.csv'
with open(path_csv) as csv_file:
  # starting
  print(READING_FORMAT, path_csv)
  t_start = time.perf_counter()
  # read and process
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    embed = [float(x) for x in row['vector'].split()]
    inputs.append(np.array(embed))
    track_index.append(row['track'])
  # finishing
  inputs = np.array(inputs)
  print(f'✅ Finished: {time.perf_counter()-t_start:.3f}s')

# FCM: variables update
n_data = inputs.shape[0]
n_clusters = n_data//div_cluster

# FCM: learn
print(PROCESS_FORMAT, 'FCM Learning')
print('- data shape       =', inputs.shape)
print('- n_clusters       =', n_clusters)
print('- fuzzy param      =', fuzzy_param)
print('- change_threshold =', change_threshold)
print('- iter_max         =', iter_max)
# FCM: init weights, centroids
weights = np.random.rand(n_data, n_clusters)
centroids = None
log_SSE = []
log_dSSE = []
last_SSE = float('inf')
for i in range(iter_max):
  # For progress checking
  t_start = time.perf_counter()
  print(PROCESS_FORMAT, f'Iteration {i+1}/{iter_max}')
  # learn
  new_centroids = get_centroids(weights, inputs, fuzzy_param)
  new_weights = update_weights(weights, inputs, new_centroids, fuzzy_param)
  new_SSE = SSE(new_weights, inputs, new_centroids, fuzzy_param)
  # learning check
  SSE_diff = last_SSE - new_SSE
  log_dSSE.append(SSE_diff)
  if (i < iter_patience):
    weights, centroids, last_SSE = new_weights, new_centroids, new_SSE
    log_SSE.append(new_SSE)
    # progress stats
    t_elapsed = time.perf_counter()-t_start
    print(f'Elapsed = {t_elapsed:.3f}s SSE = {new_SSE} dSSE = {SSE_diff}')
  else:
    # more than threshold
    if (SSE_diff) > change_threshold:
      weights, centroids, last_SSE = new_weights, new_centroids, new_SSE
      log_SSE.append(new_SSE)
      # progress stats
      t_elapsed = time.perf_counter()-t_start
      print(f'Elapsed = {t_elapsed:.3f}s SSE = {new_SSE} dSSE = {SSE_diff}')
    # less than threshold but non negative
    elif SSE_diff > 0:
      weights, centroids, last_SSE = new_weights, new_centroids, new_SSE
      log_SSE.append(new_SSE)
      # progress stats
      t_elapsed = time.perf_counter()-t_start
      print(f'Elapsed = {t_elapsed:.3f}s SSE = {new_SSE} dSSE = {SSE_diff}')
      print(f'Stopping: 0 < dSSE < change_threshold')
      break
    # negative diff
    else:
      print(f'Stopping: dSSE < 0')
      break

# Save learning logs
print()
print('SSE =', log_SSE)
plt.plot(list(range(1,len(log_SSE)+1)), log_SSE)
plt.ylabel('Sum of squared error (SSE)')
plt.xlabel('Iteration')
plt.title('FCM - Error Learning Logs')
path_save = path_fcm + '/SSE_loss.png'
plt.savefig(
  path_save,
  bbox_inches='tight')
os.system('open ' + f'{path_save}'.replace(' ','\ '))

# Save track-index
header =  ['track', 'index']
path_csv = path_fcm + '/track-index.csv'
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
  # starting
  print(EXPORT_FORMAT, path_csv)
  t_start = time.perf_counter()
  writer = csv.writer(f)
  # write header
  writer.writerow(header)
  # write content
  for i, v in enumerate(track_index):
    writer.writerow([v, i])
  # finishing
  print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')

# Save track-cluster
header =  ['track_index', '20cluster_memval']
# clusters_20 = '{cluster_index}:{mem_value}'
path_csv = path_fcm + '/track-20cluster.csv'
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
  # starting
  print(EXPORT_FORMAT, path_csv)
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
    memvals.resize(20)
    memvals = [f'{index}:{memval}' for index, memval in memvals]
    writer.writerow([j, ' '.join(memvals)])
  # finishing
  print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')


# Save cluster-100tracks
header =  ['cluster_index', '100track']
# 100track = '{index}:{mem_value}'
path_csv = path_fcm + '/cluster-100tracks.csv'
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
  # starting
  print(EXPORT_FORMAT, path_csv)
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
path_csv = path_fcm + '/weights.csv'
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
  # starting
  print(EXPORT_FORMAT, path_csv)
  t_start = time.perf_counter()
  writer = csv.writer(f)
  # write content
  for w in weights:
    writer.writerow(w)
  # finishing
  print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')

# Save sorted weights
path_csv = path_fcm + '/sorted_weights(test_only).csv'
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
  # starting
  print(EXPORT_FORMAT, path_csv)
  t_start = time.perf_counter()
  writer = csv.writer(f)
  # write content
  for w in weights:
    sorted_weights = np.sort(w)
    writer.writerow(sorted_weights)
  # finishing
  print(f'✅ Finished: {time.perf_counter() - t_start:.3f}s')

# update parameters values
params['vars'][f'{n_playlist}']['n_clusters'] = n_clusters
params['vars'][f'{n_playlist}']['log_SSE'] = log_SSE
params['vars'][f'{n_playlist}']['log_dSSE'] = log_dSSE
json.dump(params, open('parameters.json', 'w'), indent=2)