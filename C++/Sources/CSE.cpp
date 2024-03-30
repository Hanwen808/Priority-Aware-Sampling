#include "../Headers/CSE.h"
#include <ctime>
#include "../Headers/MurmurHash3.h"
#include <cstdlib>
#include <cmath>

CSE::CSE(int n, int s) {
    srand(time(0));
    this->n = n;
    this->s = s;
    B = allocbitmap(this->n);
    //fillzero(B, n);
    hashSeeds = new uint32_t[this->s];
    for (int i = 0; i < this->s; i ++)
        hashSeeds[i] = (i * 100) + 100 * rand() / (RAND_MAX + 1);
    this->K = (this->s * 1000) + (int)  1000 * rand() / (RAND_MAX + 1);
}

CSE::~CSE() {
    delete B;
    delete hashSeeds;
}

void CSE::update(char * src, char * dst, uint32_t priority) {
    uint32_t hashValue, hashIndex;
    MurmurHash3_x86_32(dst, KEY_LEN, this->K, &hashValue);
    hashIndex = hashValue % s;
    MurmurHash3_x86_32(src, KEY_LEN, hashSeeds[hashIndex], &hashValue);
    hashIndex = hashValue % n;
    setbit(hashIndex, B);
}

void CSE::setVn() {
    for (int i = 0; i < n; ++i) {
        if (!getbit(i, B))
            vn ++;
    }
    vn = 1.0 * vn / n;
}

uint32_t CSE::estimate(char * src) {
    uint32_t estimatedSpread;
    double vs = 0.0;
    uint32_t hashValue, hashIndex;
    for (int i = 0; i < s; ++i) {
        MurmurHash3_x86_32(src, KEY_LEN, hashSeeds[i], &hashValue);
        hashIndex = hashValue % n;
        if (!getbit(hashIndex, B))
            vs += 1.0;
    }
    vs = vs / s;
    if (!vs)
        estimatedSpread = (uint32_t) round(s * log(1.0 * vn));
    else {
        //std::cout << log(1.0 * vn) << "---" << log(1.0 * vs) << std::endl;
        estimatedSpread = round(fmax(s * (log(1.0 * vn) - log(1.0 * vs)),1.0));
    }
    return estimatedSpread;
}
