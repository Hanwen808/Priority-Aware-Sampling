from Params import *
from Sketches.BasicFunc import gen_rand_seed, gen_hash, SpreadCollection, actual_relative_error
'''
  Python implementation of Virtual Hyperloglog
'''
class vhll():
    '''
      num_phy_registers: the number of physical registers in on-chip memory
      num_registers_for_vhll: the number of virtual registers allocated to each flow
    '''
    def __init__(self, num_phy_registers, num_registers_for_vhll):
        self.num_phy_registers = num_phy_registers
        self.num_registers_for_vhll = num_registers_for_vhll
        self.f_p_table = defaultdict(int) # flow label with priority
        self.sss1 = 12
        self.sss2 = 21
        distinct_seeds = set()
        while len(distinct_seeds) < num_registers_for_vhll:
            seed_t = gen_rand_seed()
            if seed_t not in distinct_seeds:
                distinct_seeds.add(seed_t)
        self.seeds = list(distinct_seeds)
        self.range_for_seed_index = math.floor(math.log(self.num_registers_for_vhll, 2))
        self.hash_seed = gen_rand_seed()
        self.flows_info = defaultdict(list)
        self.real_spread_sets = {}
        self.real_spreads = {}
        self.pred_spreads = {}
        for i in range(1, max_priority + 1):
            self.real_spread_sets[i] = defaultdict(set)
            self.real_spreads[i] = defaultdict(int)
            self.pred_spreads[i] = defaultdict(int)
        self.phy_registers = [0 for i in range(num_phy_registers)]
        self.flows = set()

        self.spread_of_all_flows = 0
        self.alpha = 0
        if self.num_registers_for_vhll == 16:
            self.alpha = 0.673
        elif self.num_registers_for_vhll == 32:
            self.alpha = 0.697
        elif self.num_registers_for_vhll == 64:
            self.alpha = 0.709
        else:
            self.alpha = (0.7213 / (1 + (1.079 / self.num_registers_for_vhll)))

    def set(self, flow_id, ele_id):
        self.flows.add(flow_id)

        ele_hash_value = gen_hash(ele_id, self.hash_seed)
        p_part = ele_hash_value >> (32 - self.range_for_seed_index)
        q_part = ele_hash_value - (p_part << (32 - self.range_for_seed_index))

        leftmost_index = 0
        while q_part:
            leftmost_index += 1
            q_part >>= 1
        leftmost_index = 32 - self.range_for_seed_index - leftmost_index + 1

        index_for_register = gen_hash(flow_id ^ self.seeds[p_part], self.hash_seed) % self.num_phy_registers
        self.phy_registers[index_for_register] = max(self.phy_registers[index_for_register], leftmost_index)

    def update_para(self):
        fraction_zeros = 0
        sum_registers = 0
        for register in self.phy_registers:
            sum_registers += 2 ** (-register)
            if register == 0:
                fraction_zeros += 1
        fraction_zeros = fraction_zeros / self.num_phy_registers
        spread_of_all_flows = (0.7213 / (1 + (1.079 / self.num_phy_registers))) * (
                    self.num_phy_registers ** 2) / sum_registers
        if spread_of_all_flows < 2.5 * self.num_phy_registers:
            if fraction_zeros != 0:
                self.spread_of_all_flows = - self.num_phy_registers * math.log(fraction_zeros)
        elif spread_of_all_flows > 2 ** 32 / 30:
            self.spread_of_all_flows = - 2 ** 32 * math.log(1 - spread_of_all_flows / 2 ** 32)

    def estimate(self, flow_id):
        fraction_zeros_for_vhll = 0
        sum_registers_for_vhll = 0
        for seed in self.seeds:
            index_for_vhll = gen_hash(flow_id ^ seed, self.hash_seed) % self.num_phy_registers
            sum_registers_for_vhll += 2 ** (- self.phy_registers[index_for_vhll])
            if self.phy_registers[index_for_vhll] == 0:
                fraction_zeros_for_vhll += 1
        fraction_zeros_for_vhll = fraction_zeros_for_vhll / self.num_registers_for_vhll
        spread_of_the_flow = self.alpha * (self.num_registers_for_vhll ** 2) / sum_registers_for_vhll

        if spread_of_the_flow < 2.5 * self.num_registers_for_vhll:
            if fraction_zeros_for_vhll != 0:
                spread_of_the_flow = - self.num_registers_for_vhll * math.log(fraction_zeros_for_vhll) - \
                                 (self.num_registers_for_vhll * self.spread_of_all_flows / self.num_phy_registers)
            else:
                spread_of_the_flow = spread_of_the_flow - \
                                     (self.num_registers_for_vhll * self.spread_of_all_flows / self.num_phy_registers)
        elif spread_of_the_flow > 2 ** 32 / 30:
            spread_of_the_flow = - 2 ** 32 * math.log(1 - spread_of_the_flow / 2 ** 32) - \
                                 (self.num_registers_for_vhll * self.spread_of_all_flows / self.num_phy_registers)
        else:
            spread_of_the_flow = spread_of_the_flow - \
                                 (self.num_registers_for_vhll * self.spread_of_all_flows / self.num_phy_registers)

        return max(spread_of_the_flow,1)

    def get_all_spread(self):
        self.update_para()
        all_spread = {}
        for i in range(1, max_priority + 1):
            all_spread[i] = {}
        for flow_id in tqdm(self.f_p_table):
            all_spread[self.f_p_table[flow_id]][flow_id] = self.estimate(mmh3.hash(flow_id, self.sss1))
            # print(all_spread[flow_id])
        return all_spread

    def run(self, filename):
        file = open(filename, 'r')
        datas = file.readlines()
        for pkt in tqdm(datas):
            f, e, p = pkt.strip().split()
            p = int(p)
            self.real_spread_sets[p][f].add(e)
            self.f_p_table[f] = p
            f = mmh3.hash(f, self.sss1)
            e = mmh3.hash(e, self.sss2)
            self.set(f, e)
        file.close()
        for i in range(1, max_priority + 1):
            for f in self.real_spread_sets[i]:
                self.real_spreads[i][f] = len(set(self.real_spread_sets[i][f]))
        estimation = self.get_all_spread()
        return self.real_spreads, estimation