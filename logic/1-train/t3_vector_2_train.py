import os, csv, time, json
import numpy as np
import matplotlib.pyplot as plt
from gensim.test.utils import datapath
from gensim.test.utils import common_texts
from gensim.models import FastText
from gensim.test.utils import get_tmpfile

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# General Variables
params = json.load(open('parameters.json'))
n_playlist = params['n_playlist']
epoch_min = params['epoch_min']
epoch_max = params['epoch_max']
epoch_patience = params['epoch_patience']
path_general = f'data/general'
# # # # # # # # # # # # # # # # # # # # # #


# Paths
path_vector = f'data/model/vector/playlist={n_playlist}'
best_model_path = f'{os.getcwd()}/{path_vector}/fasttext_best.model'

# Init gradual training
data_valid = json.load(open(path_vector + '/data_valid.json'))
train_stat = {}
embed_list = params['embed_list']
epoch_range = list(range(1, epoch_max+1))
accuracy_max = params['result'][str(n_playlist)]['accuracy_max']

# Start gradual training
for curr_size_embed in embed_list:
  print(PROCESS_FORMAT, f'vector training with embed = {curr_size_embed}')
  train_stat[curr_size_embed] = {'accuracy' : []}
  
  # FastText - load data
  print(SUBPROCESS_FORMAT, 'Model building')
  print('window_size', params['window_size'])
  t_start = time.perf_counter()
  corpus_file = datapath(f'{os.getcwd()}/{path_vector}/playlists_corpus_train.csv')  # absolute path to corpus
  model = FastText(vector_size=curr_size_embed, window=params['window_size'], min_count=1)
  model.build_vocab(corpus_file=corpus_file)  # scan over corpus to build the vocabulary
  total_words = model.corpus_total_words  # number of words in the corpus
  track_keys = model.wv.key_to_index.keys()
  t_elapsed = time.perf_counter()-t_start
  print(f'✅ Finished {t_elapsed:.3f}s')
  
  # Init training
  print(SUBPROCESS_FORMAT, f'Learning max epoch = {epoch_max}')
  t_start = time.perf_counter()
  patience_left = epoch_patience
  accuracy_max_local = 0

  # FastText - training
  for curr_epoch in epoch_range:
    print(SUBPROCESS_FORMAT, f'Learning -- Epoch = {curr_epoch}/{epoch_max}', end=' -- ')
    t_epoch_start = time.perf_counter()
    model.train(corpus_file=corpus_file, total_words=total_words, epochs=1)
    t_elapsed = time.perf_counter()-t_start
    t_epoch = time.perf_counter()-t_epoch_start
    print(f'Elapsed {t_elapsed:.3f}s (+{t_epoch:.3f}s)', end = ' -- ')

    # FastText - validate
    TP = FP = TN = FN = 0
    for data in data_valid['value']:
      id1, id2, target = data
      output = model.wv.similarity(id1, id2)
      # negative output
      if output < 0.5:
        if target == 0: TN += 1
        else: FN += 1
      # positive output
      else:
        if target == 1: TP += 1
        else: FP += 1
    
    # FastText - training check
    total_data = (TP+FP+TN+FN)
    accuracy = (TN+TP)/total_data
    train_stat[curr_size_embed]['accuracy'].append(accuracy)
    print(f'Accuracy = {accuracy:.3f}', end=' ')
    # check best model local
    if accuracy > accuracy_max_local:
      accuracy_max_local = accuracy
      patience_left = epoch_patience
      print(f'✅ Local best -> Patience = {patience_left}', end=' ')
    # check best model global
    if accuracy > accuracy_max:
      params['result'][f'{n_playlist}']['best_epoch'] = curr_epoch
      params['result'][f'{n_playlist}']['best_embed'] = curr_size_embed
      accuracy_max = accuracy
      print('✅ Global best', end=' ')
      # saving model
      model.save(best_model_path)
    print()
    # early stop
    if curr_epoch > epoch_min:
      curr_F = train_stat[curr_size_embed]['accuracy'][-1]
      last_F = train_stat[curr_size_embed]['accuracy'][-2]
      if (curr_F < last_F):
        patience_left -= 1
        print(f'⛔️ Negative learning', end=' ')
        if patience_left == 0:
          print('-> Patience = 0 -- Early stopping')
          break
        else:
          print(f'-> Patience left = {patience_left}')

# Print best model
print('- Best embed size =', params['result'][f'{n_playlist}']['best_embed'])
print('- Best epoch at   =', params['result'][f'{n_playlist}']['best_epoch'])
for key, value in train_stat.items():
  max_acc = max(value['accuracy'])
  print(f'Best accuracy for embed {key} = {max_acc}')
if (accuracy_max > params['result'][str(n_playlist)]['accuracy_max']):
  params['result'][str(n_playlist)]['accuracy_max'] = accuracy_max
  params['result'][str(n_playlist)]['best_model_path'] = best_model_path
  print(f'model saved to: {best_model_path}')

# Save all-accuracy
legend_tag = []
plt.clf()
for k,v in train_stat.items():
  plt.plot(v['accuracy'])
  legend_tag.append(f'vector_size {k}')
plt.xticks(rotation = 90)
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.title(f'FastText - Learning')
plt.legend(legend_tag, loc='lower right')
path_save = path_vector + f'/train_accuracy.png'
plt.savefig(path_save, bbox_inches='tight')
os.system('open ' + f'{path_save}'.replace(' ','\ '))

json.dump(params, open('parameters.json', 'w'), indent=2)
json.dump(train_stat, open(path_vector + '/train_stat.json', 'w'), indent=2)

