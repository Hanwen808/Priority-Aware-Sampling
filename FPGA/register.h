//
// Created by Hanwen on 2024/1/27.
//

#ifndef PAS_REGISTER_H
#define PAS_REGISTER_H
typedef unsigned char* registerArray;
// each register consists of 2 bts
#define getreg(n,reg) (((reg[(n)>>2])&(0xC0>>(((n)&0x03)<<1)))>>((~((n)&0x03)&0x03)<<1))
#define cleanreg(n,reg) {reg[(n)>>2]&=(~(0xC0>>(((n)&0x03)<<1)));}
#define setreg(n,x,reg) {reg[(n)>>2]|=(x<<((0x03&(~((n)&0x03)))<<1));}
#define regarraysize(n) (((int)(n<<1)+7)>>3)
#define allocregarray(n) (unsigned char*)malloc(regarraysize(n))
#define fillzero(reg,n) {int internali;for(internali=(((int)(n)-1)>>3);internali>=0;internali--){reg[internali]=0x00;}}

#endif //PAS_REGISTER_H
