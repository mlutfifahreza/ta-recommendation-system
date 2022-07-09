import os, csv, time
import random

from numpy import mat

# General Variables
READING_STRING = '\033[94m' + "Reading :" + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export :" + '\033[0m'
TIME_START = time.time()
current_path = os.getcwd()

PLAYLIST_TOTAL = 200000
TRAINING_RATIO = 0.8
VALIDATION_RATIO = 0.1
TESTING_RATIO = 0.1
TRAINING_TOTAL = PLAYLIST_TOTAL * TRAINING_RATIO
VALIDATION_TOTAL = PLAYLIST_TOTAL * VALIDATION_RATIO
TESTING_TOTAL = PLAYLIST_TOTAL * TESTING_RATIO

playlist_processed = 0
training_count = 0
validation_count = 0
testing_count = 0

writing_paths = {
    "training" : current_path + "/data/data-training/playlists.csv",
    "validation" : current_path + "/data/data-validation/playlists.csv",
    "testing" : current_path + "/data/data-testing/playlists.csv",
}

def write_split_data(type, playlist):
    with open(writing_paths[type], 'a+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(playlist)
    if (type == "training"):
        global training_count
        training_count += 1
    elif (type == "validation"):
        global validation_count
        validation_count += 1
    else:
        global testing_count
        testing_count += 1

# Reading playlists.csv dataset
csv_name = "playlists.csv"
with open(current_path + "/data/data-200/" + csv_name) as csv_file:
    # starting
    print(READING_STRING, csv_name)
    start_time = time.time()
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        # write header for each file
        if is_at_header:
            for path in writing_paths.values():
                with open(path, 'w', encoding='UTF8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(row)
            is_at_header = False
        else:
            x = random.random()
            # Training Data
            if (x <= TRAINING_RATIO and training_count < TRAINING_TOTAL):
                write_split_data("training", row)
            # Validation Data
            elif (x <= TRAINING_RATIO + VALIDATION_RATIO and validation_count < VALIDATION_TOTAL):
                write_split_data("validation", row)
            # Testing Data
            elif (testing_count < TESTING_TOTAL):
                write_split_data("testing", row)
            # cycle through training -> validation
            elif (training_count < TRAINING_TOTAL):
                write_split_data("training", row)
            else:
                write_split_data("validation", row)
            playlist_processed += 1
        # progress stats
        time_elapsed = time.time()-TIME_START
        time_remaining = (PLAYLIST_TOTAL-playlist_processed)/PLAYLIST_TOTAL * time_elapsed
        progress_string = "Processed: " + str(playlist_processed) + "/" + str(PLAYLIST_TOTAL)
        progress_string += " Elapsed: " + "{:.2f}".format(time_elapsed) + "s Remaining: " + "{:.2f}".format(time_remaining) + "s"
        print("\r" + progress_string, end ="")
print()
print("Playlist processed:", playlist_processed)
print("Training count:", training_count)
print("Validation count:", validation_count)
print("Testing count:", testing_count)