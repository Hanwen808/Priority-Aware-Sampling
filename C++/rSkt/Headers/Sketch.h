#ifndef PAS_SKETCH_H
#define PAS_SKETCH_H
#include <stdint.h>

class Sketch {
public:
    virtual void update(uint32_t, uint32_t, uint32_t) = 0;
    virtual int estimate(uint32_t, int ) = 0;
};
#endif //PAS_SKETCH_H
