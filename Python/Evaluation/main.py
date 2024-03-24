from Sketches.NDS import *
from Sketches.PAS import *
from Sketches.vHLL import *

class Experiment:
    '''
      name: algorithm's name
    '''
    def __init__(self, name, *args):
        self.sketch = None
        self.real_dict = None
        self.pred_dict = None
        self.flow_count = 0
        self.flow_count_dict = {}
        self.are_dict = defaultdict(int)
        self.are = 0
        self.fine_are_dict = {}
        self.fine_flow_count = {}
        self.class_flow_count = {}
        self.class_are_dict = {}
        if name == "NDS":
            if len(args) != 2:
                print("Sorry, NDS requires two parameters to be passed in, prob and m")
                exit()
            self.sketch = NDS(args[0], args[1])
        elif name == "vHLL" or name == "VHLL":
            if len(args) != 2:
                print("Sorry, vHLL requires two parameters to be passed in, physical register number "
                      "and virtual register number")
                exit()
            self.sketch = vhll(args[0], args[1])
        elif name == "PAS":
            if len(args) != 4:
                print("Sorry, PAS requires four parameters to be passed in, the number of filter units "
                      ", pre-sampling rates, post-sampling rates and maximum priority")
                exit()
            self.sketch = PAS(args[0], args[1], args[2], args[3])
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

    def draw(self):
        x = np.arange(math.log10(mea_T) if mea_T != 0 else 0, 6, 1)
        for i in range(1, max_priority + 1):
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
                else:
                    self.class_are_dict['low'] += temp_are
                    self.class_flow_count['low'] += 1
                x_log.append(self.real_dict[i][key])
                y_log.append(self.pred_dict[i][key])
            x_log = np.log10(x_log)
            y_log = np.log10(y_log)
            plt.plot(x_log, y_log, '*', color = color_lst[i - 1], label = str(i) + "-priority flow")
        for i in range(1, max_priority + 1):
            self.are_dict[i] = self.are_dict[i] / self.flow_count_dict[i] if self.flow_count_dict[i] != 0 else None
            for j in range(8):
                self.fine_are_dict[i][j] = self.fine_are_dict[i][j] / self.fine_flow_count[i][j] if self.fine_flow_count[i][j] != 0 else None
        self.class_are_dict['high'] = self.class_are_dict['high'] / self.class_flow_count['high'] if self.class_flow_count['high'] != 0 else None
        self.class_are_dict['low'] = self.class_are_dict['low'] / self.class_flow_count['low'] if self.class_flow_count['low'] != 0 else None
        plt.plot(x, x)
        plt.legend()
        plt.xlabel("Real spreads")
        plt.ylabel("Estimated spreads")
        plt.tight_layout()
        plt.show()
        print("Show the are in different priority flow sets.")
        #print(self.are_dict)
        for i in range(1, max_priority + 1):
            print("  The are of {}-priority flows is {}.".format(i, self.are_dict[i]))
            for j in range(8):
                if self.fine_are_dict[i][j] == None:
                    continue
                print("    The are of [{},{}) is {}.".format(10 ** j, 10 ** (j + 1), self.fine_are_dict[i][j]))
        print("Show the are in high/low priority flow sets.")
        print("  The are of high-priority flows is {}.".format(self.class_are_dict['high']))
        print("  The are of low-priority flows is {}.".format(self.class_are_dict['low']))
        print("Total ARE is {}.".format(self.are / self.flow_count))

def nds_demo():
    exp = Experiment("NDS", 0.1, 100 * 1024 * 8)
    exp.run("../data/caida_2019/00_7.txt")
    exp.draw()

def vhll_demo():
    p1 = int(50 * 2 ** 13 / 5)
    p2 = 16
    exp = Experiment("vHLL", p1, p2)
    exp.run("../data/caida_2019/00_7.txt")
    exp.draw()

def pas_demo():
    p1 = 200 * 1024 * 8 // 3
    p2 = [1, 1, 1, 1, 1, 1, 1]
    p3 = [0.039870228769679786, 0.05425990763315014, 0.08353920308331102, 0.12519484958411123, 0.22027212869744037, 0.429493169259816, 0.6220310272663637]
    p4 = 7
    exp = Experiment("PAS", p1, p2, p3, p4)
    exp.run("../data/caida_2019/00_7.txt")
    exp.draw()

if __name__ == '__main__':
    vhll_demo()