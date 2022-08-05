import os, csv, time

# General Variables
READING_STRING = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_STRING = '\033[92m' + 'Export:' + '\033[0m'
root_path = os.getcwd()
titles = {}

# Reading playlists.csv dataset
csv_name = 'playlists.csv'
with open(root_path + '/data/data-all/' + csv_name) as csv_file:
    # starting
    print(READING_STRING, csv_name)
    print('Please wait...', end='\r')
    start_time = time.time()
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        if is_at_header:
            is_at_header = False
        else:
            titles[row[1]] = None
    time_elapsed = '{:.2f}'.format(time.time()-start_time)
    print(f'in {time_elapsed}s')

# Writing to titles.csv
csv_name = 'titles.csv'
with open(root_path + '/data/data-all/' + csv_name, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, csv_name)
    print('Please wait...', end='\r')
    start_time = time.time()
    writer = csv.writer(f)
    # write header
    header = ['title']
    writer.writerow(header)
    # write content
    sorted_titles = sorted(titles.keys())
    total = len(titles)
    print('Please wait...', end='\r')
    for title in sorted_titles:
        writer.writerow([title])
    time_elapsed = '{:.2f}'.format(time.time()-start_time)
    print(f'in {time_elapsed}s')