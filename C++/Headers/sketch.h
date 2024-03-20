//
// Created by lenovo on 2024/1/27.
//

#ifndef PAS_SKETCH_H
#define PAS_SKETCH_H
#include <iostream>
#include <cstring>
#define MAX_PRIORITY 3
#define KEY_LEN 16
class Sketch{
public:
// src, dst, priority
virtual void update(char *, char *, uint32_t) = 0;
// src
virtual uint32_t estimate(char *) = 0;
};

#endif //PAS_SKETCH_H
