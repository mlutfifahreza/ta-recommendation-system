import os, time, csv
import numpy as np
import matplotlib.pyplot as plt

# General Variables
READING_STRING = '\033[94m' + "Reading :" + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export :" + '\033[0m'
PROCESS_STRING = '\033[35m' + "Process :" + '\033[0m'
root_path = os.getcwd()

# FCM: helper functions
def square_dist(x, y):
    return np.sum(np.square(x - y))

def SSE(weights, inputs, centroids, p = 1.75):
    sse = 0
    for k in range(n_clusters):
        for i in range(n_data):
            sse += (weights[i,k] ** p) * square_dist(inputs[i], centroids[k])
    return sse

def get_centroids(weights, inputs, p = 1.75):
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
# Getting embedding as inputs
inputs = []
csv_path = root_path + "/data/result/cbow_embeddings.csv"
with open(csv_path) as csv_file:
    # starting
    print(READING_STRING, csv_path)
    print("Please wait...", end="\r")
    t_start = time.time()
    # read and process
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        embed = [float(x) for x in row["vector"].split()]
        inputs.append(np.array(embed))
    # finishing
    inputs = np.array(inputs)
    print(f"Done in {time.time()-t_start:.3f}s")
print("inputs.shape =", inputs.shape)
print("example:", list(inputs[20]))

# FCM: variables update
n_data = inputs.shape[0]
n_clusters = n_data//200
n_dimension = inputs.shape[1]
fuzzy_param = 1.8
max_iter = 20
threshold = 1e-10

# FCM: init weights, centroids
weights = np.random.rand(n_data, n_clusters)
centroids = None
# FCM: learn
print(PROCESS_STRING, "FCM Learning")
print(f"Parameters:"
    + f"\n  fuzzy param = {fuzzy_param} "
    + f"\n  threshold = {threshold} "
    + f"\n  num of clusters = {n_clusters}")
log_sse = []
log_sse_diff = []
last_sse = float("inf")
for i in range(max_iter):
    # For progress checking
    t_start = time.time()
    print(f"Iteration: {i+1}/{max_iter} Status: computing...", end ="\r")
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
        log_sse_diff.append(sse_diff)
        # progress stats
        t_elapsed = time.time()-t_start
        print(f"\rIteration: {i+1}/{max_iter} Status: Done - "
            + f"Elapsed: {t_elapsed:.3f}s E: {new_sse} dE:{sse_diff}")
    else:
        print(f"\rIteration: {i+1}/{max_iter} Status: stopping, change of error < threshold")
        break
# Save learning logs
print("sse =",log_sse)
plt.plot(list(range(1,len(log_sse)+1)), log_sse)
plt.ylabel("Sum of squared error (SSE)")
plt.xlabel("Iteration")
plt.plot()
plt.title("FCM - Error Learning Logs")
plt.savefig("./data/result/fcm_error.png", bbox_inches="tight")
os.system("open ./data/result/fcm_error.png")


# Save cluster-100tracks