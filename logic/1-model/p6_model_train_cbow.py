import os, csv, time, random, sys
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense, InputLayer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import plot_model

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

# Getting labels -> convert to one hot encoding
label_encoding = {}
path_relative = path_pop + '/track-count.csv'
with open(path_root + path_relative) as csv_file:
    # starting
    print(READING_STRING, path_relative)
    t_start = time.time()
    # read and process
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        label_encoding[row['track_id']] = None
    # finishing
    print(f'✅ {(time.time()-t_start):.2f}s')
# Get one hot encoding
track_count = len(label_encoding)
print('track_count =',track_count)
i = 0
for key in label_encoding.keys():
    label_encoding[key] = np.zeros(track_count, dtype='i')
    label_encoding[key][i] = 1
    i += 1

# Getting data training
print(PROCESS_STRING, 'Getting data training')
inputs, targets = [], []
path_relative = '/data/data-training/playlists.csv'
with open(path_root + path_relative) as csv_file:
    # starting
    print(READING_STRING, path_relative)
    t_start = time.time()
    # read and process
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        track_ids = row['track_ids'].split()
        for i in range(1, len(track_ids)-1):
            # add context of the label's neighbour as inputs
            inputs.append(np.concatenate((
                label_encoding[track_ids[i-1]], 
                label_encoding[track_ids[i+1]]), 
                dtype='i'))
            # add label as target
            targets.append(np.array(label_encoding[track_ids[i]], dtype='i'))
    # finishing
    print(f'✅ {(time.time()-t_start):.3f}s')
n_data_train = len(inputs)
print('n_data_train =', n_data_train)
# Shuffle data training
print(PROCESS_STRING, 'Shuffle data training')
t_start = time.time()
for i in range(100 * n_data_train):
    ran_1 = int(random.random()*n_data_train)
    ran_2 = int(random.random()*n_data_train)
    # swapping between index ran_1 and ran_2 
    inputs[ran_1], inputs[ran_2] = inputs[ran_2], inputs[ran_1]
    targets[ran_1], targets[ran_2] = targets[ran_2], targets[ran_1]
# finishing
print(f'✅ {(time.time()-t_start):.3f}s')


# Model CBOW
print(PROCESS_STRING, 'Model CBOW Learning')
inputs = np.array(inputs)
targets = np.array(targets)
model = Sequential([
    InputLayer(input_shape=(inputs.shape[1]), name='input'),
    Dense(size_embed, activation='sigmoid', name='hidden'),
    Dense(targets.shape[1], activation='sigmoid', name='output')
])
print(f'✅ Architecture set')
print('ℹ️  Inputs shape  =', inputs.shape)
print('ℹ️  Targets shape =', targets.shape)
print('ℹ️  Learning rate =', learn_rate)
print('ℹ️  Num of epoch  =', n_epoch)
model.compile(
    Adam(learn_rate),
    loss='mse',
    metrics=['accuracy', 'mse'])
print(f'✅ Model compiled')
history = model.fit(
    x = inputs,
    y = targets,
    epochs = n_epoch,
    verbose = 0,
    validation_split= 1/9)
print(f'✅ Learning done')

# Creating saving directory path
if not os.path.exists(path_root + path_cbow):
    os.makedirs(path_root + path_cbow)

# Save model architecture
plot_model(
    model,
    to_file = path_root + path_cbow + '/cbow_arch.png',
    show_shapes = True,
    show_dtype = True,
    expand_nested = True,
    show_layer_names = True,
    show_layer_activations = True)

# # Save history : accuracy
# plt.plot(history.history['accuracy'])
# plt.plot(history.history['val_accuracy'])
# plt.title(f'size embed: {size_embed}, {n_playlist}:playlists')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# path_save = path_root + path_cbow + '/accuracy.png'
# print(EXPORT_STRING, path_save)
# plt.savefig(path_save, bbox_inches='tight')
# os.system(f'open {path_save}')

# Save history : accuracy - train
plt.clf()
plt.plot(history.history['accuracy'])
plt.title(f'size embed: {size_embed}, {n_playlist}:playlists')
plt.ylabel('accuracy-train')
plt.xlabel('epoch')
plt.legend(['train'], loc='upper left')
path_save = path_root + path_cbow + '/accuracy-train.png'
print(EXPORT_STRING, path_save)
plt.savefig(path_save, bbox_inches='tight')
os.system(f'open {path_save}')

# Save history : accuracy - test
plt.clf()
plt.plot(history.history['val_accuracy'])
plt.title(f'size embed: {size_embed}, {n_playlist}:playlists')
plt.ylabel('accuracy-test')
plt.xlabel('epoch')
plt.legend(['test'], loc='upper left')
path_save = path_root + path_cbow + '/accuracy-test.png'
print(EXPORT_STRING, path_save)
plt.savefig(path_save, bbox_inches='tight')
os.system(f'open {path_save}')

# Save history : loss
plt.clf()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title(f'model loss size embed: {size_embed}, {n_playlist}:playlists')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
path_save = path_root + path_cbow + '/loss.png'
print(EXPORT_STRING, path_save)
plt.savefig(path_save, bbox_inches='tight')
os.system(f'open {path_save}')

# Save history : DONE
print(f'✅ Model history saved')

# Extract embeddings
path_relative = path_cbow + '/embeddings.csv'
with open(path_root + path_relative, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, path_relative)
    n_total = track_count
    n_done = 0
    t_start = time.time()
    writer = csv.writer(f)
    # write header
    header = ['one_hot_index', 'vector']
    writer.writerow(header)
    # write content
    for i in range(track_count):
        embed = []
        for j in range(size_embed):
            embed.append(model.layers[1].get_weights()[0][j][i])
        embed = ' '.join([str(e) for e in embed])
        writer.writerow([i, embed])
        # progress stats
        n_done += 1
        t_elapsed = time.time()-t_start
        t_remaining = (n_total-n_done)/n_done* t_elapsed
        print(f'\rProgress: {n_done}/{n_total} '
            + f'Elapsed: {t_elapsed:.3f}s '
            + f'Remaining: {t_remaining:.3f}s', end = ' ')
    # finishing
    print()
    print(f'✅ {(time.time()-t_start):.3f}s')