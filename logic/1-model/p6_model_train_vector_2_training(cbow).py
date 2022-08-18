import os, csv, time, random, json, gc
import numpy as np
import matplotlib.pyplot as plt
from math import ceil
from tensorflow.keras.layers import Dense, InputLayer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import plot_model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.metrics import BinaryAccuracy

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

# One hot function
def get_one_hot(index):
  result = np.zeros(n_vocab, dtype='i')
  result[index] = 1
  return result

# Getting data training :
def get_train_data(idx_min, idx_max):
  idx_max = min(idx_max, n_data_train-1)
  inputs, targets = [], []
  path_csv = path_vector + '/train=input-target.csv'
  with open(path_csv) as csv_file:
    # init progress check
    n_total = idx_max - idx_min + 1
    n_done = 0
    counter = 0
    t_start = time.perf_counter()
    t_elapsed = 0
    # init csv
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
      if counter > idx_max:
        break
      elif idx_min <= counter:
        idx_input1, idx_input2 = [int(x) for x in row['input'].split()]
        idx_target = int(row['target'])
        inputs.append(np.concatenate(
          (get_one_hot(idx_input1), get_one_hot(idx_input2)),
          dtype='i'
        ))
        targets.append(get_one_hot(idx_target))
        # progress stats
        n_done += 1
        t_elapsed = time.perf_counter()-t_start
        t_remaining = (n_total-n_done)/n_done*t_elapsed
        print(f'\r🟡 Done: {n_done}/{n_total} '
          + f'Elapsed: {t_elapsed:.3f}s '
          + f'ETA: {t_remaining:.3f}s', end = ' ')
      counter += 1
    # end
    print(f'\r✅ Done: {n_done}/{n_total} - '
      + f'Elapsed: {t_elapsed:.3f}s'
      + ' '*20)
  
  # Shuffle data training
  print('🟡 Shuffle data training', end='')
  n_data = len(inputs)
  t_start = time.perf_counter()
  for i in range(100 * n_data):
    ran_1 = int(random.random()*n_data)
    ran_2 = int(random.random()*n_data)
    # swapping index: ran_1 <-> ran_2 
    inputs[ran_1], inputs[ran_2] = inputs[ran_2], inputs[ran_1]
    targets[ran_1], targets[ran_2] = targets[ran_2], targets[ran_1]
  print('\r✅ Shuffle data training')

  inputs = np.array(inputs)
  targets = np.array(targets)
  return inputs, targets

# Model CBOW init
print(PROCESS_FORMAT, 'Model CBOW Learning')
early_stop_patience = params['n_epoch']
early_stop_min_delta = 1e-5
cbow_input_shape = n_vocab*2
cb_early_stop = EarlyStopping(
  monitor = 'val_loss',
  min_delta = early_stop_min_delta,
  patience = early_stop_patience,
  verbose = 0,
  mode = 'auto')
model_embedding = Sequential([
  InputLayer(input_shape=cbow_input_shape, name='entry'),
  Dense(cbow_input_shape, activation='linear', name='input'),
  Dense(size_embed, activation='linear', name='hidden'),
  Dense(n_vocab, activation='softmax', name='output')])
model_embedding.build(cbow_input_shape)

# cbow compile
print(PROCESS_FORMAT, 'Model CBOW compile')
metric_name = 'binary_accuracy'
model_metric = BinaryAccuracy(threshold=0.8)
model_embedding.compile(
  Adam(learn_rate),
  loss = 'mae',
  # metrics = [model_metric])
  metrics = [model_metric, 'accuracy'])

# Save model architecture
model_embedding.summary()
path_save = path_vector + '/cbow_arch.png'
plot_model(
  model_embedding,
  to_file = path_save,
  show_shapes = True,
  show_dtype = True,
  expand_nested = True,
  show_layer_names = True,
  show_layer_activations = True)
os.system('open ' + f'{path_save}'.replace(' ','\ '))
print(f'✅ Architecture set')
print('   - Inputs shape  =', n_vocab*2)
print('   - Targets shape =', n_vocab)

# LEARN
n_batch = ceil(n_data_train / n_data_batch)
learn_log = {
  'accuracy' : [],
  'val_accuracy' : [],
  'binary_accuracy' : [],
  'val_binary_accuracy' : [],
  'loss' : [],
  'val_loss' : [],
}
# init print
print(PROCESS_FORMAT, "CBOW is now learning")
print('   - Learning rate  =', learn_rate)
print('   - Max epoch    =', n_epoch)
print('   - Patience     =', early_stop_patience)
print('   - Min delta    =', early_stop_min_delta)
print('   - Total data   =', n_data_train)
print('   - Num of batch   =', n_batch)
print('   - Data per batch =', n_data_batch)
# start
for i in range(n_batch):
  # get data train
  print(PROCESS_FORMAT, f'Getting data training - batch {i+1} of {n_batch}')
  idx_min = n_data_batch * i
  idx_max = idx_min + n_data_batch - 1
  inputs, targets = get_train_data(idx_min, idx_max)
  
  # learn
  print(PROCESS_FORMAT, 'Model CBOW learning')
  history = model_embedding.fit(
    x = inputs,
    y = targets,
    epochs = n_epoch,
    verbose = 1,
    validation_split= 1/9,
    callbacks=[cb_early_stop])
  
  # Saving history: START
  accuracy_key = metric_name
  val_accuracy_key = 'val_' + metric_name
  loss_key = 'loss'
  val_loss_key = 'val_loss'
  
  # Save history: accuracy
  plt.clf()
  plt.plot(history.history['accuracy'])
  plt.plot(history.history['val_accuracy'])
  plt.title(f'accuracy batch {i+1}')
  plt.ylabel(metric_name)
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  path_save = path_vector + f'/accuracy-batch-{i+1}.png'
  print(EXPORT_FORMAT, path_save)
  plt.savefig(path_save, bbox_inches='tight')
  os.system('open ' + f'{path_save}'.replace(' ','\ '))
  
  # Save history: binary_accuracy
  plt.clf()
  plt.plot(history.history[accuracy_key])
  plt.plot(history.history[val_accuracy_key])
  plt.title(f'binary_accuracy batch {i+1}')
  plt.ylabel(metric_name)
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  path_save = path_vector + f'/binary_accuracy-batch-{i+1}.png'
  print(EXPORT_FORMAT, path_save)
  plt.savefig(path_save, bbox_inches='tight')
  os.system('open ' + f'{path_save}'.replace(' ','\ '))
  
  # Save history: loss MAE
  plt.clf()
  plt.plot(history.history[loss_key])
  plt.plot(history.history[val_loss_key])
  plt.title(f'batch {i+1} - loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  path_save = path_vector + f'/loss-batch-{i+1}.png'
  print(EXPORT_FORMAT, path_save)
  plt.savefig(path_save, bbox_inches='tight')
  os.system('open ' + f'{path_save}'.replace(' ','\ '))

  # Add logs
  learn_log['accuracy'].append(history.history['accuracy'])
  learn_log['val_accuracy'].append(history.history['val_accuracy'])
  learn_log['binary_accuracy'].append(history.history['binary_accuracy'])
  learn_log['val_binary_accuracy'].append(history.history['val_binary_accuracy'])
  learn_log['loss'].append(history.history['loss'])
  learn_log['val_loss'].append(history.history['val_loss'])
  
  # Save history: DONE
  print(f'✅ Model batch {i+1} history saved')

  # Clearing memory
  del inputs
  del targets
  gc.collect()
  
# save logs
path_save = path_vector + f'/learn_log.json'
json.dump(learn_log, open(path_save, 'w'), indent=4)

# Extract embeddings
embeddings = model_embedding.get_layer('output').get_weights()[0]
path_csv = path_vector + '/embeddings.csv'
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
      embed.append(embeddings[j][i])
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