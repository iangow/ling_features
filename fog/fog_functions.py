import re, nltk, sys
import string
from nltk.corpus import cmudict

dic = cmudict.dict()

def nsyl(word):
    if word in dic:
        prons = dic[word]
        num_syls = [len([syl for syl in pron if re.findall('[0-9]', syl)]) for pron in prons]
        return max(num_syls)
    else:
        return 0 # Needed this to get function to work; not sure what the best way is

def fog(the_text):
    sents = nltk.sent_tokenize(the_text)
    words = [word.lower() for sent in sents
                for word in nltk.word_tokenize(sent) if re.findall('[a-zA-Z]', word)]

    # Require words to be more than three characters. Otherwise, "edu"="E-D-U" => 3 syllables
    complex_words = [word for word in words if nsyl(word)>=3 and len(word)>3]
    if len(words) > 0 and len(sents) > 0:
        fog = 0.4 * (100.0*len(complex_words)/len(words) + 1.0*len(words)/len(sents))
        the_dict = {'fog':fog, 'complex_words': len(complex_words), 'fog_words': len(words),
                    'fog_sents': len(sents)}
        return the_dict
