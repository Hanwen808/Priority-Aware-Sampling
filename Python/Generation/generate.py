import numpy as np
from collections import defaultdict
import math
import mmh3
import pickle
from tqdm import tqdm
'''
  This program is used to generate datasets (Uniform and Zipf prioritization)
  While generating the optimal pre-sampling rates and post-sampling rates for PAS
'''
# Generate the same dataset every time
hash_seed = 51241
# filename: the original dataset
# dir_name: the target directory
# max_priority: the maximum flow priority
def generate_dataset(filename, dir_name, max_priority):
    f = open(filename, 'r')
    cnt = 0 # Unique identifier for each packet
    datas = f.readlines()
    f.close()
    total_ = len(datas)
    p_flow = defaultdict(set)
    real_spread_set = defaultdict(set)
    real_spreads = defaultdict(int)
    p_flow_table = defaultdict(int)
    f_write = open("../data/{}/00_{}.txt".format(dir_name, max_priority), 'w')
    for pkt in tqdm(datas):
        src, dst = pkt.split()
        real_spread_set[src].add(dst)
    for src in tqdm(real_spread_set):
        real_spreads[src] = len(real_spread_set[src])
    for src in tqdm(real_spread_set):
        p = mmh3.hash(str(cnt), seed = hash_seed, signed = False) % max_priority + 1
        cnt += 1
        p_flow_table[src] = p
    for pkt in tqdm(datas):
        src, dst = pkt.split()
        p = p_flow_table[src]
        p_flow[p].add(src)
        row = pkt.strip('\n') + " " + str(p) + '\n'
        f_write.write(row)
    f_write.close()
    print("Successfully generated a uniformly distributed priority dataset {}.".format("./data/{}/00_{}.txt".format(dir_name, max_priority)))
    real_spreads_file = open("../data/records/real_spreads_{}.pickle".format(dir_name),'wb')
    pickle.dump(real_spreads, real_spreads_file)
    real_spreads_file.close()
    real_flow_priority_file = open("../data/records/real_map_{}.pickle".format(dir_name), 'wb')
    pickle.dump(p_flow, real_flow_priority_file)
    real_flow_priority_file.close()

# filename1: A pkl file that stores the true flow cardinality information (./data/records/)
# filename2: A pkl file that preserves the mapping relationship between flow and priority
# units: the number of filter units in the on-chip memory
# max_priority: the supported maximum flow priority
def get_optimal_sampling_rates(filename1, filename2, units, max_priority):
    real_spreads_file = open(filename1,'rb')
    p_flow_file = open(filename2, 'rb')
    real_spreads = pickle.load(real_spreads_file)
    p_flow = pickle.load(p_flow_file)
    real_spreads_file.close()
    p_flow_file.close()
    sum_spread_dict = defaultdict(int)
    for i in range(1, max_priority + 1):
        for src in p_flow[i]:
            sum_spread_dict[i] += real_spreads[src]
    r_1_lst = {} # pre-sampling rates
    r_2_lst = {} # post-sampling rates
    for i in range(1, max_priority + 1):
        r_1_lst[i] = 0
        r_2_lst[i] = 0
    for i in range(1, max_priority + 1):
        r_1_lst[i] = min(1, units / sum_spread_dict[i])
    for i in range(1, max_priority + 1):
        sum_ = 0
        for j in range(i, max_priority + 1):
            sum_ += sum_spread_dict[j] * r_1_lst[j]
        sum_ = sum_ / units
        r_2_lst[i] = np.e ** (- sum_)
    res1 = []
    res2 = []
    overall = []
    for i in range(1, max_priority + 1):
        res1.append(r_1_lst[i])
        res2.append(r_2_lst[i])
    print(res1)
    print(res2)
    for i in range(max_priority):
        overall.append(res1[i] * res2[i])
    print("Overall sampling rates ", [round(x, 4)for x in overall])
    return res1, res2

def zipf(alpha, gamma, filename, dir_name):
    real_spread_set = defaultdict(set)
    real_spreads = defaultdict(int)
    f = open(filename, 'r')
    packets = f.readlines()
    f.close()
    for pkt in tqdm(packets):
        src, dst = pkt.split()
        real_spread_set[src].add(dst)
    for src in tqdm(real_spread_set):
        real_spreads[src] = len(real_spread_set[src])
    real_spreads_sorted = sorted(real_spreads.items(), key = lambda x : x[1], reverse = True)
    datas = [item[0] for item in real_spreads_sorted]
    b_part, sum_ = 0, 0
    sum_vec = [0]
    flow_len = len(datas)
    key_lst = []
    flow_p_dict = defaultdict(int)
    for key in tqdm(datas):
        key_lst.append(key)
    priority_rank_lst = []
    for i in range(1, gamma + 1):
        b_part += (1 / i) ** alpha
    for x in range(gamma, 0, -1):
        a_part = x ** alpha
        res = 1 / (a_part * b_part)
        sum_ += res
        sum_vec.append(sum_)
    for i in range(len(sum_vec)):
        priority_rank_lst.append(sum_vec[i] * flow_len)
    for i in range(flow_len):
        for j in range(1, len(priority_rank_lst)):
            if i < priority_rank_lst[j]:
                flow_p_dict[key_lst[i]] = gamma - j + 1
                break
    filename = "../data/{}/00_zipf_gamma={}_alpha={}.txt".format(dir_name, gamma, alpha)
    f = open(filename, 'w')
    for row in tqdm(packets):
        src, dst = row.split()
        f.write(src + " " + dst + " " + str(flow_p_dict[src]) + '\n')
    f.close()
    inverse_table = defaultdict(set)
    for src in tqdm(flow_p_dict):
        inverse_table[flow_p_dict[src]].add(src)
    inverse_int_table = defaultdict(int)
    sum_n = 0
    for p in inverse_table:
        inverse_int_table[p] = len(inverse_table[p])
        sum_n += inverse_int_table[p]
    print("sum_", sum_n)
    return flow_p_dict, inverse_int_table, inverse_table

def generate_caida_2019_uniform(n):
    filename = "../19_0.txt"
    dir_name = "caida_2019"
    generate_dataset(filename, dir_name, n)

def generate_caida_2016_uniform(n):
    filename = "../00.txt"
    dir_name = "caida_2016"
    generate_dataset(filename, dir_name, n)

# M is the on-chip memory
# n is the maximum flow priority
def get_opt_caida_2016(M, n):
    b = int(math.log2((n))) + 1
    filename1 = "../data/records/real_spreads_caida_2016.pickle"
    filename2 = "../data/records/real_map_caida_2016.pickle"
    pre, post = get_optimal_sampling_rates(filename1, filename2, M * 1024 * 8 // b, n)
    print("The optimal pre-sampling rates are ", pre)
    print("The optimal post-sampling rates are ", post)

def get_opt_caida_2019(M, n):
    b = int(math.log2((n))) + 1
    filename1 = "../data/records/real_spreads_caida_2019.pickle"
    filename2 = "../data/records/real_map_caida_2019.pickle"
    pre, post = get_optimal_sampling_rates(filename1, filename2, M * 1024 * 8 // b, n)
    print("The optimal pre-sampling rates are ", pre)
    print("The optimal post-sampling rates are ", post)

'''
  M is the on-chip memory
  n is the maximum priority
  alpha is the skewness of zipf distribution
  gamma is equal to n
'''
def get_opt_caida_2016_zipf(M, n, alpha, gamma):
    filename = "../00.txt"
    dir_name = "caida_2016"
    units = M * 1024 * 8 // (int(math.log2(n)) + 1)
    sum_spread_dict = defaultdict(int)
    real_spread_filename = "../data/records/real_spreads_caida_2016.pickle"
    f = open(real_spread_filename, 'rb')
    real_spreads = pickle.load(f)
    flow_p_table, num_dict, p_dict = zipf(alpha, gamma, filename, dir_name)
    for i in range(1, n + 1):
        for src in p_dict[i]:
            sum_spread_dict[i] += real_spreads[src]
    r_1_lst = {} # pre-sampling rates
    r_2_lst = {} # post-sampling rates
    for i in range(1, n + 1):
        r_1_lst[i] = 0
        r_2_lst[i] = 0
    for i in range(1, n + 1):
        r_1_lst[i] = min(1, units / sum_spread_dict[i] if sum_spread_dict[i] != 0 else 1)
    for i in range(1, n + 1):
        sum_ = 0
        for j in range(i, n + 1):
            sum_ += sum_spread_dict[j] * r_1_lst[j]
        sum_ = sum_ / units
        r_2_lst[i] = np.e ** (- sum_)
    res1 = []
    res2 = []
    overall = []
    for i in range(1, n + 1):
        res1.append(r_1_lst[i])
        res2.append(r_2_lst[i])
    print(res1)
    print(res2)
    for i in range(n):
        overall.append(res1[i] * res2[i])
    print("Overall sampling rates ", [round(x, 4)for x in overall])
    return res1, res2

def get_opt_caida_2019_zipf(M, n, alpha, gamma):
    filename = "../19_0.txt"
    dir_name = "caida_2019"
    units = M * 1024 * 8 // (int(math.log2(n)) + 1)
    sum_spread_dict = defaultdict(int)
    real_spread_filename = "../data/records/real_spreads_caida_2019.pickle"
    f = open(real_spread_filename, 'rb')
    real_spreads = pickle.load(f)
    flow_p_table, num_dict, p_dict = zipf(alpha, gamma, filename, dir_name)
    for i in range(1, n + 1):
        for src in p_dict[i]:
            sum_spread_dict[i] += real_spreads[src]
    r_1_lst = {} # pre-sampling rates
    r_2_lst = {} # post-sampling rates
    for i in range(1, n + 1):
        r_1_lst[i] = 0
        r_2_lst[i] = 0
    for i in range(1, n + 1):
        r_1_lst[i] = min(1, units / sum_spread_dict[i] if sum_spread_dict[i] != 0 else 1)
    for i in range(1, n + 1):
        sum_ = 0
        for j in range(i, n + 1):
            sum_ += sum_spread_dict[j] * r_1_lst[j]
        sum_ = sum_ / units
        r_2_lst[i] = np.e ** (- sum_)
    res1 = []
    res2 = []
    overall = []
    for i in range(1, n + 1):
        res1.append(r_1_lst[i])
        res2.append(r_2_lst[i])
    print(res1)
    print(res2)
    for i in range(n):
        overall.append(res1[i] * res2[i])
    print("Overall sampling rates ", [round(x, 4)for x in overall])
    return res1, res2

if __name__ == '__main__':
    get_opt_caida_2019_zipf(100, 3, 3.0, 3)