import re
import numpy as np
from numpy import dot
from numpy.linalg import norm

# Compute cosine similarity between two vectors
def compute_cos_sim(vector_a, vector_b):
    if not np.all(vector_a == 0) and not np.all(vector_b == 0):
        cos_sim = dot(vector_a, vector_b)/(norm(vector_a) * norm(vector_b))
    else:
        cos_sim = 0
        
    return cos_sim

# Assemble the regexes for function words 
def assemble_regexes(words):
    regex_list = {}
    
    for word in words:
        key = "func_" + re.sub("\*|\'", "_", word.lower())
        regex = r"\b(?:" + re.sub('\*(?:\s*$)?', "[a-z0-9]*(')?[a-z0-9]*", word.lower()) + r")(?=(?:[^a-zA-Z0-9_']|$))"
        regex_list[key] = re.compile(regex)
    
    return regex_list