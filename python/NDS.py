import mmh3
import numpy as np
import pandas as pd
import math
from collections import defaultdict
import matplotlib.pyplot as plt
from tqdm import tqdm
'''
  Python implementation of Non-duplicate Sampling
'''
class NDS:
    '''
        prob: the overall sampling rate of NDS
        post_rate: the post sampling rate of NDS
        B: the Bloom filter of NDS
        k: the number of hash functions
        c: the counter used to count 1-bits in Bloom filter
        m: the total bits of Bloom filter in NDS
        N: the number of non-duplicates before measurement, which can be preset as a large value, e.g., 30000000
    '''
    def __init__(self, prob, m, max_prior):
        self.prob = prob
        self.post_rate = prob
        self.m = m
        self.c = 0
        self.max_prior = max_prior
        self.k = 1 #math.ceil(np.log(2) * (m / N))
        self.B = np.zeros(shape = (self.m,), dtype = np.int32)
        # the hash seeds used to map each item to bloom filter
        self.hash_seeds = [ np.random.randint(i * 10000, (i + 1) * 10000) for i in range(self.k)]
        self.sample_seed = 34324  # this hash seed, which can be set to another random value
                                  # needs to be fed into the post-sampling hash function
        self.hash_table = {}
        self.downloads = 0        # the number of non-duplicates downloaded from on-chip memory
        for i in range(1, self.max_prior + 1):
            self.hash_table[i] = defaultdict(int) # deployed at the off-chip memory in real scenario
        self.real_spread_sets = {}
        self.real_spreads = {}
        self.pred_spreads = {}
        for i in range(1, self.max_prior + 1):
            self.real_spread_sets[i] = defaultdict(set)
            self.real_spreads[i] = {}
            self.pred_spreads[i] = {}
        print("On-chip memory is {}KB.".format(m / 8 / 1024))

    def update(self, src, dst, p):
        flag = False         # Suppose this element is a duplicate
        for i in range(self.k):
            idx = mmh3.hash(src + dst, seed = self.hash_seeds[i]) % self.m
            if self.B[idx] == 0:
                self.B[idx] = 1
                self.c += 1
                flag = True  # this element is deemed as a non-duplicate
        if flag == True:
            if mmh3.hash(src + dst, seed = self.sample_seed) % 0xffffffff <= self.post_rate * 0xffffffff:
                self.hash_table[p][src] += 1
                self.downloads += 1
                self.post_rate = self.prob / (1 - (self.c / self.m) ** self.k)

    def estimate(self, src):
        for i in range(1, self.max_prior + 1):
            if src in self.hash_table[i]:
                return int(self.hash_table[i][src] / self.prob)
        else:
            return 0

    def run(self, filename):
        f = open(filename, 'r')
        datas = f.readlines()
        for row in tqdm(datas):
            src, dst, p = row.split()
            p = int(p)
            self.update(src, dst, p)
            self.real_spread_sets[p][src].add(dst)
        for i in range(1, self.max_prior + 1):
            for key in self.real_spread_sets[i]:
                if len(self.real_spread_sets[i][key]) >= 0:
                    self.real_spreads[i][key] = len(self.real_spread_sets[i][key])
                    self.pred_spreads[i][key] = self.estimate(key)
        f.close()
        return self.real_spreads, self.pred_spreads