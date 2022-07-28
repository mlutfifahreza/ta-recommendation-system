# 2022/07/26 22:47
import os, csv, time, sys, math
from nltk.corpus import wordnet
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from math import exp

# General Variables
READING_STRING = '\033[94m' + "Reading :" + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export :" + '\033[0m'
root_path = os.getcwd()

def sigmoid(x):
    return 1.0 / (1.0 + exp(-x))

def activate(inputs, weights):
    result = []
    for w in weights:
        result.append(sigmoid(np.dot(inputs, w)))
    return np.array(result)

def error(outputs, targets):
    return np.square(np.subtract(targets, outputs)).mean()

def train(size_embed = 6):
    # Getting labels -> convert to one hot encoding
    label_encoding = {}
    # read track_count.csv dataset
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
    encoding = np.zeros(track_count, dtype='i')
    i = 0
    for key in label_encoding.keys():
        encoding[i] = 1
        label_encoding[key] = encoding.copy()
        encoding[i] = 0
        i += 1

    # Getting data training
    inputs = []
    targets = []
    # read playlists.csv dataset
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
                    # add context of the label's neighbour (before and after) as input + add bias
                    data_input = np.concatenate((label_encoding[row[i-1]], label_encoding[row[i+1]], [1]), dtype='i')
                    # add label as target 
                    data_target = label_encoding[row[i]]
                    inputs.append(data_input.copy())
                    targets.append(data_target.copy())
        # finishing
        print("Done in {:.2f}s".format(time.time()-TIME_START))
    
    # TODO: Getting data validation

    # Set Up Variables
    learning_rate = 0.1
    iterations = 10
    size_input = len(inputs[0])
    size_output = len(targets[0])
    size_hidden = size_embed # default = 6
    # initialize layers
    L1 = np.zeros(size_input, dtype='f')
    L2 = np.zeros(size_hidden, dtype='f')
    L3 = np.zeros(size_output, dtype='f')
    # initialize weights
    W1 = np.full((size_hidden, size_input), 0.5, dtype='f')
    W2 = np.full((size_output, size_hidden), 0.5, dtype='f')
    # learning logs
    logs = { "error" : [], "accuracy" : [],}

    # Start Learning
    size_data = len(inputs)
    for itr in range(iterations):
        for d in range(size_data):
            # fast forward 1 : input -> hidden
            L1 = inputs[d]
            L2 = activate(L1, W1)
            # fast forward 2 : hidden -> output
            L3 = activate(L2, W2)
            # back propagation 1 : update weight(output -> hidden)
            # back propagation 2 : update weight(hidden -> input)
        # check error
        logs["error"].append(error(L3, targets[d]))
    # plt.plot(logs["error"])
    # plt.show()
    print(logs["error"])


train()