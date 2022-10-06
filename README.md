# Thesis
- Muhammad Lutfi Fahreza
- 18/430269/PA/18782

# MPD
1. Download datasets from here https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/dataset_files
2. Extract
3. Put 'spotify_million_playlist_dataset' under 'data/mpd/'

# How to run
1. Make sure all dependencies installed
2. Check params.json, update these fields (if necessary):
   - n_playlist : how many playlists to select from mpd
   - vector_list : list of vector size to train
   - window_size : window size for Word2Vec train
   - epoch_min
   - epoch_max
   - epoch_patience : how many patience of negative progress of accuracy
   - n_list : list of starting number of tracks in playlist to reccomend
3. After updating the params, run the main.py

# Dependencies used
- Python v3.8.13
- demoji v1.1.0
- gensim v4.2.0
- matplotlib v3.5.2
- nltk v3.7
- numpy v1.22.4