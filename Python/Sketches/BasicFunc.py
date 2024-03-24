# -*- coding:utf-8 -*-

import sys
import mmh3
import random
import socket
import struct
import math
import numpy as np


def gen_rand_seed():
    return random.randint(0, 2**32)


def gen_hash(key, seed=None):
    if seed is None:
        seed = gen_rand_seed()
    hash_value = mmh3.hash(str(key), seed, False) % (2**32)
    return hash_value


def is_valid_ipv4_address(ip_addr):
    try:
        socket.inet_pton(socket.AF_INET, ip_addr)
    except AttributeError:
        try:
            socket.inet_aton(ip_addr)
        except socket.error:
            return False
        return ip_addr.count('.') == 3
    except socket.error:
        return False
    return True


def ip_addr_to_int(ip_addr):
    return struct.unpack("!I", socket.inet_aton(ip_addr))[0]


def int_to_ip_addr(int_value):
    return socket.inet_ntoa(struct.pack("!I", int_value))


def NDS_bitmap_size_cal(num_distinct_elements, threshold_sacrifice=128):

    return - num_distinct_elements / math.log(1 - (sys.float_info.epsilon) ** (1 / threshold_sacrifice))


def filter_bucket_num_cal(num_hash_func, shift_value, single_bucket_size, threshold_sacrifice):
    # theta = - math.log(1 - (sys.float_info.epsilon) ** (1 / threshold_sacrifice))

    num_flows_in_spread = [1289031, 294855, 72771, 19894, 7229, 2020, 546, 249, 156, 24, 16]
    # distinct_elements_of_filtered_flows =


    num_unfiltered_flows = 0
    for index in range(shift_value+single_bucket_size, len(num_flows_in_spread)):
        num_unfiltered_flows += num_flows_in_spread[index]

    # available_size = round(NDS_bitmap_size_cal(distinct_elements_of_filtered_flows, threshold_sacrifice=128)) + 1
    #
    # up = distinct_elements_of_filtered_flows * (num_unfiltered_flows ** num_hash_func) * \
    #      (num_hash_func ** (num_hash_func + 1)) * (1 + theta * (num_hash_func + 1) * 200)
    # down = theta * single_bucket_size
    # m1 = (up / down) ** (1 / (num_hash_func + 1))

    # m2 = round(available_size / single_bucket_size)
    m2 = num_unfiltered_flows * num_hash_func / ((0.1 ** 10) ** (1 / num_hash_func))

    return m2


def actual_relative_error(true_spread, estimated_spread, threshold=1):

    ARE_all = []
    ARE_1_100 = []
    ARE_101_500 = []
    ARE_501_1000 = []
    ARE_1001_10000 = []
    ARE_10001_ = []

    for index in range(len(true_spread)):
        single_are = float(abs(true_spread[index] - estimated_spread[index])) / float(true_spread[index])
        if true_spread[index] >= threshold:
            ARE_all.append(single_are)

        judge_range_val = true_spread[index]
        if judge_range_val < 100:
            ARE_1_100.append(single_are)
        elif judge_range_val < 500:
            ARE_101_500.append(single_are)
        elif judge_range_val < 1000:
            ARE_501_1000.append(single_are)
        elif judge_range_val < 10000:
            ARE_1001_10000.append(single_are)
        else:
            ARE_10001_.append(single_are)

    if len(ARE_1_100) == 0 :
        ARE_1_100.append(0)

    if len(ARE_101_500) == 0:
        ARE_101_500.append(0)

    return [np.average(ARE_all), [np.average(ARE_1_100), np.average(ARE_101_500),
                                  np.average(ARE_501_1000), np.average(ARE_1001_10000), np.average(ARE_10001_)], [np.size(ARE_1_100), np.size(ARE_101_500),
                                  np.size(ARE_501_1000), np.size(ARE_1001_10000), np.size(ARE_10001_)]]


class SpreadCollection:

    def __init__(self):
        self.collector = {}

    def packet_processing(self, flow_id, element_id):
        if flow_id not in self.collector:
            self.collector[flow_id] = set()

        if element_id not in self.collector[flow_id]:
            self.collector[flow_id].add(element_id)

    def get_spread(self):
        spread = {}
        for key in self.collector.keys():
            spread[key] = len(self.collector[key])

        return spread


if __name__ == '__main__':
    # print(int_to_ip_addr(0xc0a80164))  # 192.168.1.100
    # print(ip_addr_to_int('10.0.0.1'))  # 167772161
    #
    # print(is_valid_ipv4_address('277.0.0.1'))
    # print(is_valid_ipv4_address('122.0.0.1:a'))
    # print(is_valid_ipv4_address('0.255.255.255'))

    a = None
    print(a is not None)
