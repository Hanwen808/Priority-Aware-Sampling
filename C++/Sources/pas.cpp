#include "../Headers/pas.h"

PAS::PAS(uint32_t m, float * parray, float pre) {
    this->m = m; // m is the length of R
    this->sample_seed = 91234;
    this->hash_seed = 35512;
    this->pre_sample_seed = 77123;
    this->pre = pre;
    this->R = allocregarray(m);
    for (int i = 0; i < MAX_PRIORITY; ++i) {
        this->V[i] = parray[i];
        this->P[i] = parray[i];
        this->C[i] = 0;
    }
    fillzero(R, m << 1);
}

PAS::~PAS() {
    delete R;
}

void PAS::update(char * src, char * dst, uint32_t priority) {
    uint32_t hashVal, hashIndex, regVal, sumVal = 0;
    char XOR[KEY_LEN];
    for (int i = 0; i < KEY_LEN; ++i)
        XOR[i] = src[i] ^ dst[i];
    MurmurHash3_x86_32(XOR, KEY_LEN, this->pre_sample_seed, &hashVal);
    hashIndex = hashVal % 0xffffffff;
    if (hashIndex > this->pre * 0xffffffff)
        return;
    //MurmurHash3_x86_32(XOR, KEY_LEN, this->hash_seed, &hashVal);
    hashIndex = hashVal % m;
    regVal = getreg(hashIndex, R);
    if (regVal < priority) {
        if (regVal != 0)
            C[regVal - 1] -= 1;
        cleanreg(hashIndex, R);
        setreg(hashIndex, priority, R);
        C[priority - 1] += 1;
        MurmurHash3_x86_32(XOR, KEY_LEN, this->sample_seed, &hashVal);
        hashIndex = hashVal % 0xffffffff;
        if (hashIndex <= this->P[priority - 1] * 0xffffffff) {
            //T[priority][src] += 1;
        }
        for (int j = priority - 1; j < MAX_PRIORITY; ++j)
            sumVal += C[j];
        this->P[priority - 1] = (m * V[priority - 1]) / (pre * (m - sumVal));
        sumVal = 0;
    }
}

uint32_t PAS::estimate(char * src) {
    for (int i = 1; i < MAX_PRIORITY + 1; ++i) {
        if (T[i].find(src) != T[i].end())
            return T[i][src] / V[i - 1];
    }
    return 0;
}
