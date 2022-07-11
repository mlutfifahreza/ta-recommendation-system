import os, csv, time

# General Variables
READING_STRING = '\033[94m' + "Reading :" + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export :" + '\033[0m'
current_path = os.getcwd()

# Reading tracks.csv dataset
track_count = []
csv_name = "tracks.csv"
with open(current_path + "/data/data-200/" + csv_name) as csv_file:
    # starting
    print(READING_STRING, csv_name)
    print("Please wait...", end="\r")
    start_time = time.time()
    # read and process
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        if is_at_header: is_at_header = False
        else: track_count.append([row[0], int(row[4])]) # row 0 = track_id, row 4 = count
    # finished
    time_elapsed = "{:.2f}".format(time.time()-start_time)
    print(f"Done in {time_elapsed}s")

# Writing to track-count.csv
csv_name = "track-count.csv"
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
    for item in track_count:
        writer.writerow(item)
    # finished
    time_elapsed = "{:.2f}".format(time.time()-start_time)
    print(f"Done in {time_elapsed}s")