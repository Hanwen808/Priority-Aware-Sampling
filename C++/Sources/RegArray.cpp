//
// Created by lenovo on 2024/1/28.
//
#include <cstdlib>
#include "../Headers/RegArray.h"

RegArray::RegArray(int n, int w) {
    this->n = n;
    this->w = w;
    this->m = 8 / w;
    this->R = (unsigned char*) malloc(((n * w) + 7) >> 3);
}

RegArray::~RegArray() {
    delete R;
}

int RegArray::getreg(int i) {
    int bytesIndex = (i * w) / 8;
    int offset = (i * w) % 8;
    // span two bytes?
    bool span = offset >= 8 - w;
    if (!span)
        return (R[bytesIndex] & (0xF8 >> offset)) >> (8 - (offset + w));
    else {
        int t = 0xF8 >> offset;
        if (t & 0x08) {
            return ((R[bytesIndex] & (0xF8 >> offset)) << 1) + ((R[bytesIndex + 1] & 0x80) >> 7);
        } else if (t & 0x04) {
            return ((R[bytesIndex] & (0xF8 >> offset)) << 2) + ((R[bytesIndex + 1] & 0xC0) >> 6);
        } else if (t & 0x02) {
            return ((R[bytesIndex] & (0xF8 >> offset)) << 3) + ((R[bytesIndex + 1] & 0xE0) >> 5);
        } else {
            return ((R[bytesIndex] & (0xF8 >> offset)) << 4) + ((R[bytesIndex + 1] & 0xF0) >> 4);
        }
    }
}

void RegArray::setreg(int i, int x) {

}