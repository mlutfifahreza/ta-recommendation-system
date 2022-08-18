# ta-recommendation-system

[ON-GOING] PENGGUNAAN METODE SEMANTIC SIMILARITY DAN FUZZY CLUSTERING UNTUK SISTEM REKOMENDASI KELANJUTAN DAFTAR PUTAR LAGU

Automatic Playlist Continuation (APC) adalah tugas untuk menambahkan satu atau lebih lagu ke dalam suatu playlist yang mana sesuai dengan karakteristik dari playlist pada awal mulanya. Dengan ini dapat memudahkan pengguna untuk menikmati mendengarkan lagu secara berkelanjutan melebihi dari jumlah lagu di dalam playlist dan meluaskan playlist tanpa menuntut pengetahuan pengguna secara luas. Penelitian yang dilakukan mencoba untuk menggunakan pendekatan dengan memanfaatkan makna semantik untuk mengolah data teks judul playlist dan fuzzy clustering yang didasarkan kepada representasi numerik (word vector) dari lagu untuk menganalisis setiap lagu di dalam playlistnya.

python logic/0-data/p1_data_preprocessing_playlist_selection.py 50000 20 0.0005 200 500
python logic/0-data/p3_data_split.py 50000 20 0.0005 200 500
python logic/1-model/p4_model_train_popularity.py  50000 20 0.0005 200 500
python logic/1-model/p5_model_train_wordnet_1_tokens.py 50000 20 0.0005 200 500
python logic/1-model/p5_model_train_wordnet_2_token-20tokens.py 50000 20 0.0005 200 500
python logic/1-model/p5_model_train_wordnet_3_token-50tracks.py 50000 20 0.0005 200 500
python logic/1-model/p6_model_train_w2v.py 50000 20 0.0005 200 500
python logic/1-model/p6_model_train_w2v_1_get_train_data.py 50000 20 0.0005 200 500
python logic/1-model/p7_model_train_fcm.py 50000 20 0.0005 200 500