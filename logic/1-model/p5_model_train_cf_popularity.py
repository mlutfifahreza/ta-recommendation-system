import os, csv, time
from collections import OrderedDict

# General Variables
READING_STRING = '\033[94m' + "Reading :" + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export :" + '\033[0m'
current_path = os.getcwd()

# Reading playlists.csv dataset
track_count = []
csv_name = "playlists.csv"
track_count = {}
with open(current_path + "/data/data-training/" + csv_name) as csv_file:
    # starting
    print(READING_STRING, csv_name)
    print("Please wait...", end="\r")
    start_time = time.time()
    # read and process
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        if is_at_header: is_at_header = False
        else:
            for id in row[2:]:
                if id in track_count: track_count[id] += 1
                else: track_count[id] = 1
    # finished
    time_elapsed = "{:.2f}".format(time.time()-start_time)
    print(f"Done in {time_elapsed}s")

# Convert to list
track_count_list = []
for k,v in track_count.items():
    track_count_list.append([k,v])
# Sort with index 1 : count value
track_count_list.sort(key=lambda row: (row[1]), reverse=True)

# Writing to track_count.csv
csv_name = "track_count.csv"
with open(current_path + "/data/data-training/" + csv_name, 'w', encoding='UTF8', newline='') as f:
    # starting
    TIME_START = time.time()
    print(EXPORT_STRING, csv_name)
    print("Please wait...", end="\r")
    start_time = time.time()
    writer = csv.writer(f)
    # write header
    header = ["track_id", "count"]
    writer.writerow(header)
    # write content
    for item in track_count_list:
        writer.writerow(item)
    # finishing
    time_elapsed = "{:.2f}".format(time.time()-start_time)
    print(f"Done in {time_elapsed}s")