import mmh3
import numpy as np
import pandas as pd
import math
from collections import defaultdict
import matplotlib.pyplot as plt
from tqdm import tqdm
from BasicFunc import gen_rand_seed, gen_hash, SpreadCollection, actual_relative_error
'''
  Python implementation of rskt2
'''
class rSkt:
    '''
    其中每个数组的组件实现为5bit的Hyperloglog
      -w: 表示每个数组的长度
      -m: 表示每个计数器中包含的HLL数目
    '''
    def __init__(self, w, m, max_prior):
        self.w = w
        self.m = m
        self.max_prior = max_prior
        self.maxval = 31               # 5bit寄存器能够表示的最大估计范围
        self.b = math.ceil(np.log2(self.m))  # 用来定位HLL数组中更新位置
        self.right_move = 32 - self.b      # 默认使用32位哈希函数
        self.left_move = 2 ** self.right_move - 1 # 掩码
        self.alpha_m_s = {16 : 0.673 , 32 : 0.697 , 64 : 0.709}  # HLL算法的参数配置
        self.alpha_m = None
        # 计算HLL的估计参数
        if self.m in self.alpha_m_s:
            self.alpha_m = self.alpha_m_s[self.m]
        else:
            self.alpha_m = 0.7213 / (1 + 1.079 / self.m)
        self.small_size = 5 / 2 * self.m  # 当HLL计算时参数估计超出范围使用
        self.large_size = 1 / 30 * 2 ** 32
        self.large_temp = 2 ** 32
        self.hash_key_seed = 12231
        self.hash_ele_seed = 23121
        self.hash_g_seed = 76512 #[np.random.randint(i * 1000, (i + 1) * 1000) for i in range(self.m)]
        self.C = np.zeros(shape = (self.w, self.m), dtype = np.int32)
        self.C1 = np.zeros(shape = (self.w, self.m), dtype = np.int32)
        self.f_p_table = defaultdict(int)
        self.flows_info = defaultdict(list)
        self.real_spread_sets = {}
        self.real_spreads = {}
        self.pred_spreads = {}
        for i in range(1, self.max_prior + 1):
            self.real_spread_sets[i] = defaultdict(set)
            self.real_spreads[i] = defaultdict(int)
            self.pred_spreads[i] = defaultdict(int)
        print("b={}. right_move={}, left_move={}".format(self.b, self.right_move, self.left_move))

    def update(self, src, dst, p):
        self.real_spread_sets[p][src].add(dst)
        hash_src_idx = mmh3.hash(src, seed = self.hash_key_seed, signed = False) % self.w
        h_e_value = mmh3.hash(dst, seed = self.hash_ele_seed, signed = False)
        h_e = (h_e_value >> self.right_move) % self.m
        q = h_e_value & self.left_move  # 计算得到最右侧哈希二进制字符串
        num = 0
        while q:
            num += 1
            q >>= 1
        num = self.right_move - num + 1
        g_f_i = mmh3.hash(src + str(h_e), self.hash_g_seed, signed=False) % 2
        if g_f_i == 0:
            self.C[hash_src_idx, h_e] = max(num, self.C[hash_src_idx, h_e])
        else:
            self.C1[hash_src_idx, h_e] = max(num, self.C1[hash_src_idx, h_e])

    def query(self, Lf, _Lf):
        sum_Lf = 0
        _sum_Lf = 0
        for i in range(self.m):
            sum_Lf += 2 ** (-Lf[i])
            _sum_Lf += 2 ** (-_Lf[i])
        Z = 1 / sum_Lf
        n = self.alpha_m * self.m ** 2 * Z
        _Z = 1 / _sum_Lf
        _n = self.alpha_m * self.m ** 2 * _Z
        if n <= self.small_size:
            V = 0
            for M in Lf:
                if M == 0:
                    V += 1
            if V:
                n = self.m * math.log(self.m / V)
        elif n > self.large_size:
            n = -self.large_temp * math.log(1 - n / self.large_temp)

        if _n <= self.small_size:
            _V = 0
            for _M in _Lf:
                if _M == 0:
                    _V += 1
            if _V:
                _n = self.m * math.log(self.m / _V)
        elif _n > self.large_size:
            _n = -self.large_temp * math.log(1 - _n / self.large_temp)

        return n,_n

    def estimate(self, src):
        h_f = mmh3.hash(src, seed = self.hash_key_seed, signed = False) % self.w
        Lf = np.zeros((self.m,))
        _Lf = np.zeros((self.m,))
        for i in range(self.m):
            g_f_i = mmh3.hash(src + str(i), self.hash_g_seed, signed = False) % 2
            if g_f_i == 0:
                Lf[i] = self.C[h_f, i]
                _Lf[i] = self.C1[h_f, i]
            else:
                Lf[i] = self.C1[h_f, i]
                _Lf[i] = self.C[h_f, i]
        n, n1 = self.query(Lf, _Lf)
        return max(round(n - n1), 1)

    def run(self, filename):
        f = open(filename, 'r')
        datas = f.readlines()
        for pkt in tqdm(datas):
            src, dst, p = pkt.strip().split()
            p = int(p)
            self.real_spread_sets[p][src].add(dst)
            self.f_p_table[src] = p
            self.update(src, dst, p)
        for i in range(1, self.max_prior + 1):
            for src in tqdm(self.real_spread_sets[i]):
                self.real_spreads[i][src] = len(set(self.real_spread_sets[i][src]))
                self.pred_spreads[i][src] = self.estimate(src)
        f.close()
        return self.real_spreads, self.pred_spreads