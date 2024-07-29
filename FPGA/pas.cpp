#include "./murmurhash.h"
#include "./register.h"
#define M 204800
#define MAX_PRIORITY 3
unsigned char R[M] = {0};
const double Pre[MAX_PRIORITY] = {0.6754015968235019, 0.6973980378869656, 0.6594262862515415};
const double V[MAX_PRIORITY] = {0.04978706836786395, 0.1353352832366127, 0.36787944117144233};
                      
void update(uint32_t key_i, uint32_t ele_i, uint32_t priority_i, uint32_t* key_o, uint32_t* ele_o, uint32_t* priority_o, uint32_t* C, double* post) {
    uint32_t hashVal, hashIndex, regVal, XOR, sumVal = 0;
    XOR = key_i ^ ele_i;
    MurmurHash3_x86_32(&XOR, 0, &hashVal);
    hashIndex = hashVal % 0xffffffff;
    if (hashIndex > Pre[priority_i - 1] * 0xffffffff)
        return;
    hashIndex = hashVal % M;
    regVal = getreg(hashIndex, R);
    if (regVal < priority_i) {
        if (regVal != 0)
            C[regVal - 1] -= 1;
        cleanreg(hashIndex, R);
        setreg(hashIndex, priority_i, R);
        C[priority_i - 1] += 1;
        if (hashIndex <= post[priority_i - 1] * M) {
            *key_o = key_i;
            *ele_o = ele_i;
            *priority_o = priority_i;
        }
        for (int j = priority_i - 1; j < MAX_PRIORITY; ++j) {
            sumVal += C[j];
        }
        post[priority_i - 1] = (M * V[priority_i - 1]) / (Pre[priority_i - 1] * (M - sumVal));
    }
}
