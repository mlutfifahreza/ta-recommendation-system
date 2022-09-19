# Thesis
- Muhammad Lutfi Fahreza
- 18/430269/PA/18782

# MPD
1. Download datasets from here https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/dataset_files
2. Extract
3. Put 'spotify_million_playlist_dataset' under 'data/mpd/'

# How to run
0. Make sure all dependencies installed
1. Check parameters.json, update these fields (if necessary):
   - n_playlist : how many playlists to select from mpd
   - embed_list : list of embed size to train
   - window_size : window size for FastText train
   - epoch_min
   - epoch_max
   - epoch_patience : how many patience of negative progress of accuracy
   - n_list : list of starting number of tracks in playlist to reccomend
2. After updating the params, run the main.py