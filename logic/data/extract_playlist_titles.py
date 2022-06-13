import os, csv, time

# Getting path
current_path = os.getcwd()
playlists_csv_path = current_path + "/data/data-200/playlists.csv"
playlist_titles_csv_path = current_path + "/data/data-200/playlist_titles.csv"
titles = []

# Reading playlists.csv dataset
titles = {}
with open(playlists_csv_path) as csv_file:
    print("Reading :",playlists_csv_path)
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    print("Please wait...", end="\r")
    start_time = time.time()
    for row in csv_reader:
        if is_at_header:
            is_at_header = False
        else:
            titles[row[1]] = None
    time_elapsed = "{:.3f}".format(time.time()-start_time)
    print(f"Done in {time_elapsed}s\n")

# Writing to titles.csv
header = ["title"]
with open(playlist_titles_csv_path, 'w', encoding='UTF8', newline='') as f:
    print("Creating :", playlist_titles_csv_path)
    writer = csv.writer(f)
    writer.writerow(header)
    sorted_titles = sorted(titles.keys())
    total = len(titles)
    print("Please wait...", end="\r")
    start_time = time.time()
    for title in sorted_titles:
        writer.writerow([title])
    time_elapsed = "{:.3f}".format(time.time()-start_time)
    print(f"Done in {time_elapsed}s\n")