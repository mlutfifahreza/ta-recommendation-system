import re, demoji
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def clean(raw_title, characters_mapping):
    # initialization
    processed_title = raw_title
    
    # normalization 1: convert emojis
    emojis = demoji.findall(processed_title)
    for key, value in emojis.items():
        mapping = re.sub(r'((\w+)\s+skin tone)|(face)|(flag)|(hand)', ' ', value)
        processed_title = processed_title.replace(key, f' {mapping} ')
    
    # normalization 1: convert special characters
    for key,value in characters_mapping.items():
        processed_title = processed_title.replace(key, value)
    # replace known patterns
    processed_title = re.sub(r'(0s)', '0', processed_title)
    processed_title = re.sub(r'(0S)', '0', processed_title)
    processed_title = re.sub(r'(2k)|(2K)', '20', processed_title)
    processed_title = re.sub(r'(2o)|(2O)', '20', processed_title)
    
    # normalization 2: remove unknown characters
    processed_title = re.sub(r'[^0-9a-zA-Z]+', ' ', processed_title)

    # normalization 3: small case
    processed_title = processed_title.lower().strip()

    # tokenization
    word_tokens = word_tokenize(processed_title)

    # remove stop words and length 1 word
    stop_words = set(stopwords.words('english'))
    filtered_words = []
    for word in word_tokens:
        if (word not in stop_words
            and len(word) > 1
        ): filtered_words.append(word)

    # lemmatization
    lemmatizer = WordNetLemmatizer()
    for i in range (len(filtered_words)):
        filtered_words[i] = lemmatizer.lemmatize(filtered_words[i])

    # return
    result = ' '.join(filtered_words)
    return result