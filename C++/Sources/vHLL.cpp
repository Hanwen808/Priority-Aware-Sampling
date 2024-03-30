#include "../Headers/vHLL.h"

void VHLL::update(char * src, char * dst, uint32_t priority) {
    flows.insert(src);
    uint32_t hashIndex, hashValue, P, Q, leftmost = 0;
    MurmurHash3_x86_32(dst, KEY_LEN, this->hashSeed, &hashValue);
    P = hashValue >> (sizeof(uint32_t) * 8 - numLeadingBits);
    Q = hashValue - (P << (sizeof(uint32_t) * 8 - numLeadingBits));
    while (Q) {
        leftmost ++;
        Q = Q >> 1;
    }
    leftmost = sizeof(uint32_t) * 8 - numLeadingBits - leftmost + 1;
    MurmurHash3_x86_32(src, KEY_LEN, this->hashSeeds[P], &hashValue);
    hashIndex = hashValue % m;
    R[hashIndex] = std::max(R[hashIndex], leftmost);
}

void VHLL::updateParams() {
    double zero_ratio = 0;
    double sum_register_arr = 0;
    for(int i = 0; i < m; i++) {
        sum_register_arr += pow(2.0, -double(R[i]));
        if(R[i] == 0)    zero_ratio += 1;
    }
    zero_ratio = zero_ratio / m;
    double temp_cardi_all_flow = (0.7213 / (1 + (1.079 / m))) * pow(double(m), 2) / sum_register_arr;

    if(temp_cardi_all_flow <= 2.5 * m) {
        if(zero_ratio != 0) {
            cardi_all_flow = - double(m) * log(zero_ratio);
        }
    }
    else if(temp_cardi_all_flow > pow(2.0, 32) / 30) {
        cardi_all_flow = - pow(2.0, 32) * log(1 - temp_cardi_all_flow / pow(2.0, 32));
    }
    else if(temp_cardi_all_flow < pow(2.0, 32) / 30) {
        cardi_all_flow = temp_cardi_all_flow;
    }
}

uint32_t VHLL::estimate(char * src) {
    uint32_t hashIndex, hashValue;
    if(flows.count(src) != 0) {
        double zero_ratio_v_reg = 0;
        double sum_v_reg = 0;
        for(int i = 0; i < s; i++) {
            MurmurHash3_x86_32(src, KEY_LEN, hashSeeds[i], &hashValue);
            hashIndex = hashValue % m;
            sum_v_reg += pow(2.0, -double(R[hashIndex]));
            if(R[hashIndex] == 0)    zero_ratio_v_reg += 1;
        }
        zero_ratio_v_reg = zero_ratio_v_reg / s;
        double flow_cardi = alpha * pow(s, 2) / sum_v_reg;

        if(flow_cardi <= 2.5 * s) {
            if(zero_ratio_v_reg != 0) {
                flow_cardi = - log(zero_ratio_v_reg) * s - cardi_all_flow * s / m;
            }
            else {
                flow_cardi = flow_cardi - cardi_all_flow * s / m;
            }
        }
        else if(flow_cardi > pow(2.0, 32) / 30) {
            flow_cardi = - pow(2.0, 32) * log(1 - flow_cardi / pow(2.0, 32)) - cardi_all_flow * s / m;
        }
        else if(flow_cardi < pow(2.0, 32) / 30) {
            flow_cardi = flow_cardi - cardi_all_flow * s / m;
        }

        return flow_cardi;
    }
    else {
        return 0;
    }
}
