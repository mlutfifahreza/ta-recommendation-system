import os, csv, time, sys

# General Variables
READING_STRING = '\033[94m' + "Reading :" + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export :" + '\033[0m'
root_path = os.getcwd()
PLAYLIST_TOTAL = int(sys.argv[1]) if (len(sys.argv) > 1) else 200000

# Reading track_count.csv dataset
track_count = {}
csv_name = "track_count.csv"
with open(root_path + "/data/data-training/" + csv_name) as csv_file:
    # starting
    print(READING_STRING, csv_name, end = " ")
    start_time = time.time()
    # read and process
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        if is_at_header: is_at_header = False
        else: track_count[row[0]] = int(row[1]) # row 0 = track_id -> key, row 4 = count -> value
    # finished
    print(f"✅ {time.time()-start_time:.3f}s")

# Reading token_tracks.csv dataset
token_tracks = {} # key = token, value = list of [track id, count]
csv_name = "token_tracks.csv"
with open(root_path + "/data/data-training/" + csv_name) as csv_file:
    # starting
    print(READING_STRING, csv_name)
    print("Please wait...", end="\r")
    total_count = int(PLAYLIST_TOTAL * 0.8)
    processed_count = 0
    TIME_START = time.time()
    # read and process
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        token = row[0]
        if is_at_header: is_at_header = False
        else: 
            track_ids = row[1:] 
            token_tracks[token] = []
            # add track_id and count for each track in token
            for id in track_ids:
                token_tracks[token].append([id, track_count[id]])
            # sort the track_ids by count
            token_tracks[token].sort(key=lambda idx: (idx[1]), reverse=True)
            # trim to first 50 only
            token_tracks[token] = token_tracks[token][:50]
        # progress stats
        processed_count += 1
        time_elapsed = time.time()-TIME_START
        time_remaining = (total_count-processed_count)/processed_count * time_elapsed
        progress_string = "Processed: " + str(processed_count) + "/" + str(total_count)
        progress_string += " Elapsed: " + "{:.2f}".format(time_elapsed) + "s Remaining: " + "{:.2f}".format(time_remaining) + "s"
        print("\r" + progress_string, end ="")
    print()

# Writing to token-50tracks.csv
csv_name = "token-50tracks.csv"
with open(root_path + "/data/data-training/" + csv_name, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    TIME_START = time.time()
    print(EXPORT_STRING, csv_name, end = " ")
    start_time = time.time()
    writer = csv.writer(f)
    # write header
    header = ["token", "20tokens"]
    writer.writerow(header)
    # write content
    for key, value in token_tracks.items():
        ids = []
        for v in value: ids.append(v[0])
        writer.writerow([key] + ids)
    # finished
    time_elapsed = "{:.2f}".format(time.time()-start_time)
    print(f"✅ {time_elapsed}s")

