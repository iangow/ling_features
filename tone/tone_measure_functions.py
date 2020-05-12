import re
import pandas as pd
import json

def make_regex(words):
    word_list = words.lower().split(",")
    regex_text = '\\b(?:' + '|'.join(word_list) + ')\\b'
    regex = re.compile(regex_text)
    
    return regex

def re_dict():
    df = pd.read_csv("lm_words.csv")    
    categories = [key for key in regex_dict.keys()]
    regex_dict = { cat: make_regex(df['words'][df['category'] == cat].iloc[0]) for cat in categories}
    return regex_dict

def tone_count(the_text):
    # rest of function
    """Function to return number of matches in a category in a text"""
    df = pd.read_csv("lm_words.csv")    
    categories = [key for key in df['category']]
    regex_dict = { cat: make_regex(df['words'][df['category'] == cat].iloc[0]) for cat in categories}
    #regex_dict = re_dict
    text = the_text.lower()
    the_dict = {category: len(re.findall(regex_dict[category], text)) for category in categories}
  #  return json.dumps(the_dict)    
    return the_dict
