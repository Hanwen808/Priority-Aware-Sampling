//
// Created by lenovo on 2024/1/31.
//

#ifndef PAS_TOOLS_H
#define PAS_TOOLS_H
#include <iostream>
#include <string>
#include <vector>
#include <sstream>

uint32_t ip_to_int(std::string ip_addr) {
    std::vector<std::string> segments;
    std::string temp;
    char split = '.';
    std::stringstream ss(ip_addr);
    while (getline(ss, temp, split))
        segments.push_back(temp);
    uint32_t segment1 = atoi(segments[0].c_str()) << 24;
    uint32_t segment2 = atoi(segments[1].c_str()) << 16;
    uint32_t segment3 = atoi(segments[2].c_str()) << 8;
    uint32_t segment4 = atoi(segments[3].c_str());
    uint32_t res = segment1 + segment2 + segment3 + segment4;
    return res;
}

#endif //PAS_TOOLS_H
