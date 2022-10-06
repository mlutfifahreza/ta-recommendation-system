import csv, time, sys, json
from nltk.corpus import wordnet
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


# Get token tracks list
print(PROCESS_FORMAT, 'Get token tracks list')
tokens = [] 
path_csv = path_token_sim + '/token-tracks.csv'
with open(path_csv) as csv_file:
  print(READING_FORMAT, path_csv)
  n_done = 0
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    tokens.append(str(row['token']))
    n_done += 1
print(f'\r✅ Done: {n_done}')

# LEARN: Generating token-20tokens
print(PROCESS_FORMAT, 'Generate token-20tokens')
similarities = {}
n_done, n_total = 0, len(tokens)
t_start = time.perf_counter()
for i in range(n_total):
  token_1 = tokens[i]
  similarities[token_1] = []
  # synsets for token 1
  token_1_synset = {}
  try: token_1_synset['n'] = wordnet.synset(token_1 + '.' + 'n' + '.01')
  except: token_1_synset['n'] = None
  try: token_1_synset['a'] = wordnet.synset(token_1 + '.' + 'a' + '.01')
  except: token_1_synset['a'] = None
  try: token_1_synset['v'] = wordnet.synset(token_1 + '.' + 'v' + '.01')
  except: token_1_synset['v'] = None
  # start comparing
  for token_2 in tokens[:i]+tokens[i+1:]:
    # synsets for token 2
    token_2_synset = {}
    try: token_2_synset['n'] = wordnet.synset(token_2 + '.' + 'n' + '.01')
    except: token_2_synset['n'] = None
    try: token_2_synset['a'] = wordnet.synset(token_2 + '.' + 'a' + '.01')
    except: token_2_synset['a'] = None
    try: token_2_synset['v'] = wordnet.synset(token_2 + '.' + 'v' + '.01')
    except: token_2_synset['v'] = None
    temp_similarities = []
    # path_similarity
    for type1 in ['n', 'a', 'v']:
      for type2 in ['n', 'a', 'v']:
        if ((token_1_synset[type1] is not None) 
        and (token_2_synset[type2] is not None)):
          try: 
            sim_value = token_1_synset[type1].path_similarity(token_2_synset[type2])
            temp_similarities.append(sim_value)
          except: pass
    similarity_with_token2 = [token_2, 0]
    if len(temp_similarities) > 0: 
      similarity_with_token2[1] = max(temp_similarities)
    similarities[token_1].append(similarity_with_token2)
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
    if sim[1] > 0: 
      sim_token, sim_value = sim[0], sim[1]
      new_top20[sim_token] = sim_value
    else:
      break
  if len(new_top20) > 1:
    new_top20[token] = 0.5 # add its own token
    token_20tokens[token] = new_top20

# Save JSON
path_export = path_token_sim + '/token_20tokens.json'
print(EXPORT_FORMAT, path_export)
json.dump(token_20tokens, open(path_export, 'w'))
print(f'✅ Finished')