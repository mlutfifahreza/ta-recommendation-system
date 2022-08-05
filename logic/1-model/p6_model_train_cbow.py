import os, csv, time, random, sys
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense, InputLayer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import plot_model

# General Variables
READING_STRING = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_STRING = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_STRING = '\033[35m' + 'Process:' + '\033[0m'
root_path = os.getcwd()

# From input argv
n_playlist = int(sys.argv[1])
size_embed = int(sys.argv[2])

# Getting labels -> convert to one hot encoding
label_encoding = {}
rel_path = '/data/data-training/track-count.csv'
with open(root_path + rel_path) as csv_file:
    # starting
    print(READING_STRING, rel_path)
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
rel_path = '/data/data-training/playlists.csv'
with open(root_path + rel_path) as csv_file:
    # starting
    print(READING_STRING, rel_path)
    t_start = time.time()
    # read and process
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        track_ids = row['track_ids']
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
for i in range(10 * n_data_train):
    ran_1 = int(random.random()*n_data_train)
    ran_2 = int(random.random()*n_data_train)
    # swapping between index ran_1 and ran_2 
    inputs[ran_1], inputs[ran_2] = inputs[ran_2], inputs[ran_1]
    targets[ran_1], targets[ran_2] = targets[ran_2], targets[ran_1]
# finishing
inputs = np.array(inputs)
targets = np.array(targets)
print('inputs shape  =', inputs.shape)
print('targets shape =', targets.shape)

# Model CBOW
print(PROCESS_STRING, 'Model CBOW Learning')
learning_rate, n_epoch = 0.001, 5
model = Sequential([
    InputLayer(input_shape=(inputs.shape[1]), name='input'),
    Dense(size_embed, activation='sigmoid', name='hidden'),
    Dense(targets.shape[1], activation='sigmoid', name='output')
])
plot_model(
    model,
    to_file = './data/result/cbow_arch.png',
    show_shapes = True,
    show_dtype = True,
    expand_nested = True,
    show_layer_names = True,
    show_layer_activations = True)
model.compile(
    Adam(learning_rate),
    loss='mse',
    metrics=['accuracy'])
history = model.fit(
    x = inputs,
    y = targets,
    epochs = n_epoch,
    verbose = 1,
    validation_split= 1/9)

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
save_path = f'./data/result/cbow_accuracy_size_embed_{size_embed}_with_{n_playlist}_playlists.png'
plt.savefig(save_path, bbox_inches='tight')
# os.system(f'open {save_path}')

# summarize history for loss
plt.clf()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
save_path = f'./data/result/cbow_loss_size_embed_{size_embed}_with_{n_playlist}_playlists.png'
plt.savefig(save_path, bbox_inches='tight')
# os.system(f'open {save_path}')

# Extract embeddings
rel_path = '/data/result/cbow_embeddings.csv'
with open(root_path + rel_path, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, rel_path)
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