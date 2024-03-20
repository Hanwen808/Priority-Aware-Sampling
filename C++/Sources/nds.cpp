//
// Created by lenovo on 2024/1/27.
//
#include "../Headers/nds.h"

using namespace std;
NDS::NDS(uint32_t m, float p) {
    this->m = m;
    this->c = 0;
    this->p = p;
    this->p1 = p;
    this->hash_seed = 54133;
    this->sample_seed = 71241;
    this->B = allocbitmap(m);
}

NDS::~NDS() {
    free(this->B);
}

void NDS::update(char * src, char * dst, uint32_t priority) {
    uint32_t hashVal, hashIndex;
    char XOR[KEY_LEN];
    for (int i = 0; i < KEY_LEN; ++i)
        XOR[i] = src[i] ^ dst[i];
    MurmurHash3_x86_32(XOR, KEY_LEN, this->hash_seed, &hashVal);
    hashIndex = hashVal % this->m;
    if (getbit(hashIndex, B) == 0) {
        c += 1;
        setbit(hashIndex, B);
    } else {
        return;
    }
    MurmurHash3_x86_32(XOR, KEY_LEN, this->sample_seed, &hashVal);
    hashIndex = hashVal % 0xffffffff;
    if (hashIndex <= this->p1 * 0xffffffff) {
        //this->T[priority][src] += 1;
    }
    this->p1 = (m * p) / (m - c);
}

uint32_t NDS::estimate(char * src) {
    for (int i = 1; i < MAX_PRIORITY + 1; ++i) {
        if (T[i].find(src) != T[i].end())
            return T[i][src] / p;
    }
    return 0;
}