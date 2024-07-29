import mmh3
import numpy as np
import pandas as pd
import math
from collections import defaultdict
import matplotlib.pyplot as plt
from tqdm import tqdm
class PAS:
    '''
      m: the number of filter units in PAF
      pre_lst: the pre-sampling rates
      post_lst: the sampling rates of each non-duplicate passed by first stage
      max_prior: the maximum flow priority
    '''
    def __init__(self, m, pre_lst, post_lst, max_prior):
        self.pre_sampling_lst = pre_lst
        #self.pre_sample_seed = 21321
        #self.sample_seed = 98123
        self.hash_seed = 13123
        self.m = m
        self.max_prior = max_prior
        self.pre_p = pre_lst
        self.post_p = post_lst
        # overall sampling rates for different priority flow sets
        self.prob_lst = [round(self.pre_p[i] * self.post_p[i] - 0.0001, 3) for i in range(self.max_prior)]
        print("Overall sampling rates are ", self.prob_lst)
        self.R = np.zeros(shape = (self.m, ), dtype = np.int8)  # PAF
        self.c = np.zeros(shape = (self.max_prior, ), dtype = np.int32) # monitors
        self.are = 0
        self.flow_count = 0
        self.are_dict = {}
        self.fine_are_dict = {}
        self.class_are_dict = {'low':0, 'high':0}
        self.real_set_dict = {}
        self.flow_count_dict = {}
        self.flow_count_p = {'low':0, 'high':0}
        self.real_dict = {}
        self.pred_dict = {}
        self.hash_table = {}
        self.mea_T = 0
        self.color_table = ['red', 'green', 'blue', 'c', 'pink', 'purple', 'orange', 'crimson', 'skyblue', 'chocolate', 'violet', 'navy']
        self.color_lst = [self.color_table[i] for i in range(self.max_prior)]
        self.downloads = 0
        for i in range(1, self.max_prior + 1):
            self.flow_count_dict[i] = 0
        for i in range(1, self.max_prior + 1):
            self.are_dict[i] = 0
            self.fine_are_dict[i] = {0:0 ,1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
            self.real_dict[i] = defaultdict(int)
            self.pred_dict[i] = defaultdict(int)
            self.real_set_dict[i] = defaultdict(set)
            self.hash_table[i] = defaultdict(int)

    def update(self, src, dst, p):
        pre_sample_idx = mmh3.hash(src + dst, seed = self.hash_seed) % 0xffffffff
        if pre_sample_idx > self.pre_sampling_lst[p - 1] * 0xffffffff:
            return
        #hash_idx = mmh3.hash(src + dst, seed = self.hash_seed) % self.m
        hash_idx = pre_sample_idx % self.m
        if self.R[hash_idx] < p:
            if self.R[hash_idx] != 0:
                self.c[self.R[hash_idx] - 1] -= 1
            self.R[hash_idx] = p
            self.c[p - 1] += 1
            #sample_idx = mmh3.hash(src + dst, seed = self.sample_seed) % 0xffffffff
            if hash_idx <= self.post_p[p - 1] * self.m:
                self.hash_table[p][src] += 1
                self.downloads += 1
            sum_ = 0
            for j in range(p - 1, self.max_prior):
                sum_ += self.c[j]
            self.post_p[p - 1] = (self.m * self.prob_lst[p - 1]) / (self.m - sum_) / self.pre_sampling_lst[p - 1]

    def estimate(self, src):
        for i in range(1, self.max_prior + 1):
            if src in self.hash_table[i]:
                return int(self.hash_table[i][src] / self.prob_lst[i - 1])
        else:
            return 0

    def run(self, filename):
        f = open(filename, 'r')
        data = f.readlines()
        for pkt in tqdm(data):
            src, dst, p = pkt.split()
            p = int(p)
            self.real_set_dict[p][src].add(dst)
            self.update(src, dst, p)
        for i in range(1, self.max_prior + 1):
            for key in tqdm(self.real_set_dict[i]):
                if len(self.real_set_dict[i][key]) >= self.mea_T:
                    self.real_dict[i][key] = len(self.real_set_dict[i][key])
                    self.pred_dict[i][key] = self.estimate(key)
        f.close()
        return self.real_dict, self.pred_dict