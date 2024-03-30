#ifndef PAS_NDS_H
#define PAS_NDS_H
#include "bitmap.h"
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

class NDS: virtual public Sketch{
private:
    uint32_t hash_seed, sample_seed;
    float p, p1;
    std::uint32_t m, c;
    bitmap B;
    std::unordered_map<uint32_t , std::unordered_map<char*, uint32_t, HashFunc, Cmp>> T;
public:
    NDS(uint32_t, float);
    ~NDS();
    void update(char *, char *, uint32_t);
    uint32_t estimate(char *);
};

#endif //PAS_NDS_H
