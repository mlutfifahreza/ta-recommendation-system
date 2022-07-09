from lib2to3.pgen2 import token
import os, csv, time

# General Variables
READING_STRING = '\033[94m' + "Reading :" + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export :" + '\033[0m'
current_path = os.getcwd()
tokens = {}

# Reading playlists.csv dataset
csv_name = "playlists.csv"
with open(current_path + "/data/data-training/" + csv_name) as csv_file:
    # starting
    print(READING_STRING, csv_name)
    print("Please wait...", end="\r")
    total_count = 160000
    processed_count = 0
    TIME_START = time.time()
    # read and process
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        if is_at_header: is_at_header = False
        else:
            title = row[1]
            track_ids = row[2:]
            for token in title.split():
                if token in tokens.keys():
                    # add track_ids without duplicate
                    tokens[token] = list(set(tokens[token] + track_ids))
                else:
                    tokens[token] = track_ids
        # progress stats
        processed_count += 1
        time_elapsed = time.time()-TIME_START
        time_remaining = (total_count-processed_count)/processed_count * time_elapsed
        progress_string = "Processed: " + str(processed_count) + "/" + str(total_count)
        progress_string += " Elapsed: " + "{:.2f}".format(time_elapsed) + "s Remaining: " + "{:.2f}".format(time_remaining) + "s"
        print("\r" + progress_string, end ="")
    print()

# Writing to tokens.csv
csv_name = "tokens.csv"
with open(current_path + "/data/data-training/" + csv_name, 'w', encoding='UTF8', newline='') as f:
    # starting
    print(EXPORT_STRING, csv_name)
    print("Please wait...", end="\r")
    start_time = time.time()
    writer = csv.writer(f)
    # write header
    header = ["token","track_ids"]
    writer.writerow(header)
    # write content
    for key, value in tokens.items():
        writer.writerow([key] + value)
    time_elapsed = "{:.2f}".format(time.time()-start_time)
    print(f"Done in {time_elapsed}s")

# Generating token-20tokens
# todo
# tokens = list(tokens.keys())
# for token in tokens:
#     for token in tokens:
        