import csv, time, sys, json
import gensim.downloader as api
csv.field_size_limit(sys.maxsize)

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# General Variables
params = json.load(open('params.json'))
n_playlist = params['n_playlist']
path_token_sim = f'data/model/token_sim/playlist={n_playlist}'
# # # # # # # # # # # # # # # # # # # # # #


# Get token list
print(PROCESS_FORMAT, 'Get token list')
tokens = [] 
path_csv = path_token_sim + '/token-tracks.csv'
with open(path_csv) as csv_file:
  print(READING_FORMAT, path_csv)
  csv_reader = csv.DictReader(csv_file)
  n_done = 0
  for row in csv_reader:
    tokens.append(str(row['token']))
    n_done += 1
print(f'\r✅ Total token: {n_done}')

# Load FastText Pre-Trained Model
t_start = time.perf_counter()
print(PROCESS_FORMAT, 'Load FastText Pre-Trained Model')
model = api.load("fasttext-wiki-news-subwords-300")
print(f'✅ Finished: {(time.perf_counter()-t_start):.3f}s')

# LEARN: Generating token-20tokens
print(PROCESS_FORMAT, 'Generate token-20tokens')
similarities = {}
n_done, n_total = 0, len(tokens)
t_start = time.perf_counter()
for token_1 in tokens:
  similarities[token_1] = []
  for token_2 in tokens:
    sim_value = 0
    try: 
      sim_value = float(model.similarity(token_1, token_2))
    except:
      pass
    sim_with_token2 = [token_2, sim_value]
    similarities[token_1].append(sim_with_token2)
  n_done += 1
  t_elapsed = time.perf_counter()-t_start
  t_remaining = (n_total-n_done)/n_done * t_elapsed
  print(f'\r🟡 {n_done}/{n_total} - Elapsed: {t_elapsed:.3f}s '
      + f'- ETA: {t_remaining:.3f}s', end = ' ')
print(f'\r✅ {n_total}  - Elapsed: {t_elapsed:.3f}s' + ' '*40)

# Writing to token_20tokens.json
token_20tokens = {}
for token in similarities:
  # sort -> get top 20
  similarities[token].sort(key=lambda row: (row[1]), reverse=True)
  similarities_top20 = similarities[token][:20]
  new_top20 = {}
  for sim in similarities_top20:
    sim_token, sim_value = sim[0], sim[1]
    new_top20[sim_token] = sim_value
  if len(new_top20) > 1:
    token_20tokens[token] = new_top20

# Save JSON
path_export = path_token_sim + '/token_20tokens.json'
print(EXPORT_FORMAT, path_export)
json.dump(token_20tokens, open(path_export, 'w'), indent=2)
print(f'✅ Finished')