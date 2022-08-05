import os, csv, time, sys
from nltk.corpus import wordnet

# General Variables
READING_STRING = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_STRING = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_STRING = '\033[35m' + 'Process:' + '\033[0m'
root_path = os.getcwd()
tokens = [] 
PLAYLIST_TOTAL = int(sys.argv[1]) if (len(sys.argv) > 1) else 200000

# Reading token_tracks.csv dataset
rel_path = '/data/data-training/token-tracks.csv'

with open(root_path + rel_path) as csv_file:
    # starting
    print(READING_STRING, rel_path)
    n_done = 0
    t_start = time.time()
    # read and process
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        if is_at_header: is_at_header = False
        else:
            tokens.append(str(row[0]))
            # progress stats
            n_done += 1
            print(f'\rProcessed: {n_done} - Elapsed: {time.time()-t_start:.3f}', end =' ')
    print(f'\n✅ Finished: {time.time() - t_start:.3f}s')

# LEARN: Generating token-20tokens
print(PROCESS_STRING, 'Generating token-20tokens')
similarities = {}
n_done = 0
n_total = len(tokens)
t_start = time.time()
for i in range(n_total):
    # starting
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
                if ((token_1_synset[type1] is not None) and (token_2_synset[type2] is not None)):
                    try: temp_similarities.append(token_1_synset[type1].path_similarity(token_2_synset[type2]))
                    except: pass
        similarity_with_token2 = [token_2, 0]
        if len(temp_similarities) > 0: 
            similarity_with_token2[1] = max(temp_similarities)
            # similarity_with_token2[1] = sum(temp_similarities) / len(temp_similarities)
        similarities[token_1].append(similarity_with_token2)
    # progress stats
    n_done += 1
    t_elapsed = time.time()-t_start
    t_remaining = (n_total-n_done)/n_done * t_elapsed
    print(f'\rProgress: {n_done}/{n_total} '
        + f'Elapsed: {t_elapsed:.3f}s '
        + f'Remaining: {t_remaining:.3f}s', end = ' ')
print(f'\n✅ Finished: {time.time() - t_start:.3f}s')

# Writing to token-20tokens.csv
rel_path = '/data/data-training/token-20tokens.csv'
with open(root_path + rel_path, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, rel_path)
    t_start = time.time()
    writer = csv.writer(f)
    # write header
    header = ['token', '20tokens']
    writer.writerow(header)
    # write content
    for token in similarities:
        # sort -> get top 20
        similarities[token].sort(key=lambda row: (row[1]), reverse=True)
        similarities_top20 = similarities[token][:20]
        top20 = ''
        for sim in similarities_top20:
            if sim[1] > 0: 
                # sim[0] = token, sim[1] = value
                top20 += f'{sim[0]}:{sim[1]} '
            else:
                break
        if len(top20) > 1:
            writer.writerow([token, top20])
    # progress
    print(f'✅ Finished: {time.time() - t_start:.3f}s')
