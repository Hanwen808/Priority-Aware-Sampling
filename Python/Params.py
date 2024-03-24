'''
  This file contains the configuration parameters of sketches during measurement.
'''
import mmh3
import numpy as np
import pandas as pd
import math
from collections import defaultdict
import matplotlib.pyplot as plt
from tqdm import tqdm

max_priority = 7
mea_T = 0
color_table = ['red', 'green', 'blue', 'c', 'pink', 'purple', 'orange', 'crimson', 'skyblue', 'chocolate', 'violet', 'navy']
color_lst = [color_table[i] for i in range(max_priority)]
high_prior_flows = set([6,7])
low_prior_flows = set([1,2,3,4,5])