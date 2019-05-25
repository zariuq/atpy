import subprocess
import re
import os
import numpy as np
import scipy.sparse as sp
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD
from collections import Counter
from functools import reduce
from .. import enigma

BASE_PATH = '/home/zar/PROOF_WATCH/'
cnf_clause_pattern = re.compile('cnf\((.+), ?(.+), ?(\(.+\))\).')
cnf_line_pattern = re.compile('(cnf\(.+, ?.+, ?\(.+\)\).)')
feature_pattern = re.compile('\*\|(.+)\|\n')


def check_and_make_dirs(path):
    if not os.path.exists(path):
	os.makedirs(path)

# Cycle through all problems given BIN/PROTOS/ARTICLE/PROBLEM structure
# Or actually just through BIN/PROTOS/PROBLEM structure -- after the trial runs on the above :p 
'''
def apply_all(f, basedir, tardir=None):
    outputs = []
    if not tardir:
        tardir = basedir
    check_and_make_dirs(tardir) 
    for protos in os.listdir(basedir):
        check_and_make_dirs(os.path.join(tardir, protos)) 
        for problem in filter(lambda n : n[-4] != '.', os.listdir('{}/{}/{}'.format(basedir, protos, article))):
            problem_location = os.path.join(basedir, protos, problem)
            target_location = os.path.join(tardir, protos, problem)
            outputs.append(f( (problem_location, target_location) ))
    return outputs
'''

#apply_all(lambda (pl, tl) : subprocess.call('enigma-features-current --free-numbers --enigma-features="VHSLC" {0} > {1}.pre'.format(pl, tl), shell=True)
#           ,'watchlists','watchlists_pre')

# Given a featurized problem file "*.pre", return a feature vector
# (problem_location, array size, clause-matrix or problem-vector)
def featurize_pre((pl, fl), (D, emap), clauses=False):
    # Get clauses data (needed to find which are part of the conjecture)
    with open('{}'.format(pl)) as f: 
        cn = cnf_clause_pattern.findall(f.read())

    with open('{}'.format(fl)) as f: 
        cf = feature_pattern.findall(f.read())

    # Make the vectors 
    def mk_vector(features, vector={}):    
        enigma.trains.count(features.split(" "), vector, emap, 0, True)
        return vector

    if clauses:
        N = len(cn)
        fvector = sp.lil_matrix((N, 2*D + 1), dtype=np.float32) # N by clause D + conjecture D + 1 (as we count from 1 not 0 and I'm lazy)
        conj_features = Counter()

        for i, features in enumerate(cf):
            cvector = Counter(mk_vector(features))
            if cn[i][1] == 'negated_conjecture':
                conj_features += cvector
            for feature_num, count in cvector.items():
                fvector[i, feature_num] = count

        for feature_num, count in conj_features.items():
            fvector[:, D + feature_num] = count

    else: 
        fvector = sp.lil_matrix((1, 2*D +1), dtype=np.float32)
        conj_features = Counter()
        vector = {}
        for i, features in enumerate(cf):
            mk_vector(features, vector)
            
            if cn[i][1] == 'negated_conjecture':
                conj_features += Counter(mk_vector(features))
    
        for feature_num, count in vector.items():
            fvector[0, feature_num] = count

        for feature_num, count in conj_features.items():
            fvector[0, D + feature_num] = count

    return fvector






