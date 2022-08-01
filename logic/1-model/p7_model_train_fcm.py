import os, time, numpy as np, sys
import matplotlib.pyplot as plt

# General Variables
READING_STRING = '\033[94m' + "Reading :" + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export :" + '\033[0m'
PROCESS_STRING = '\033[35m' + "Process :" + '\033[0m'
root_path = os.getcwd()

n_clusters = 4
n_data = 120
n_dimension = 2
fuzzy_param = 1.8
max_iter = 20
threshold = 1e-6

# Fuzzy C Means Clustering
def square_dist(x, y):
    return np.sum(np.square(x - y))

def SSE(weights, inputs, centroids, p = fuzzy_param):
    sse = 0
    for k in range(n_clusters):
        for i in range(n_data):
            sse += (weights[i,k] ** p) * square_dist(inputs[i], centroids[k])
    return sse

def get_centroids(weights, inputs, p = fuzzy_param):
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

def update_weights(weights, inputs, centroids, p = fuzzy_param):
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

# FCM: init inputs
cluster1 = np.random.randint(low=81, high=90, size=(n_data//n_clusters, n_dimension))
cluster2 = np.random.randint(low=41, high=50, size=(n_data//n_clusters, n_dimension))
cluster3 = np.random.randint(low=31, high=40, size=(n_data//n_clusters, n_dimension))
cluster4 = np.random.randint(low=1, high=10, size=(n_data//n_clusters, n_dimension))
inputs = np.concatenate((cluster1, cluster2, cluster3, cluster4))
# FCM: init weights, centroids
weights = np.random.rand(n_data, n_clusters)
centroids = None
# FCM: learn
log_sse = []
last_sse = float("inf")
for i in range(max_iter):
    new_centroids = get_centroids(weights, inputs)
    new_weights = update_weights(weights, inputs, new_centroids)
    new_sse = SSE(new_weights, inputs, new_centroids)
    if (last_sse - new_sse) > threshold:
        weights = new_weights
        centroids = new_centroids
        last_sse = new_sse
        log_sse.append(new_sse)
    else:
        break

# Save cluster-100tracks