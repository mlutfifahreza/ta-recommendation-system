import os, csv, time

# General Variables
READING_STRING = '\033[94m' + "Reading :" + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export :" + '\033[0m'
root_path = os.getcwd()

# Reading playlists.csv dataset
track_count = []
csv_path = root_path + "/data/data-training/playlists.csv"
track_count = {}
with open(csv_path) as csv_file:
    # starting
    print(READING_STRING, csv_path)
    t_start = time.time()
    # read and process
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        for id in [row["track_ids"]] + row[None]:
            if id in track_count: track_count[id] += 1
            else: track_count[id] = 1
    # finished
    print(f"Done in {time.time() - t_start:.3f}s")

# Convert to list
track_count_list = []
for k,v in track_count.items():
    track_count_list.append([k,v])
# Sort with index 1 : count value
track_count_list.sort(key=lambda row: (row[1]), reverse=True)

# Writing to track_count.csv
csv_path = root_path + "/data/data-training/track_count.csv"
with open(csv_path, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    TIME_START = time.time()
    print(EXPORT_STRING, csv_path)
    t_start = time.time()
    writer = csv.writer(f)
    # write header
    header = ["track_id", "count"]
    writer.writerow(header)
    # write content
    for item in track_count_list:
        writer.writerow(item)
    # finishing
    print(f"Done in {time.time() - t_start:.3f}s")