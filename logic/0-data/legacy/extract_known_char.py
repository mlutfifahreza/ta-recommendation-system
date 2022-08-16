import os, csv, time, re

# General Variables
READING_FORMAT = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_FORMAT = '\033[92m' + 'Export:' + '\033[0m'
path_root = os.getcwd()
chars = {}

# Reading titles.csv dataset
csv_name = 'titles.csv'
with open(path_root + '/data/data-all/' + csv_name) as csv_file:
    # starting
    print(READING_FORMAT, csv_name)
    print('Please wait...', end='\r')
    start_time = time.perf_counter()
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_at_header = True
    for row in csv_reader:
        if is_at_header: is_at_header = False
        else:
            title = row[0]
            for ch in title:
                chars[ch] = None
                # if not(re.match(r'[0-9a-zA-Z]', ch)): chars[ch] = None
    time_elapsed = '{:.3f}'.format(time.perf_counter()-start_time)
    print(f'in {time_elapsed}s')

# Writing to known_characters.csv
csv_name = 'known_characters.csv'
with open(path_root + '/data/data-all/' + csv_name, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_FORMAT, csv_name)
    print('Please wait...', end='\r')
    start_time = time.perf_counter()
    writer = csv.writer(f)
    # write header
    header = ['character']
    writer.writerow(header)
    # write content
    sorted_chars = sorted(chars)
    total = len(chars)
    for ch in sorted_chars:
        writer.writerow([ch])
    time_elapsed = '{:.3f}'.format(time.perf_counter()-start_time)
    print(f'in {time_elapsed}s')