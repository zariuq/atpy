import subprocess
import re
import os
import numpy as np
from sklearn.neighbors import NearestNeighbors
from .. import enigma

BASE_PATH = '/local1/zar/WATCH-ENIGMA/'

# Read a 00SOLVED results file and return #-name and name-# dictionaries
def get_problems(problem_list_location):
    with open(problem_list_location) as f:
        pl = re.findall('(\w+\.p)\n', f.read())
    problem_dic_num_to_key = dict(enumerate(pl))
    problem_dic_key_to_num = {problem_name:num for (num, problem_name) in problem_dic_num_to_key.items()}
    return problem_dic_num_to_key, problem_dic_key_to_num

# Encome features in a file (joining all clauses) into a vector.
def encode_features(pre, emap, strict=True):
    vector = {}
    for pr in pre:
        (_,clause,_) = pr.strip().split("|")
        enigma.trains.count(clause.strip().split(" "), vector, emap, 0, strict)
    indices, counts = zip(*vector.items())
    vector = np.zeros(len(emap) + 1)
    vector[list(indices)] = list(counts)
    return vector

# Given a list of problems solved, an emap, and a directory of feature files
# Return the {num:feature vectors}, and a feature_array
def get_features(problems, emap, directory):
    problem_features = dict()
    for num, problem in problems.items():
        path = os.path.join(BASE_PATH, directory, "{0}.fea".format(problem))
        problem_features[num] = encode_features(file(path), emap)
    feature_array = np.zeros( (len(problem_features), len(problem_features[0])) ) # [samples, features]
    for index, features in problem_features.items():
        feature_array[index] = features
    return problem_features, feature_array

# Given feature array and returns a knn-recommender
def init_fit(feature_array, n_neighbors=32):
    krec = NearestNeighbors(n_neighbors)
    krec.fit(feature_array)
    return krec

# Given feature array returns the recommendations
def get_rec(feature_array, krec, problems, kproblems, n_neighbors=32):
    rec_names = dict()
    rec = krec.kneighbors(feature_array, return_distance=False)
    for i in range(rec.shape[0]):
        rec_names[problems[i]] = [kproblems[j] for j in rec[i]]
    return rec_names

# Given rkeys (bid, limit, pid) and recommendations, 
# Make a watchlist with the recommendations and all other entries cnf(empty,axiom,\$false). 
def mk_watchlists(bid, limit, pid, recs, empty="empty.mptpC", prefix="knn-", wldir="watchlists"):
    subprocess.call('rm -fr {0}/{1}/{2}/{3}{4}'.format(wldir, bid, limit, prefix, pid), shell=True)
    subprocess.call('mkdir -p {0}/{1}/{2}/{3}{4}'.format(wldir, bid, limit, prefix, pid), shell=True)
    for problem, recl in recs.items():
        wpl = '{0}/{1}/{2}/{3}{4}/{5}'.format(wldir, bid, limit, prefix, pid, problem)
        subprocess.call('cp -r {0}/{1} {2}'.format(wldir, empty, wpl), shell=True)
        for rec in recl:
            subprocess.call('cat 00RESULTS/{0}/{1}/{2}/{3}.out | grep "^cnf" | grep trainpos >> {4}/{3}'.format(bid, limit, pid, rec, wpl), shell=True)


