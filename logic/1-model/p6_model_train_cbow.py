import os, csv, time, random
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense, InputLayer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import plot_model

# General Variables
READING_STRING = '\033[94m' + "Reading :" + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export :" + '\033[0m'
PROCESS_STRING = '\033[35m' + "Process :" + '\033[0m'
root_path = os.getcwd()

size_embed = 6
# Getting labels -> convert to one hot encoding
label_encoding = {}
csv_path = root_path + "/data/data-training/track_count.csv"
with open(csv_path) as csv_file:
    # starting
    print(READING_STRING, csv_path)
    print("Please wait...", end="\r")
    t_start = time.time()
    # read and process
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        if is_at_header: is_at_header = False
        else: label_encoding[row[0]] = None
    # finishing
    print(f"Done in {(time.time()-t_start):.2f}s")


# Get one hot encoding
track_count = len(label_encoding)
print("track_count =",track_count)
i = 0
for key in label_encoding.keys():
    label_encoding[key] = np.zeros(track_count, dtype='i')
    label_encoding[key][i] = 1
    i += 1


# Getting data training
print(PROCESS_STRING, "Getting data training")
inputs, targets = [], []
csv_path = root_path + "/data/data-training/playlists.csv"
with open(csv_path) as csv_file:
    # starting
    print(READING_STRING, csv_path)
    print("Please wait...", end="\r")
    t_start = time.time()
    # read and process
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        if is_at_header: is_at_header = False
        else:
            for i in range(3, len(row)-1):
                # add context of the label's neighbour as inputs
                inputs.append(np.concatenate((
                    label_encoding[row[i-1]], 
                    label_encoding[row[i+1]]), 
                    dtype='i'))
                # add label as target
                targets.append(np.array(label_encoding[row[i]], dtype='i'))
    # finishing
    print(f"✅ {(time.time()-t_start):.3f}s")
n_data_train = len(inputs)
print("n_data_train =", n_data_train)
# Shuffle data training
print(PROCESS_STRING, "Shuffle data training")
for i in range(10 * n_data_train):
    ran_1 = int(random.random()*n_data_train)
    ran_2 = int(random.random()*n_data_train)
    # swapping between index ran_1 and ran_2 
    inputs[ran_1], inputs[ran_2] = inputs[ran_2], inputs[ran_1]
    targets[ran_1], targets[ran_2] = targets[ran_2], targets[ran_1]
# finishing
inputs = np.array(inputs)
targets = np.array(targets)
print("inputs shape  =", inputs.shape)
print("targets shape =", targets.shape)


# Model CBOW
print(PROCESS_STRING, "Model CBOW Learning")
learning_rate, n_epoch = 0.001, 5
model = Sequential([
    InputLayer(input_shape=(inputs.shape[1]), name="input"),
    Dense(size_embed, activation='sigmoid', name="hidden"),
    Dense(targets.shape[1], activation='sigmoid', name="output")
])
plot_model(
    model, to_file = "./data/result/cbow_arch.png",
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
    verbose = 'auto',
    validation_split= 1/9)

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
save_path = "./data/result/cbow_accuracy.png"
plt.savefig(save_path, bbox_inches='tight')
os.system(f"open {save_path}")

# summarize history for loss
plt.clf()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
save_path = "./data/result/cbow_loss.png"
plt.savefig(save_path, bbox_inches='tight')
os.system(f"open {save_path}")


# Extract embeddings
csv_path = root_path + "/data/result/cbow_embeddings.csv"
with open(csv_path, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, csv_path, end = " ")
    n_total = track_count
    n_done = 0
    t_start = time.time()
    writer = csv.writer(f)
    # write header
    header = ["one_hot_index", "vector"]
    writer.writerow(header)
    # write content
    for i in range(track_count):
        embed = []
        for j in range(size_embed):
            embed.append(model.layers[1].get_weights()[0][j][i])
        embed = " ".join([str(e) for e in embed])
        writer.writerow([i, embed])
        # progress stats
        n_done += 1
        t_elapsed = time.time()-t_start
        t_remaining = (n_total-n_done)/n_done * t_elapsed
        progress_string = "Processed: " + str(n_done) + "/" + str(n_total)
        progress_string += " Elapsed: " + "{:.2f}".format(t_elapsed) + "s Remaining: " + "{:.2f}".format(t_remaining) + "s"
        print("\r" + progress_string, end ="")
    # finishing
    print(f"✅ {(time.time()-t_start):.3f}s")