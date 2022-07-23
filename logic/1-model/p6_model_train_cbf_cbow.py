import os, csv, time, sys
from nltk.corpus import wordnet

# General Variables
READING_STRING = '\033[94m' + "Reading :" + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export :" + '\033[0m'
root_path = os.getcwd()
PLAYLIST_TOTAL = 200000
if len(sys.argv) > 1 :
    PLAYLIST_TOTAL = int(sys.argv[1])

def train():
    # init labels
    # Reading tracks.csv dataset
    csv_name = "tracks.csv"
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
            if is_at_header: is_at_header = False
            else:
                title = row[1]
                track_ids = row[2:]
                for token in title.split():
                    # add track_ids without duplicate
                    if token in token_tracks.keys(): token_tracks[token] = list(set(token_tracks[token] + track_ids))
                    else: token_tracks[token] = track_ids
            # progress stats
            processed_count += 1
            time_elapsed = time.time()-TIME_START
            time_remaining = (total_count-processed_count)/processed_count * time_elapsed
            progress_string = "Processed: " + str(processed_count) + "/" + str(total_count)
            progress_string += " Elapsed: " + "{:.2f}".format(time_elapsed) + "s Remaining: " + "{:.2f}".format(time_remaining) + "s"
            print("\r" + progress_string, end ="")
        print()

    # learn for each item
    window = 1

# TO DO : FINISH