import os, time, json
from random import sample
import matplotlib.pyplot as plt
from gensim.test.utils import datapath
from gensim.models import Word2Vec

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# General Variables
params = json.load(open('params.json'))
n_playlist = params['n_playlist']
epoch_min = params['epoch_min']
epoch_max = params['epoch_max']
epoch_patience = params['epoch_patience']
vector_size = params['vector_size']
window_size = params['window_size']
path_general = f'data/general'
# # # # # # # # # # # # # # # # # # # # # #


# Paths
path_track_sim = f'data/model/track_sim/playlist={n_playlist}'
best_model_path = f'{os.getcwd()}/{path_track_sim}/Word2Vec_best.model'

# Init gradual training
data_valid = json.load(open(path_track_sim + '/data_valid.json'))
train_stat = {}
max_accuracies = {}
try: 
  train_stat = json.load(open(path_track_sim + f'/train_stat.json'))
  max_accuracies = json.load(open(path_track_sim + f'/max_accuracies.json'))
except: pass
accuracy_best = 0
epoch_best = 0


# Word2Vec - load data
print(SUBPROCESS_FORMAT, 'Model building')
t_start = time.perf_counter()
corpus_file = datapath(f'{os.getcwd()}/{path_track_sim}/playlists_corpus_train.csv')  # absolute path to corpus
model = Word2Vec(vector_size=vector_size, window=window_size, min_count=1)
model.build_vocab(corpus_file=corpus_file)  # scan over corpus to build the vocabulary
total_words = model.corpus_total_words  # number of words in the corpus
t_elapsed = time.perf_counter()-t_start
print(f'✅ Finished {t_elapsed:.3f}s')

# Init training
print(PROCESS_FORMAT, f'Training vector_size = {vector_size}')
model_key = f'vector_{vector_size}'
train_stat[model_key] = {'accuracy' : []}
print(SUBPROCESS_FORMAT, f'Learning max epoch = {epoch_max}')
t_start = time.perf_counter()
patience_left = epoch_patience
accuracy_best = 0
epoch_now = 1
while epoch_now <= epoch_max:
  # Word2Vec - training
  print(SUBPROCESS_FORMAT, f'Learning | Epoch = {epoch_now}/{epoch_max}', end=' | ')
  t_epoch_start = time.perf_counter()
  model.train(corpus_file=corpus_file, total_words=total_words, epochs=1, alpha=0.01, sample=0.01)
  t_elapsed = time.perf_counter()-t_start
  t_epoch = time.perf_counter()-t_epoch_start
  print(f'Elapsed {t_elapsed:.3f}s (+{t_epoch:.3f}s)', end = ' -- ')

  # Word2Vec - validate
  TP = FP = TN = FN = 0
  for data in data_valid['value']:
    [id1, id2, target] = data
    output = (target + 1) % 2
    try: output = model.wv.similarity(id1, id2)
    except: pass
    if output < 0.5:
      if target == 0: TN += 1
      else: FN += 1
    else:
      if target == 1: TP += 1
      else: FP += 1
  total_data = (TP+FP+TN+FN)
  accuracy = (TN+TP)/total_data
  train_stat[model_key]['accuracy'].append(accuracy)
  print(f'Accuracy = {accuracy:.3f}', end=' | ')
  
  # check best model local
  if accuracy > accuracy_best:
    accuracy_best = accuracy
    epoch_best = epoch_now
    patience_left = epoch_patience
    print(f'✅ Local best -> Patience = {patience_left}', end=' ')
    # saving model
    model.save(best_model_path)
  
  print()
  
  epoch_now += 1
  # early stop
  if epoch_now > epoch_min:
    curr_F = train_stat[model_key]['accuracy'][-1]
    last_F = train_stat[model_key]['accuracy'][-2]
    if (curr_F < last_F):
      patience_left -= 1
      print(f'⛔️ Negative learning', end=' ')
      if patience_left == 0:
        print('-> Patience = 0 -- Early stopping')
        break
      else:
        print(f'-> Patience left = {patience_left}')

# Print best model
print('\n✅ FINISHED LEARNING')
for key, value in train_stat.items():
  max_acc = max(value['accuracy'])
  print(f'Best accuracy for model {key} = {max_acc}')
  max_accuracies[key] = max_acc
params['result'][str(n_playlist)]['best_model_path'] = best_model_path
print(f'model saved to: {best_model_path}')

# Save all-accuracy
legend_tag = []
plt.clf()
for key, stat in train_stat.items():
  plt.plot(stat['accuracy'])
  legend_tag.append(f'Model {key}')
plt.xticks(rotation = 90)
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.title(f'Word2Vec - Accuracy')
plt.legend(legend_tag, loc='lower right')
path_save = path_track_sim + f'/train_accuracy.png'
plt.savefig(path_save, bbox_inches='tight')
# os.system('open ' + f'{path_save}'.replace(' ','\ '))

# Save each-accuracy
for key, stat in train_stat.items():
  legend_tag = []
  plt.clf()
  plt.plot(stat['accuracy'])
  legend_tag.append(f'Model {key}')
  plt.xticks(rotation = 90)
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.title(f'Word2Vec - Accuracy {key}')
  plt.legend(legend_tag, loc='lower right')
  path_save = path_track_sim + f'/train_accuracy_{key}.png'
  plt.savefig(path_save, bbox_inches='tight')
  # os.system('open ' + f'{path_save}'.replace(' ','\ '))

# JSON SAVE
json.dump(train_stat, open(path_track_sim + f'/train_stat.json', 'w'), indent=2)
json.dump(max_accuracies, open(path_track_sim + f'/max_accuracies.json', 'w'), indent=2)
json.dump(params, open('params.json', 'w'), indent=2)