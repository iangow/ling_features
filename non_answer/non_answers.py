#!/usr/bin/env python3
import re
import json
import re
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
import pandas as pd

def makeWordLists(file):

    # helper function for assembling regexes from dictionary files
    # takes in a file that has one word/phrase per line
    # produces (word1|word2|word with space3|...|wordN)
    def makeRegexList(lsFile):
        regex_list = "("
        with open(os.path.join(_HERE, lsFile)) as listFile:
            for line in listFile:
                line = line.strip()
                regex_list += line
                regex_list += "|"
        regex_list = regex_list[:-1]
        regex_list += ")"
        return regex_list

    word_lists = {}
    with open(file) as f:
        # get the word lists from the file
        for line in f:
            line = line.strip()

            if len(line) > 0 and line[0] != '#':
                tmp = line.split("=")
                word_lists[tmp[0]] = makeRegexList(tmp[1])
    return word_lists

########################
# Assemble the regexes #
########################

word_lists = makeWordLists(os.path.join(_HERE, "word_lists.txt"))

def assembleRegexes(word_lists, regex_file):
    regexes = []

    # assemble the regexes
    with open(regex_file) as f:
        regex_id = 0
        regex_flavor = 'UNKNOWN'
        for line in f:
            line = line.strip()

            # Skip empty lines o
            if len(line) == 0 or line[0] == '#':
                continue
            elif line.startswith('TYPE'):
                tmp = line.split("=")
                regex_flavor = tmp[1]
                continue
            else:

                for word_set in word_lists.keys():
                    line = line.replace(word_set, word_lists[word_set])
                regexes.append({ 'regex_id': regex_id, 'category': regex_flavor, 'pattern': line,
                                're': re.compile(line)})
                regex_id = regex_id + 1
    return regexes

regexes = assembleRegexes(word_lists, os.path.join(_HERE, "regex.txt"))

def non_answers(sents):
    """sents is a list of sentences returned by nltk.sent_tokenize"""
    matches = [{'regex_id': r['regex_id'],
                'sentence': s,
                'phrase': r['re'].search(s).group() }
                for s in sents
                    for r in regexes
                        if r['re'].search(s) is not None]

    if not matches:
        return None
    else:
        return [json.dumps(match) for match in matches]

def get_regexes_df():
    regexes_df = pd.DataFrame(regexes)
    regexes_df = regexes_df.drop(['re'], axis=1)
    return regexes_df

if __name__ == "__main__":
    sents = ["I refuse to answer that.",
             "I don't know about that.",
             "We expect profits of $123 million.",
             "Let me get back to you on that."]

    res = non_answers(sents)

    for r in res:
        print(r)
