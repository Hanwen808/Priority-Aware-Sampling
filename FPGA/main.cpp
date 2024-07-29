#include <stdio.h>
#include "../Source/pas.cpp"

int main() {
	uint32_t key_o = 0, ele_o = 0, priority_o = 0;
	uint32_t C[MAX_PRIORITY] = {0};
	double post[MAX_PRIORITY] = {0.04978706836786395, 0.1353352832366127, 0.36787944117144233};
	for (int key = 0; key < 10000; key++) {
		for (int ele = 0; ele < 10000; ele ++) {
			for (int prior = 1; prior <= 3; prior++) {
				update(key, ele, prior, &key_o, &ele_o, &priority_o, C, post);
			}
		}
	}
	return 0;
}
