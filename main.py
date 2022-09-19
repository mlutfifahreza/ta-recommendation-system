import os, time, json

RUNNING_FORMAT = '\033[33m' + '$ RUNNING:' + '\033[0m'

paths = [
  # DATA
  f'logic/0-data/d0_setup_env.py',
  f'logic/0-data/d1_data_preprocess.py', # 2_text_preprocess called here
  f'logic/0-data/d3_data_split.py',

  # TRAINING
  f'logic/1-train/t1_popularity.py ',
  f'logic/1-train/t2_wordsim_1_tokens.py',
  f'logic/1-train/t2_wordsim_2_token-20tokens.py',
  f'logic/1-train/t2_wordsim_3_token-100tracks.py',
  f'logic/1-train/t3_vector_1_init_data.py',
  f'logic/1-train/t3_vector_2_train.py',
  
  # RECCOMENDATION
  f'logic/2-reccomend/r0_init_data.py',
  f'logic/2-reccomend/r1_title.py',
  f'logic/2-reccomend/r2_vector.py',
  f'logic/2-reccomend/r3_pop.py',
  f'logic/2-reccomend/r4_blend.py',
  f'logic/2-reccomend/r5_eval.py', 
]

ALL_t_start = time.perf_counter()
for path in paths:
  print('____________________________________________________________\n')
  print(RUNNING_FORMAT, path)
  t_start = time.perf_counter()
  os.system(f'python3 {path}')
  print(f'\n✅ ✅ DONE {time.perf_counter()-t_start:.3f}s')

print('____________________________________________________________\n')
print(f'✅ ✅ ✅ ALL DONE {time.perf_counter()-ALL_t_start:.3f}s')
print('____________________________________________________________\n')

os.system(f'open done.jpeg')