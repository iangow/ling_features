import re

from tone.word_lists import word_lists
categories = [key for key in word_lists.keys()]

def make_regex(word_list):
    regex_text = '\\b(?:' + '|'.join(word_list) + ')\\b'
    regex = re.compile(regex_text)
    
    return regex
    
regex_dict = {cat: make_regex(word_lists[cat]) for cat in categories }

def tone_count(the_text):
    """Function to return number of matches in a category in a text"""

    text = the_text.lower()
    the_dict = {category: len(re.findall(regex_dict[category], text)) for category in categories}
    return the_dict
