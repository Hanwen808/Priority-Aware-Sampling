#ifndef PAS_VHLL_H
#define PAS_VHLL_H
#include <iostream>
#include <set>
#include <cmath>
#include <unordered_map>
#include "MurmurHash3.h"
#include "sketch.h"

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

class VHLL: public Sketch {
private:
    uint32_t m, s, numLeadingBits;
    uint32_t * hashSeeds, hashSeed;
    uint32_t * R;
    double alpha, cardi_all_flow;
    std::set<char*, Cmp> flows;
public:
    VHLL(const uint32_t num_phy_register, const uint32_t num_virtual_register) {
        m = num_phy_register;
        s = num_virtual_register;

        srand(time(NULL));
        hashSeeds = new uint32_t[num_virtual_register];
        std::set<uint32_t> seed_set;
        while(seed_set.size() < num_virtual_register) {
            seed_set.insert(uint32_t(rand()));
        }
        std::set<uint32_t>::iterator itr = seed_set.begin();
        uint32_t index = 0;
        for(; itr != seed_set.end(); itr++) {
            hashSeeds[index] = *itr;
            index++;
        }
        numLeadingBits = floor(log10(double(num_virtual_register))/log10(2.0));
        hashSeed = uint32_t(rand());
        R = new uint32_t[num_phy_register];
        memset(R, 0, sizeof(uint32_t) * num_phy_register);
        cardi_all_flow = 0;
        if(num_virtual_register == 16)       alpha = 0.673;
        else if(num_virtual_register == 32)      alpha = 0.697;
        else if(num_virtual_register == 64)      alpha = 0.709;
        else    alpha = (0.7213 / (1 + (1.079 / num_virtual_register)));
    }

    ~VHLL() {
        delete [] hashSeeds;
        delete [] R;
    }

    void update(char *, char *, uint32_t) override;
    uint32_t estimate(char *) override;
    void updateParams();

};
#endif //PAS_VHLL_H
