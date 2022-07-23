import os, json, csv, time, sys
from operator import itemgetter
# from tqdm import tqdm
import p2_text_preprocessing_title_cleaning as text_preprocess

# General Variables
READING_STRING = '\033[94m' + "Reading :" + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export :" + '\033[0m'
COUNT_MPD_FILE = 1000 # number of files inside mpd data
COUNT_MPD_FILE_DATA = 1000 # count of data inside each file
COUNT_TO_SELECT = 200000
if len(sys.argv) > 1 :
    COUNT_TO_SELECT = int(sys.argv[1])

# For progress checking
COUNT_SELECTED = 0
TIME_START = time.time()

root_path = os.getcwd()
mpd_path = root_path + "/data/mpd/spotify_million_playlist_dataset/data/"
tracks = {}

# Getting file names
mpd_file_names = []
for i in range(COUNT_MPD_FILE):
    start = i*COUNT_MPD_FILE_DATA
    end = start+(COUNT_MPD_FILE_DATA-1)
    mpd_file_names.append("mpd.slice." + str(start) + "-" + str(end) + ".json")

# characters mapping
characters_mapping = {}
# Reading characters_mapping.csv dataset
csv_name = "characters_mapping.csv"
with open(root_path + "/data/data-200/" + csv_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        if is_at_header: is_at_header = False
        else:
            characters_mapping[row[0]] = row[1]

# Generate CSV : playlists.csv
csv_name = "playlists.csv"
with open(root_path + "/data/data-200/" + csv_name, 'w', encoding='UTF8', newline='') as f:
    # starting
    print(EXPORT_STRING, csv_name)
    writer = csv.writer(f)
    # write header
    header = ["playlist_id","title","track_ids"]
    writer.writerow(header)
    # read from mpd -> write content
    for i in range(COUNT_MPD_FILE):
        opened_file = open(mpd_path+mpd_file_names[i])
        playlists_bacth_i = json.load(opened_file)["playlists"]
        # scanning each playlist
        for playlist in playlists_bacth_i:
            if (COUNT_SELECTED == COUNT_TO_SELECT) : break
            # validate condition -> write
            if (
                playlist["num_tracks"] >= 51 
                and playlist["num_tracks"] <= 100 
                and playlist["num_tracks"] == len(playlist["tracks"])
            ):
                playlist_info = []
                playlist_info.append(playlist["pid"])
                playlist_info.append(text_preprocess.clean(playlist["name"], characters_mapping))
                for track in playlist["tracks"]:
                    track_id = track["track_uri"].replace("spotify:track:","")
                    track_name = track["track_name"]
                    artist_id = track["artist_uri"].replace("spotify:artist:","")
                    artist_name = track["artist_name"]
                    playlist_info.append(track_id)
                    if track_id in tracks:
                        tracks[track_id]["count"] += 1
                    else :
                        tracks[track_id] = {
                            "track_id" : track_id,
                            "track_name" : track_name,
                            "artist_id" : artist_id,
                            "artist_name" : artist_name,
                            "count" : 1
                        }
                writer.writerow(playlist_info)
                COUNT_SELECTED += 1
            # progress stats
            time_elapsed = time.time()-TIME_START
            time_remaining = (COUNT_TO_SELECT-COUNT_SELECTED)/COUNT_SELECTED * time_elapsed
            progress_string = "Selected: " + str(COUNT_SELECTED) + "/" + str(COUNT_TO_SELECT)
            progress_string += " Elapsed: " + "{:.2f}".format(time_elapsed) + "s Remaining: " + "{:.2f}".format(time_remaining) + "s"
            print("\r" + progress_string, end ="")
        # break condition
        if (COUNT_SELECTED == COUNT_TO_SELECT) : 
            print()
            break

# Writing tracks.csv popularity sorted
csv_name = "tracks.csv"
with open(root_path + "/data/data-200/" + csv_name, 'w', encoding='UTF8', newline='') as f:
    # starting
    print(EXPORT_STRING, csv_name)
    print("Please wait...", end="\r")
    start_time = time.time()
    writer = csv.writer(f)
    # write header
    header = ["track_id","track_name","artist_id","artist_name","count"]
    writer.writerow(header)
    # write content
    tracks_sorted = sorted(tracks.values(), key=itemgetter("count"), reverse=True) # returns list
    total = len(tracks_sorted)
    for track in tracks_sorted:
        writer.writerow([
            track["track_id"],
            track["track_name"],
            track["artist_id"],
            track["artist_name"],
            track["count"]
        ])
    time_elapsed = "{:.2f}".format(time.time()-start_time)
    print(f"Done in {time_elapsed}s")