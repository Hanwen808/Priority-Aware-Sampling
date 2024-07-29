import sys

sys.path.append("../")

from NDS import *
from PAS import *
from vHLL import *
from rSkt import *
import argparse
color_table = ['red', 'green', 'blue', 'c', 'pink', 'purple', 'orange', 'crimson', 'skyblue', 'chocolate', 'violet', 'navy']

class Experiment:
    '''
      name: algorithm's name
    '''
    def __init__(self, name, max_priority, *args):
        self.sketch = None
        self.real_dict = None
        self.pred_dict = None
        self.max_priority = max_priority
        self.flow_count = 0
        self.flow_count_dict = {}
        self.mem_ = None
        self.are_dict = defaultdict(int)
        self.are = 0
        self.fine_are_dict = {}
        self.fine_flow_count = {}
        self.class_flow_count = {}
        self.class_are_dict = {}
        self.color_lst = [color_table[i] for i in range(self.max_priority)]
        if name == "NDS":
            # args[0]: p 
            # args[1]: mem
            # args[2]: high
            # args[3]: low
            self.mem_ = int(args[1] / 8 / 1024)
            print("NDS({},{},{}) is running...".format(args[0], args[1], max_priority))
            self.sketch = NDS(args[0], args[1], max_priority)
        elif name == "vHLL" or name == "VHLL":
            # args[0]: the number of physical registers
            # args[1]: the number of virtual registers
            self.mem_ = int(args[0] * 5 / 8 / 1024)
            print("vHLL({},{},{}) is running...".format(args[0], args[1], max_priority))
            self.sketch = vhll(args[0], args[1], max_priority)
        elif name == "PAS":
            # args[0]: mem
            # args[1]: pre
            # args[2]: post
            # args[3]: prior
            # args[4]: high
            # args[5]: low
            self.mem_ = args[0]
            if args[3] == 3:
                self.mem_ = int(self.mem_ * 2 / 8 / 1024)
            elif args[3] == 7:
                self.mem_ = int(self.mem_ * 3 / 8 / 1024)
            print("PAS({},{},{},{}) is running...".format(args[0], args[1], args[2], args[3]))
            self.sketch = PAS(args[0], args[1], args[2], args[3])
        elif name.lower() == "rskt":
            # args[0]: memory KB
            # args[1]: the number of virtual registers
            self.mem_ = args[0]
            print("rSkt({},{},{}) is running...".format(self.mem_, args[1], max_priority))
            self.sketch = rSkt((self.mem_ * 8 * 1024) // (32 * 5), args[1], max_priority)
        else:
            print("Sorry, we currently do not support this type of sketch")
            exit()
        self.class_are_dict['high'] = 0
        self.class_are_dict['low'] = 0
        self.class_flow_count['high'] = 0
        self.class_flow_count['low'] = 0
        for i in range(1, max_priority + 1):
            self.fine_are_dict[i] = {}
            self.fine_flow_count[i] = {}
            self.flow_count_dict[i] = 0
            for j in range(8):
                self.fine_are_dict[i][j] = 0
                self.fine_flow_count[i][j] = 0

    def run(self, filename):
        print("Running {} datasets...".format(filename))
        self.real_dict, self.pred_dict = self.sketch.run(filename)
        print("Finished!")

    def draw(self, name, dataset, high_prior_flows, low_prior_flows):
        x = np.arange(0, 7, 1)
        for i in range(1, self.max_priority + 1):
            x_log, y_log = [], []
            for key in self.real_dict[i]:
                temp_are = abs(self.pred_dict[i][key] - self.real_dict[i][key]) / self.real_dict[i][key]
                self.are_dict[i] += temp_are
                self.flow_count_dict[i] += 1
                self.are += temp_are
                self.flow_count += 1
                spread_est_log = int(round(math.log10(self.real_dict[i][key])))
                self.fine_flow_count[i][spread_est_log] += 1
                self.fine_are_dict[i][spread_est_log] += temp_are
                if i in high_prior_flows:
                    self.class_are_dict['high'] += temp_are
                    self.class_flow_count['high'] += 1
                elif i in low_prior_flows:
                    self.class_are_dict['low'] += temp_are
                    self.class_flow_count['low'] += 1
                x_log.append(self.real_dict[i][key])
                y_log.append(self.pred_dict[i][key])
            x_log = np.log10(x_log)
            y_log = np.log10(y_log)
            plt.plot(x_log, y_log, '*', color = self.color_lst[i - 1], label = "$F_{}$".format(i))
        for i in range(1, self.max_priority + 1):
            self.are_dict[i] = self.are_dict[i] / self.flow_count_dict[i] if self.flow_count_dict[i] != 0 else None
            for j in range(8):
                self.fine_are_dict[i][j] = self.fine_are_dict[i][j] / self.fine_flow_count[i][j] if self.fine_flow_count[i][j] != 0 else None
        self.class_are_dict['high'] = self.class_are_dict['high'] / self.class_flow_count['high'] if self.class_flow_count['high'] != 0 else None
        self.class_are_dict['low'] = self.class_are_dict['low'] / self.class_flow_count['low'] if self.class_flow_count['low'] != 0 else None
        plt.plot(x, x)
        plt.rcParams.update({'font.size': 18})
        plt.legend(ncol = 2, shadow = False, fancybox= False, frameon = False,)
        plt.xticks(x, ["$10^{}$".format(i) for i in range(7)],fontsize = 24)
        plt.yticks(x, ["$10^{}$".format(i) for i in range(7)],fontsize = 24)
        plt.xlabel("Real Spreads", fontsize = 24)
        plt.ylabel("Estimated Spreads", fontsize = 24)
        plt.tight_layout()
        plt.savefig("../records/exp_accuracy/{}_{}_{}_{}.jpg".format(name, dataset, self.max_priority, self.mem_))
        #plt.show()
        filename = "../records/exp_accuracy/{}_{}_{}_{}.txt".format(name, dataset, self.max_priority, self.mem_)
        f = open(filename, 'w')
        for i in range(1, self.max_priority + 1):
            f.write("The are of {}-priority flows is {}.\n".format(i, self.are_dict[i]))
            for j in range(8):
                if self.fine_are_dict[i][j] == None:
                    continue
                f.write("  The are of [$10^{}$,$10^{}$) is {}.\n".format(j, j + 1, self.fine_are_dict[i][j]))
        f.write("The are of high-priority flows is {}.\n".format(self.class_are_dict['high']))
        f.write("The are of low-priority flows is {}.\n".format(self.class_are_dict['low']))
        f.write("Total ARE is {}.\n".format(self.are / self.flow_count))
        f.close()
        
def nds_demo(p, mem_, prior, dataset, highs, lows):
    exp = Experiment("NDS", prior, p, int(mem_ * 1024 * 8))
    if dataset == 2019:
        if prior == 7:
            exp.run("../runtime_dataset/caida_2019/00_7.txt")
        elif prior == 3:
            exp.run("../runtime_dataset/caida_2019/00_3.txt")
    elif dataset == 2016:
        if prior == 7:
            exp.run("../runtime_dataset/caida_2016/00_7.txt")
        elif prior == 3:
            exp.run("../runtime_dataset/caida_2016/00_3.txt")
    exp.draw("nds", dataset, highs, lows)

def rskt_demo(mem_, prior, v, dataset, highs, lows):
    exp = Experiment("rSkt", prior, int(mem_), v)
    if dataset == 2019:
        if prior == 7:
            exp.run("../runtime_dataset/caida_2019/00_7.txt")
        elif prior == 3:
            exp.run("../runtime_dataset/caida_2019/00_3.txt")
    elif dataset == 2016:
        if prior == 7:
            exp.run("../runtime_dataset/caida_2016/00_7.txt")
        elif prior == 3:
            exp.run("../runtime_dataset/caida_2016/00_3.txt")
    exp.draw("rSkt", dataset, highs, lows)

def vhll_demo(mem_, v, prior, dataset, highs, lows):
    p1 = int(mem_ * 2 ** 13 / 5)
    p2 = v
    exp = Experiment("vHLL", prior, p1, p2)
    if dataset == 2019:
        if prior == 7:
            exp.run("../runtime_dataset/caida_2019/00_7.txt")
        elif prior == 3:
            exp.run("../runtime_dataset/caida_2019/00_3.txt")
    elif dataset == 2016:
        if prior == 7:
            exp.run("../runtime_dataset/caida_2016/00_7.txt")
        elif prior == 3:
            exp.run("../runtime_dataset/caida_2016/00_3.txt")
    exp.draw("vhll", dataset, highs, lows)

def pas_demo(mem_kb, prior, pre, post, dataset, highs, lows):
    p1 = None
    if prior == 3:
        p1 = int(mem_kb * 1024 * 8 // 2)
    elif prior == 7:
        p1 = int(mem_kb * 1024 * 8 // 3)
    else:
        print("Sorry, this code only support 3 and 7 priorities.")
        return
    p2 = pre #[1, 1, 1, 1, 1, 1, 1]
    p3 = post #[0.039870228769679786, 0.05425990763315014, 0.08353920308331102, 0.12519484958411123, 0.22027212869744037, 0.429493169259816, 0.6220310272663637]
    p4 = prior
    exp = Experiment("PAS", prior, p1, p2, p3, p4)
    if dataset == 2019:
        if prior == 7:
            exp.run("../runtime_dataset/caida_2019/00_7.txt")
        elif prior == 3:
            exp.run("../runtime_dataset/caida_2019/00_3.txt")
    elif dataset == 2016:
        if prior == 7:
            exp.run("../runtime_dataset/caida_2016/00_7.txt")
        elif prior == 3:
            exp.run("../runtime_dataset/caida_2016/00_3.txt")
    exp.draw("pas", dataset, highs, lows)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='estimation accuracy')
    parser.add_argument('--method', type = str, required = True, help = 'Algorithm name: nds, vhll, pas')
    parser.add_argument("--dataset", type = int, required = True, help = "2016 or 2019")
    parser.add_argument("--prior_num", type = int, required = True, help = "The number of maximal priority")
    parser.add_argument("--high_prior", type = int, nargs = "+", required = True, help = "The high-priority flows")
    parser.add_argument("--low_prior", type = int, nargs = "+", required = True, help = "The low-priortity flows")
    parser.add_argument("--p", type = float, required = False, help = "The sampling rate of nds")
    parser.add_argument("--mem_kb", type = float, required = False, help = "The on-chip memory (KB)")
    parser.add_argument("--v", type = int, required = False, help = "The number of registers in each virtual hll or rSkt")
    parser.add_argument("--pre", type = float, nargs='+', required = False, help = "The pre-sampling rate for the elements in different flow sets")
    parser.add_argument("--post", type = float, nargs='+', required = False, help = "The post-sampling rate for the elements in different flow sets")
    args = parser.parse_args()
    if args.method == "nds":
        nds_demo(args.p, args.mem_kb, args.prior_num, args.dataset, args.high_prior, args.low_prior)
    elif args.method == "vhll":
        vhll_demo(args.mem_kb, args.v, args.prior_num, args.dataset, args.high_prior, args.low_prior)
    elif args.method == "pas":
        pas_demo(args.mem_kb, args.prior_num, args.pre, args.post, args.dataset, args.high_prior, args.low_prior)
    elif args.method.lower() == "rskt":
        #mem_, prior, v, dataset, highs, lows
        rskt_demo(args.mem_kb, args.prior_num, args.v, args.dataset, args.high_prior, args.low_prior)