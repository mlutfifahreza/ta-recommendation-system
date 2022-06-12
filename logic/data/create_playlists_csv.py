import os, json, csv, time

# Constants
COUNT_MPD_FILE = 1000 # number of files inside mpd data
COUNT_MPD_FILE_DATA = 1000 # count of data inside each file
COUNT_TO_SELECT = 200000
COUNT_SELECTED = 0
TIME_START = time.time()

# Getting path
current_path = os.getcwd()
data_path = current_path + "/data/mpd/spotify_million_playlist_dataset/data/"

# Getting file names
mpd_file_names = []
for i in range(COUNT_MPD_FILE):
    start = i*COUNT_MPD_FILE_DATA
    end = start+(COUNT_MPD_FILE_DATA-1)
    mpd_file_names.append("mpd.slice." + str(start) + "-" + str(end) + ".json")

# Extract CSV
header = ["playlist_id","title","track_ids"]
extract_path_name = current_path + "/data/data-200/playlists.csv"
with open(extract_path_name, 'w', encoding='UTF8', newline='') as f:
    print("Export : creating", extract_path_name)
    writer = csv.writer(f)
    writer.writerow(header)
    
    print("Reading mpd files")
    for i in range(COUNT_MPD_FILE):
        opened_file = open(data_path+mpd_file_names[i])
        playlists_bacth_i = json.load(opened_file)["playlists"]

        # scanning each playlist
        for playlist in playlists_bacth_i:
            if (COUNT_SELECTED == COUNT_TO_SELECT) : break
            if (playlist["num_tracks"] >= 51 and playlist["num_tracks"] <= 100):
                playlist_info = []
                playlist_info.append(playlist["pid"])
                playlist_info.append(playlist["name"])
                for track in playlist["tracks"]:
                    playlist_info.append(track["track_uri"].replace("spotify:track:",""))
                writer.writerow(playlist_info)
                COUNT_SELECTED += 1

            # progress stats
            time_elapsed = time.time()-TIME_START
            time_remaining = (COUNT_TO_SELECT-COUNT_SELECTED)/COUNT_SELECTED * time_elapsed
            progress_string = "Selected: " + str(COUNT_SELECTED) + "/" + str(COUNT_TO_SELECT)
            progress_string += " Elapsed: " + "{:.2f}".format(time_elapsed) + "s Remaining: " + "{:.2f}".format(time_remaining) + "s"
            print("\r"+progress_string, end ="")
        
        # break condition
        if (COUNT_SELECTED == COUNT_TO_SELECT) : break