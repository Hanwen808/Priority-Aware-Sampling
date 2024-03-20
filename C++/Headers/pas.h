//
// Created by lenovo on 2024/1/27.
//

#ifndef PAS_PAS_H
#define PAS_PAS_H
#include "register.h"
#include "sketch.h"
#include "MurmurHash3.h"
#include <iostream>
#include <cstring>
#include <unordered_map>

struct Cmp {
    bool operator()(const char* a, const char* b) const {
        return strcmp(a, b) == 0;
    }
};

struct HashFunc {
    int operator()(const char* key) const {
        int hashValue = 0;
        MurmurHash3_x86_32(key, KEY_LEN, 54423, &hashValue);
        return hashValue;
    }
};

class PAS: public Sketch{
private:
    uint32_t m;
    registerArray R;
    uint32_t C[MAX_PRIORITY];
    float P[MAX_PRIORITY], V[MAX_PRIORITY];
    float pre;
    uint32_t hash_seed, sample_seed, pre_sample_seed;
    std::unordered_map<uint32_t, std::unordered_map<char*, uint32_t, HashFunc, Cmp>> T;
public:
    PAS(uint32_t, float*, float );
    ~PAS();
    void update(char *,char *, uint32_t);
    uint32_t estimate(char *);
};

#endif //PAS_PAS_H
