//
// Created by lenovo on 2024/1/28.
//

#ifndef PAS_REGARRAY_H
#define PAS_REGARRAY_H

class RegArray{
private:
    int n, w, m; // the length of register array and register
    unsigned char* R;
public:
    RegArray(int, int);
    ~RegArray();
    void setreg(int, int);
    int getreg(int);
};

#endif //PAS_REGARRAY_H
