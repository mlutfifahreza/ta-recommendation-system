import os, csv, time

# General Variables
READING_STRING = '\033[94m' + "Reading : " + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export : " + '\033[0m'
current_path = os.getcwd()
chars = {}

# Reading titles.csv dataset
csv_name = "playlist_titles.csv"
with open(current_path + "/data/data-200/" + csv_name) as csv_file:
    # starting
    print(READING_STRING, csv_name)
    print("Please wait...", end="\r")
    start_time = time.time()
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        if is_at_header:
            is_at_header = False
        else:
            title = row[0]
            for ch in title:
                chars[ch] = None
    time_elapsed = "{:.3f}".format(time.time()-start_time)
    print(f"Done in {time_elapsed}s\n")

# Writing to known_characters.csv
csv_name = "known_characters.csv"
with open(current_path + "/data/data-200/" + csv_name, 'w', encoding='UTF8', newline='') as f:
    # starting
    print(EXPORT_STRING, csv_name)
    print("Please wait...", end="\r")
    start_time = time.time()
    writer = csv.writer(f)
    # write header
    header = ["character"]
    writer.writerow(header)
    # write content
    sorted_chars = sorted(chars)
    total = len(chars)
    for ch in sorted_chars:
        writer.writerow([ch])
    time_elapsed = "{:.3f}".format(time.time()-start_time)
    print(f"Done in {time_elapsed}s\n")