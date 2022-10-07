import os, time, json

RUNNING_FORMAT = '\033[33m' + '$ RUNNING:' + '\033[0m'

params = json.load(open('params.json'))
vector_list = params['vector_list']

paths_1 = [
  'logic/0-data/d0_setup_env.py',
  'logic/0-data/d1_data_preprocess.py', # 2_text_preprocess called here
  'logic/0-data/d3_data_split.py',
  'logic/1-train/t1_popularity.py ',
  'logic/1-train/t2_wordsim_1_tokens.py',
  'logic/1-train/t2_wordsim_2_token-20tokens.py',
  'logic/1-train/t2_wordsim_3_token-100tracks.py',
  'logic/1-train/t3_vector_1_init_data.py',
]
paths_2 = [
  'logic/1-train/t3_vector_2_train.py',
  'logic/2-reccomend/r0_init_data.py',
  'logic/2-reccomend/r1_title.py',
  'logic/2-reccomend/r2_track.py',
  'logic/2-reccomend/r3_blend.py',
  'logic/2-reccomend/r4_pop_fillup.py',
  'logic/2-reccomend/r5_eval.py',
]

ALL_t_start = time.perf_counter()
for path in paths_1:
  print('____________________________________________________________\n')
  print(RUNNING_FORMAT, path)
  t_start = time.perf_counter()
  os.system(f'python3 {path}')
  print(f'\n✅ ✅ DONE {time.perf_counter()-t_start:.3f}s')

for size in vector_list:
  print('\n\n\n')
  for path in paths_2:
    params = json.load(open('params.json'))
    params['vector_size'] = size
    json.dump(params, open('params.json', 'w'), indent=2)
    print(f'_______________  VECTOR SIZE = {size}  ____________________\n')
    print(RUNNING_FORMAT, path)
    t_start = time.perf_counter()
    os.system(f'python3 {path}')
    print(f'\n✅ ✅ DONE {time.perf_counter()-t_start:.3f}s')

print('____________________________________________________________\n')
print(f'✅ ✅ ✅ ALL DONE {time.perf_counter()-ALL_t_start:.3f}s')
print('____________________________________________________________\n')

os.system(f'open done.jpeg')