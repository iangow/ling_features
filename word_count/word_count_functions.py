import re, nltk

def word_count(raw, min_length = 1):
    """ Function to count the number of words in a passage of text.
        Supplying parameter 'min_length' gives number of words with
        at least min_length letters.
    """
    tokens = nltk.word_tokenize(raw)
    return len([word for word in tokens if len(word) >= min_length])

def number_count(raw):
    """ Function to count the number of numbers appearing in a
        passage of text.
    """
    results = re.findall(r'\b(?<=-)?[,0-9\.]+(?=\s)', raw)
    results = [result for result in results
                if not re.match(r'(199|20[01])\d', result)
                  and re.search(r'[0-9]', result)]
    return len(results)

def sent_count(raw):
    """
        Function to count the number of sentences in a passage.
    """
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sents = sent_tokenizer.tokenize(raw)
    return len(sents)
