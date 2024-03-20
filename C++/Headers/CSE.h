//
// Created by lenovo on 2024/1/31.
//

#ifndef PAS_CSE_H
#define PAS_CSE_H
#include "sketch.h"
#include "bitmap.h"
#include "MurmurHash3.h"

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

class CSE: public Sketch {
private:
    bitmap B;
    int n, s, K;
    uint32_t * hashSeeds;
    double vn = 0;
public:
    CSE(int, int);
    ~CSE();
    void update(char *, char *, uint32_t) override;
    uint32_t estimate(char *) override;
    void setVn();
};
#endif //PAS_CSE_H
