import os, json, csv, time, sys
from operator import itemgetter
import p2_text_preprocessing_title_cleaning as text_preprocess

# General Variables
READING_STRING = '\033[94m' + "Reading :" + '\033[0m'
EXPORT_STRING = '\033[92m' + "Export :" + '\033[0m'
n_mpd_file = 1000 # number of files inside mpd data
n_mpd_file_playlist = 1000 # count of playlist inside each file
root_path = os.getcwd()

# Prepare characters mapping
characters_mapping = {}
with open(root_path + "/data/data-all/" + "characters_mapping.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        characters_mapping[row["char"]] = row["map"]

# Prepare mpd file names
mpd_file_names = []
for i in range(n_mpd_file):
    start = i*n_mpd_file_playlist
    end = start+(n_mpd_file_playlist-1)
    mpd_file_names.append("mpd.slice." + str(start) + "-" + str(end) + ".json")

# Read all mpd files -> create playlists.csv
mpd_path = root_path + "/data/mpd/spotify_million_playlist_dataset/data/"
csv_path = root_path + "/data/data-all/" + "playlists.csv"
tracks = {}
# For progress checking
n_processed = 0
n_to_process = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
t_start = time.time()
with open(csv_path, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, csv_path)
    writer = csv.writer(f)
    # write header
    header = ["playlist_id","title","track_ids"]
    writer.writerow(header)
    # read from mpd -> write content
    for i in range(n_mpd_file):
        opened_file = open(mpd_path+mpd_file_names[i])
        playlists_bacth_i = json.load(opened_file)["playlists"]
        # scanning each playlist
        for playlist in playlists_bacth_i:
            if (n_processed == n_to_process) : break
            # validate condition -> write
            if (
                playlist["num_tracks"] >= 51 
                and playlist["num_tracks"] <= 100 
                and playlist["num_tracks"] == len(playlist["tracks"])
            ):
                playlist_detail = []
                playlist_detail.append(playlist["pid"])
                playlist_detail.append(text_preprocess.clean(playlist["name"], characters_mapping))
                for track in playlist["tracks"]:
                    track_id = track["track_uri"].replace("spotify:track:","")
                    track_name = track["track_name"]
                    artist_id = track["artist_uri"].replace("spotify:artist:","")
                    artist_name = track["artist_name"]
                    playlist_detail.append(track_id)
                    if track_id in tracks: continue
                    else :
                        tracks[track_id] = {
                            "track_id" : track_id,
                            "track_name" : track_name,
                            "artist_id" : artist_id,
                            "artist_name" : artist_name,
                        }
                writer.writerow(playlist_detail)
                n_processed += 1
                # progress stats
                t_elapsed = time.time()-t_start
                t_remaining = (n_to_process-n_processed)/n_processed * t_elapsed
                print(f"\rProgress: {n_processed}/{n_to_process} Elapsed: {t_elapsed:.3f}s Remaining: {t_remaining:.3f}s", end ="")
        # break condition
        if (n_processed == n_to_process) : break
    print()

# Writing tracks.csv sort by id
csv_path = root_path + "/data/data-all/" + "tracks.csv"
with open(csv_path, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, csv_path)
    writer = csv.writer(f)
    t_start = time.time()
    # write header
    header = ["track_id","track_name","artist_id","artist_name","count"]
    writer.writerow(header)
    # write content
    # returns list of sorted track detail
    tracks_sorted = sorted(tracks.values(), key=itemgetter("track_id"))
    for track in tracks_sorted:
        writer.writerow([
            track["track_id"],
            track["track_name"],
            track["artist_id"],
            track["artist_name"],
        ])
    # ending
    print(f"Done in {time.time()-t_start:.3f}s")