import os, csv, time, random, sys
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense, InputLayer, Embedding, ReLU
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import plot_model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.metrics import BinaryAccuracy

# Template variables
n_playlist = int(sys.argv[1])
size_embed = int(sys.argv[2])
learn_rate = float(sys.argv[3])
n_epoch = int(sys.argv[4])
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
path_root = os.getcwd()
path_pop = f'/data/model/pop/playlist={n_playlist}'
path_word_sim = f'/data/model/word_sim/playlist={n_playlist}'
path_w2v = f'/data/model/w2v/embed:{size_embed}-playlist={n_playlist}-rate:{learn_rate}'
path_fcm = f'/data/model/w2v/embed:{size_embed}-playlist={n_playlist}'

# Creating saving directory path
if not os.path.exists(path_w2v):
  os.makedirs(path_w2v)

# Getting labels & neighbors
vocabs = {} # key is track_id, value is index
path_csv = path_pop + '/track-count.csv'
with open(path_csv) as csv_file:
  # starting
  print(READING_FORMAT, path_csv)
  t_start = time.perf_counter()
  # read and process
  csv_reader = csv.DictReader(csv_file)
  i = 0
  for row in csv_reader:
    vocabs[row['track_id']] = i
    i += 1
  # finishing
  print(f'✅ {(time.perf_counter()-t_start):.3f}s')

n_vocab = len(vocabs)
print('n_vocab =',n_vocab)

# Getting data training :
# (new) set 4 closests as neighbors
# 2 left, 2 right
print(PROCESS_FORMAT, 'Getting data training')
k = 2
inputs, targets = [], []
path_csv = '/data/data-training/playlists.csv'
with open(path_csv) as csv_file:
  # starting
  print(READING_FORMAT, path_csv)
  t_start = time.perf_counter()
  # read and process
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    track_ids = row['track_ids'].split()
    n_track = len(track_ids)
    for i in range(n_track):
      # (a,b) is index helper to find neighbors
      for a in range(i-k, i+1+k):
        if a == i: 
          continue
        for b in range(a+1, i+1+k):
          if b == i: 
            continue
          elif (a >= 0 and b < n_track):
            # label -> target
            new_target = np.array(
              vocabs[track_ids[i]],
              dtype='i'
            )
            targets.append(new_target)
            # # label's neighbor -> inputs
            # new_input = np.array(
            #   [vocabs[track_ids[a]], vocabs[track_ids[b]]],
            #   dtype='i'
            # )
            # label's neighbor -> inputs (one hot)
            new_input = np.concatenate(
              ([vocabs[track_ids[a]], vocabs[track_ids[b]]]),
              dtype='i'
            )
            inputs.append(new_input)
  # finishing
  print(f'✅ {(time.perf_counter()-t_start):.3f}s')
n_data_train = len(inputs)

# Shuffle data training
print('   - n_vocab =', n_vocab)
print('   - n_data_train =', n_data_train)
print(PROCESS_FORMAT, 'Shuffle data training')
t_start = time.perf_counter()
for i in range(100 * n_data_train):
  ran_1 = int(random.random()*n_data_train)
  ran_2 = int(random.random()*n_data_train)
  # swapping index: ran_1 <-> ran_2 
  inputs[ran_1], inputs[ran_2] = inputs[ran_2], inputs[ran_1]
  targets[ran_1], targets[ran_2] = targets[ran_2], targets[ran_1]
# finishing
print(f'✅ {(time.perf_counter()-t_start):.3f}s')

# Model CBOW
# init
print(PROCESS_FORMAT, 'Model CBOW Learning')
inputs = np.array(inputs)
targets = np.array(targets)
cb_early_stop = EarlyStopping(
  monitor = 'val_loss',
  min_delta = 1e-6,
  patience = 5,
  verbose = 0,
  mode = 'auto',
)
model_embedding = Sequential([
  InputLayer(input_shape=(inputs.shape[1]), name='input'),
  Dense(size_embed, activation='sigmoid', name='hidden'),
  Dense(targets.shape[1], activation='sigmoid', name='output')
])
# new model : using embedding layer
# model_embedding = Sequential([
#   InputLayer(input_shape=(inputs.shape[1]), name='input'),
#   Dense(size_embed, activation='sigmoid', name='hidden'),
#   Dense(targets.shape[1], activation='sigmoid', name='output')
# ])
metric_name = 'binary_accuracy'
metric_model = BinaryAccuracy(threshold=0.8)
model_embedding.compile(
  Adam(learn_rate),
  loss = 'mae',
  metrics = [metric_model]
)
for layer in model_embedding.layers:
  print(f'layer = {layer}, shape = {len(layer.get_weights())} x {len(layer.get_weights()[0])}')
# Save model architecture
plot_model(
  model_embedding,
  to_file = path_w2v + '/w2v_arch-embedding.png',
  show_shapes = True,
  show_dtype = True,
  expand_nested = True,
  show_layer_names = True,
  show_layer_activations = True
)
print(f'✅ Architecture set')
print('   - Inputs shape  =', inputs.shape)
print('   - Targets shape =', targets.shape)
print('   - Learning rate =', learn_rate)
print('   - Num of epoch  =', n_epoch)
# learn
history = model_embedding.fit(
  x = inputs,
  y = targets,
  epochs = n_epoch,
  verbose = 1,
  validation_split= 1/9,
  callbacks=[cb_early_stop])
print(f'✅ Learning done')

for key in history.history:
  print(f'key = {key}')

# Save history: binary_accuracy - train, test
plt.clf()
plt.plot(history.history[metric_name])
plt.plot(history.history['val_' + metric_name])
plt.title(f'size embed:{size_embed}, playlists:{n_playlist}')
plt.ylabel(metric_name)
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
path_save = path_w2v + '/' + metric_name + '.png'
print(EXPORT_FORMAT, path_save)
plt.savefig(path_save, bbox_inches='tight')
os.system('open ' + f'{path_save}'.replace(' ','\ '))

# # Save history: binary_accuracy - train
# plt.clf()
# plt.plot(history.history[metric_name])
# plt.title(f'size embed:{size_embed}, playlists:{n_playlist}')
# plt.ylabel(metric_name)
# plt.xlabel('epoch')
# plt.legend(['train'], loc='upper left')
# path_save = path_w2v + '/accuracy-train.png'
# print(EXPORT_FORMAT, path_save)
# plt.savefig(path_save, bbox_inches='tight')
# os.system('open ' + f'{path_save}'.replace(' ','\ '))

# # Save history: binary_accuracy - test
# plt.clf()
# plt.plot(history.history['val_' + metric_name])
# plt.title(f'size embed:{size_embed}, playlists:{n_playlist}')
# plt.ylabel(metric_name)
# plt.xlabel('epoch')
# plt.legend(['test'], loc='upper left')
# path_save = path_w2v + '/accuracy-test.png'
# print(EXPORT_FORMAT, path_save)
# plt.savefig(path_save, bbox_inches='tight')
# os.system('open ' + f'{path_save}'.replace(' ','\ '))

# Save history: loss
plt.clf()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title(f'model loss size embed:{size_embed}, playlists:{n_playlist}')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
path_save = path_w2v + '/loss.png'
print(EXPORT_FORMAT, path_save)
plt.savefig(path_save, bbox_inches='tight')
os.system('open ' + f'{path_save}'.replace(' ','\ '))

# Save history: DONE
print(f'✅ Model history saved')

# Extract embeddings
path_csv = path_w2v + '/embeddings.csv'
with open(path_csv, 'w', encoding = 'UTF8', newline = '') as f:
  # starting
  print(EXPORT_FORMAT, path_csv)
  n_total = n_vocab
  n_done = 0
  t_start = time.perf_counter()
  writer = csv.writer(f)
  # write header
  header = ['one_hot_index', 'vector']
  writer.writerow(header)
  # write content
  for i in range(n_vocab):
    embed = []
    for j in range(size_embed):
      embed.append(model_embedding.layers[1].get_weights()[0][j][i])
    embed = ' '.join([str(e) for e in embed])
    writer.writerow([i, embed])
    # progress stats
    n_done += 1
    t_elapsed = time.perf_counter()-t_start
    t_remaining = (n_total-n_done) / n_done * t_elapsed
    print(f'\r🟡 Done: {n_done}/{n_total} '
      + f'Elapsed: {t_elapsed:.3f}s '
      + f'ETA: {t_remaining:.3f}s', end = ' ')
  # finishing
  print()
  print(f'✅ {(time.perf_counter()-t_start):.3f}s')