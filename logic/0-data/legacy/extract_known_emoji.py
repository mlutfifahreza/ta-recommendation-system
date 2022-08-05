import os, csv, time, demoji, re

# General Variables
READING_STRING = '\033[94m' + 'Reading:' + '\033[0m'
EXPORT_STRING = '\033[92m' + 'Export:' + '\033[0m'
root_path = os.getcwd()
titles = {}

# Reading titles.csv dataset
csv_name = 'titles.csv'
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
            titles[row[0]] = 1
    time_elapsed = '{:.2f}'.format(time.time()-start_time)
    print(f'in {time_elapsed}s\n')

# Writing to known_emojis.csv
csv_name = 'known_emojis.csv'
with open(root_path + '/data/data-all/' + csv_name, 'w', encoding = 'UTF8', newline = '') as f:
    # starting
    print(EXPORT_STRING, csv_name)
    print('Please wait...', end='\r')
    start_time = time.time()
    writer = csv.writer(f)
    # write header
    header = ['emoji','mapping']
    writer.writerow(header)
    # write content
    all_titles = ''
    for title in titles.keys():
        all_titles += f' {title}'
    emojis = demoji.findall(all_titles)
    for key, value in emojis.items():
        mapping = re.sub(r'([^\w\s])', '', value)
        mapping = re.sub(r'((\w+)\s+skin tone)|(face)|(flag)|(hand)', '', mapping).strip()
        writer.writerow([key, mapping])
    time_elapsed = '{:.2f}'.format(time.time()-start_time)
    print(f'in {time_elapsed}s\n')