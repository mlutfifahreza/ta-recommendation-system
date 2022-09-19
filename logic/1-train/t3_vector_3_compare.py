# import os, json
# import matplotlib.pyplot as plt

# # Parameters
# params = json.load(open('parameters.json'))
# n_playlist = params['n_playlist']

# # Paths
# path_general = f'data/general'
# path_vector = f'data/model/vector/playlist={n_playlist}'
# path_vector_1 = f'data/model/vector_1/playlist={n_playlist}'
# path_vector_2 = f'data/model/vector_2/playlist={n_playlist}'
# path_vector_3 = f'data/model/vector_3/playlist={n_playlist}'

# # Load training data
# data_valid = json.load(open(path_vector + '/data_valid.json'))
# train_stats = {
#   '1': json.load(open(path_vector_1 + '/train_stat.json')),
#   '2': json.load(open(path_vector_2 + '/train_stat.json')),
#   '3': json.load(open(path_vector_3 + '/train_stat.json')),
# }

# # Compare plot
# for k in params['embed_list']:
#   legend_tag = []
#   plt.clf()
#   for run, stat in train_stats.items():
#     plt.plot(stat[str(k)]['accuracy'])
#     legend_tag.append(f'run {run} - vector_size {k}')
#   plt.xticks(rotation = 45)
#   plt.ylabel('accuracy')
#   plt.xlabel('epoch')
#   plt.title(f'FastText - Learning (Accuracy {k})')
#   plt.legend(legend_tag, loc='lower right')
#   path_save = path_vector + f'/train_accuracy_{k}.png'
#   plt.savefig(path_save, bbox_inches='tight')
#   os.system('open ' + f'{path_save}'.replace(' ','\ '))

print("OK")