import os, csv, time, numpy as np, random

from tensorflow.keras.layers import Dense, InputLayer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# General Variables
READING_STRING = '\033[94m' + "Reading :" + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export :" + '\033[0m'
PROCESS_STRING = '\033[35m' + "Process :" + '\033[0m'
root_path = os.getcwd()

def train(size_embed = 6):
    # Getting labels -> convert to one hot encoding
    label_encoding = {}
    csv_name = "track_count.csv"
    with open(root_path + "/data/data-training/" + csv_name) as csv_file:
        # starting
        print(READING_STRING, csv_name)
        print("Please wait...", end="\r")
        TIME_START = time.time()
        # read and process
        csv_reader = csv.reader(csv_file, delimiter=',')
        is_at_header = True
        for row in csv_reader:
            if is_at_header: is_at_header = False
            else: label_encoding[row[0]] = None
        # finishing
        print("Done in {:.2f}s".format(time.time()-TIME_START))
    

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
    csv_name = "playlists.csv"
    with open(root_path + "/data/data-training/" + csv_name) as csv_file:
        # starting
        print(READING_STRING, csv_name)
        print("Please wait...", end="\r")
        TIME_START = time.time()
        # read and process
        csv_reader = csv.reader(csv_file, delimiter=',')
        is_at_header = True
        for row in csv_reader:
            if is_at_header: is_at_header = False
            else:
                for i in range(3, len(row)-1):
                    # add context of the label's neighbour (before and after) as inputs
                    inputs.append(np.concatenate((label_encoding[row[i-1]], label_encoding[row[i+1]]), dtype='i'))
                    # add label as target
                    targets.append(np.array(label_encoding[row[i]], dtype='i'))
        # finishing
        print("Done in {:.2f}s".format(time.time()-TIME_START))
    n_data_train = len(inputs)
    print("n_data_train =", n_data_train)
    # Shuffle data training
    print(PROCESS_STRING, "Shuffle data training")
    for i in range(10 * n_data_train):
        ran_1, ran_2 = int(random.random()*n_data_train), int(random.random()*n_data_train)
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
    model.compile(Adam(learning_rate), loss='mse', metrics=['accuracy'])
    history = model.fit(x = inputs, y = targets, epochs = n_epoch, verbose = 1, validation_split= 1/9)

    # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    # plt.show()
    plt.savefig('cbow_accuracy.png', bbox_inches='tight')
    # os.system("open cbow_accuracy.png")
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    # plt.show()
    plt.savefig('cbow_loss.png', bbox_inches='tight')
    # os.system("open cbow_loss.png")

    # Extract embeddings
    csv_name = "embeddings.csv"
    with open(root_path + "/data/data-training/" + csv_name, 'w', encoding='UTF8', newline='') as f:
        # starting
        print(EXPORT_STRING, csv_name)
        print("Please wait...", end="\r")
        total_count = track_count
        processed_count = 0
        TIME_START = time.time()
        writer = csv.writer(f)
        # write header
        header = ["one_hot_index", "vector"]
        writer.writerow(header)
        # write content
        for i in range(track_count):
            embed = []
            for j in range(size_embed):
                embed.append(model.layers[1].get_weights()[0][j][i])
            embed = "_".join([str(e) for e in embed])
            writer.writerow([i, embed])
            # progress stats
            processed_count += 1
            time_elapsed = time.time()-TIME_START
            time_remaining = (total_count-processed_count)/processed_count * time_elapsed
            progress_string = "Processed: " + str(processed_count) + "/" + str(total_count)
            progress_string += " Elapsed: " + "{:.2f}".format(time_elapsed) + "s Remaining: " + "{:.2f}".format(time_remaining) + "s"
            print("\r" + progress_string, end ="")

train()