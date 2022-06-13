import os, json, csv, time, gc
from operator import itemgetter
from tqdm import tqdm

# Constants
COUNT_MPD_FILE = 1000 # number of files inside mpd data
COUNT_MPD_FILE_DATA = 1000 # count of data inside each file
COUNT_TO_SELECT = 200000
COUNT_SELECTED = 0
TIME_START = time.time()

# Getting file names
mpd_file_names = []
for i in range(COUNT_MPD_FILE):
    start = i*COUNT_MPD_FILE_DATA
    end = start+(COUNT_MPD_FILE_DATA-1)
    mpd_file_names.append("mpd.slice." + str(start) + "-" + str(end) + ".json")

# Getting path
current_path = os.getcwd()
data_path = current_path + "/data/mpd/spotify_million_playlist_dataset/data/"
playlists_csv_path = current_path + "/data/data-200/playlists.csv"
tracks_csv_path = current_path + "/data/data-200/tracks.csv"
popular_csv_path = current_path + "/data/data-200/popular.csv"
tracks = {}

# Generate CSV : Playlist
with open(playlists_csv_path, 'w', encoding='UTF8', newline='') as f:
    header = ["playlist_id","title","track_ids"]
    print("Export : creating", playlists_csv_path)
    writer = csv.writer(f)
    writer.writerow(header)
    
    for i in range(COUNT_MPD_FILE):
        opened_file = open(data_path+mpd_file_names[i])
        playlists_bacth_i = json.load(opened_file)["playlists"]

        # scanning each playlist
        for playlist in playlists_bacth_i:
            if (COUNT_SELECTED == COUNT_TO_SELECT) : break
            # validate condition
            if (playlist["num_tracks"] >= 51 and playlist["num_tracks"] <= 100 and playlist["num_tracks"] == len(playlist["tracks"])):
                playlist_info = []
                playlist_info.append(playlist["pid"])
                playlist_info.append(playlist["name"])
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
            print("\r"+progress_string, end ="")
        
        # break condition
        if (COUNT_SELECTED == COUNT_TO_SELECT) : 
            break
            print()

# Generate CSV : tracks sorted popularity
tracks_sorted = sorted(tracks.values(), key=itemgetter("count"), reverse=True) # returns list
with open(tracks_csv_path, 'w', encoding='UTF8', newline='') as f:
    header = ["track_id","track_name","artist_id","artist_name","count"]
    print("Export : creating", tracks_csv_path)
    writer = csv.writer(f)
    writer.writerow(header)
    for track in tqdm(tracks_sorted):
        writer.writerow([
            track["track_id"],
            track["track_name"],
            track["artist_id"],
            track["artist_name"],
            track["count"]
        ])