import re

def fls(a_sentence):

    fl_regex = r"will|should|can|could|may|might|expect|anticipate|"
    fl_regex += r"believe|plan|hope|intend|seek|project|forecast|objective|goal"
    fl_regex = re.compile(r"(?:\b(" + fl_regex + r"))", re.I)

    fl_pp = r"(?:expected|anticipated|forecasted|projected|believed)"
    fl_be_pp = r"(?:was|were|had|had been)"
    nfl_regex = re.compile(r"\b" + fl_be_pp + r"\s" + fl_pp, re.I)

    if re.findall(fl_regex, a_sentence) and not re.findall(nfl_regex, a_sentence):
        return True
    else:
        return False
