import csv, json
from math import log2, floor

# String formatting
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
PROCESS_FORMAT = '\n\033[35m' + 'Process:' + '\033[0m'
SUBPROCESS_FORMAT = '\033[94m' + 'Sub-Process:' + '\033[0m'

# General Variables
params = json.load(open('params.json'))
n_playlist = params['n_playlist']
path_data_all = f'data/data_all/playlist={n_playlist}'
path_data_test = f'data/data_test/playlist={n_playlist}'
path_track_sim = f'data/model/track_sim/playlist={n_playlist}'
path_fcm = f'data/model/fcm/playlist={n_playlist}'
vector_size = params['vector_size']
# # # # # # # # # # # # # # # # # # # # # #

# prepare track detail
track_detail = {}
path_csv =  path_data_all + '/track_detail_all.csv'
with open(path_csv) as csv_file:
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    track_detail[row['track_id']] = {
      'track_name' : row['track_name'],
      'artist_id' : row['artist_id'],
      'artist_name' : row['artist_name']
    }

# read test playlists
playlists_test = json.load(open(path_data_test + '/playlists_test.json'))
playlists_reccomend = {
  'title' : json.load(open(path_data_test + '/playlists_reccomend_title.json')),
  'pop' : json.load(open(path_data_test + '/playlists_reccomend_pop.json')),
}
n_list = params['n_list']
# track only
for n in n_list:
  path_playlists_reccomend_n = path_data_test + f'/playlists_reccomend_{n}.json'
  playlists_reccomend[f'{n} only'] = json.load(open(path_playlists_reccomend_n))
# title + track
for n in n_list:
  path_playlists_reccomend_n = path_data_test + f'/playlists_reccomend_title+{n}.json'
  playlists_reccomend[f'title + {n}'] = json.load(open(path_playlists_reccomend_n))

# Evaluation functions
def r_prec(output_ids, target_ids):
  output_ids = set(output_ids)
  output_artists = set([track_detail[id]['artist_id'] for id in output_ids])
  target_ids = set(target_ids)
  target_artists = set([track_detail[id]['artist_id'] for id in target_ids])
  intersection_track = len(output_ids.intersection(target_ids))
  intersection_artist = len(output_artists.intersection(target_artists))
  return (intersection_track + 0.25 * intersection_artist) / len(target_ids)

def ndcg(output_ids, target_ids):
  if (output_ids):
    dcg = idcg = 0
    for i, value in enumerate(output_ids, start=1):
      relevance = 1 if value in target_ids else 0
      denum = log2(i + 1)
      dcg += relevance / denum
      idcg += 1 / denum
    return dcg/idcg
  else:
    return 0

def clicks(output_ids, target_ids):
  result = floor(params['n_recc']/10) + 1
  for i, value in enumerate(output_ids, start=1):
    if value in target_ids:
      result = floor((i-1)/10)
      break
  return result

# START
evaluation = {}
evaluation_csv = []
for type in playlists_reccomend:
  evaluation[type] = {
    'overall' : {
      'r_prec' : [],
      'ndcg' : [],
      'clicks' : [],
    }
  }
  for pid, tracks_value in playlists_reccomend[type].items():
    evaluation[type][pid] = {}
    output_ids = [id for id in tracks_value.keys()][:params['n_recc']]
    # eval
    target_ids = playlists_test[pid]['all']
    r_prec_val = r_prec(output_ids, target_ids)
    ndcg_val = ndcg(output_ids, target_ids)
    clicks_val = clicks(output_ids, target_ids)
    # add
    evaluation[type][pid]['r_prec'] = r_prec_val
    evaluation[type][pid]['ndcg'] = ndcg_val
    evaluation[type][pid]['clicks'] = clicks_val
    # add to overall temp
    evaluation[type]['overall']['r_prec'].append(r_prec_val)
    evaluation[type]['overall']['ndcg'].append(ndcg_val)
    evaluation[type]['overall']['clicks'].append(clicks_val)
  # overall temp: eval list 
  r_prec_list = evaluation[type]['overall']['r_prec']
  ndcg_list = evaluation[type]['overall']['ndcg']
  clicks_list = evaluation[type]['overall']['clicks']
  # update
  evaluation[type]['overall']['r_prec'] = {
    'min' : min(r_prec_list),
    'max' : max(r_prec_list),
    'avg' : sum(r_prec_list) / len(r_prec_list)
  }
  evaluation[type]['overall']['ndcg'] = {
    'min' : min(ndcg_list),
    'max' : max(ndcg_list),
    'avg' : sum(ndcg_list) / len(ndcg_list)
  }
  evaluation[type]['overall']['clicks'] = {
    'min' : min(clicks_list),
    'max' : max(clicks_list),
    'avg' : sum(clicks_list) / len(clicks_list)
  }
  print(type)
  new_eval_row = [type]
  for measurement, val in evaluation[type]['overall'].items():
    print(measurement, val)
    new_eval_row.append(val['avg'])
  evaluation_csv.append(new_eval_row)
  print()


# save evaluation
path_export = path_data_test + f'/evaluation_{vector_size}.json'
print(EXPORT_FORMAT, path_export)
json.dump(evaluation, open(path_export, 'w'), indent=2)
print(f'✅ Finished')

# Writing tracks.csv sort by id
path_csv = path_data_test + f'/evaluation.csv'
with open(path_csv, 'a+', encoding = 'UTF8', newline = '') as f:
  print(EXPORT_FORMAT, path_csv)
  writer = csv.writer(f)
  writer.writerow([str(vector_size)])
  header = ['type', 'r_prec', 'ndcg', 'clicks']
  writer.writerow(header)
  for val in evaluation_csv:
    writer.writerow(val)
  print(f'✅ Finished')
