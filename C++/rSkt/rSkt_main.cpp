#include <vector>
#include <fstream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <time.h>
#include <iostream>
#include <unordered_set>
#include <unordered_map>
#include "Headers/rSkt.h"

using namespace std;

uint32_t convertIPv4ToUint32(char* ipAddress) {
    uint32_t result = 0;
    int octet = 0;
    char ipCopy[KEY_LEN];
    strncpy(ipCopy, ipAddress, sizeof(ipCopy) - 1);
    ipCopy[sizeof(ipCopy) - 1] = '\0';
    char* token = strtok(ipCopy, ".");
    while (token != nullptr) {
        octet = std::stoi(token);
        result = (result << 8) + octet;
        token = std::strtok(nullptr, ".");
    }
    return result;
}

// Updating rSkt and testing the processing throughput.
// for each row in dataset, the type of row is priority : <src, dst>
void processPackets(Sketch* skt, vector<pair<uint32_t, pair<uint32_t, uint32_t>>>& dataset) {
    clock_t start = clock(); // The start time of processing packet stream
    for (int i = 0; i < dataset.size(); i++) {
        skt->update(dataset[i].second.first, dataset[i].second.second, dataset[i].first);
    }
    clock_t current = clock(); // The end time of processing packet stream
    cout << dataset.size() << " lines: have used " << ((double)current - start) / CLOCKS_PER_SEC << " seconds" << endl;
    double throughput = (dataset.size() / 1000000.0) / (((double)current - start) / CLOCKS_PER_SEC);
    cout << "Update throughput: " << throughput << "Mpps" << endl;
    start = clock();
    for (int i = 0; i < dataset.size(); i++)
        skt->estimate(dataset[i].second.first, dataset[i].first);
    current = clock();
    cout << dataset.size() << " lines: have used " << ((double)current - start) / CLOCKS_PER_SEC << " seconds" << endl;
    throughput = (dataset.size() / 1000000.0) / (((double)current - start) / CLOCKS_PER_SEC);
    cout << "Query throughput: " << throughput << "Mpps" << endl;
}

/*
 *  Function: Generate the dataset and real flow spreads dict.
 *  dataDir: the directory of dataset.
 *  numOfMinutes: the measurement periods.
 *  dataset: records triple (source, destination, priority)
 * */
void getDataSet(string dataDir, unsigned int numOfMinutes, vector<pair<uint32_t, pair<uint32_t, uint32_t>>>& dataset,
                unordered_map<uint32_t, unordered_map<uint32_t , unordered_set<uint32_t>>>& realFlowInfo)
{
    char dataFileName[20]; // The filename of dataset
    uint32_t flowId;          // flow key
    uint32_t eleId;           // element key 1
    uint32_t prior;        // element key 2
    string line, source, destination, priority;
    clock_t start = clock();
    for (unsigned int i = 0; i < numOfMinutes; i++) {
        sprintf(dataFileName, "%02d.txt ", i);
        string oneDataFilePath = dataDir + "/00_3.txt"; // Organize a complete filename.
        cout << oneDataFilePath << endl;
        fstream fin(oneDataFilePath);
        while (fin.is_open() && fin.peek() != EOF) {
            getline(fin, line); // each line of dataset is consist of three fields: source address, destination address and destination port
            stringstream ss(line.c_str());
            // Build a flow element
            ss >> source >> destination >> priority;
            flowId = convertIPv4ToUint32((char*) source.c_str());
            eleId = convertIPv4ToUint32((char*) destination.c_str());
            prior = std::stoi(priority.c_str());
            dataset.push_back(make_pair(prior, make_pair(flowId, eleId)));
            realFlowInfo[prior][flowId].insert(eleId);
            if (dataset.size() % 5000000 == 0) {
                clock_t current = clock();
                cout << "have added " << dataset.size() << " packets, have used " << ((double)current - start) / CLOCKS_PER_SEC << " seconds." << endl;
            }
        }
        if (!fin.is_open()) {
            cout << "dataset file " << oneDataFilePath << "closed unexpectedlly"<<endl;
            exit(-1);
        }else
            fin.close();
    }
    clock_t current = clock();
    cout << "have added " << dataset.size() << " packets, have used " << ((double)current - start) / CLOCKS_PER_SEC << " seconds" << endl;
    // count the totol number of flows and distinct elements
    // three different type spread tasks
    for (auto iter = realFlowInfo.begin(); iter != realFlowInfo.end(); iter ++) {
        unsigned int totalSpread = 0;
        for (auto iter1 = iter->second.begin(); iter1 != iter->second.end(); iter1 ++) {
            totalSpread += iter1->second.size();
        }
        std::cout << "The total spread of " << iter->first << "-th class flows is " << totalSpread << ".\n";
    }
}

void saveResults(string outputFilePath, Sketch* skt, unordered_map<uint32_t, unordered_map<uint32_t , unordered_set<uint32_t >>>& realFlowInfo) {
    ofstream fout;
    unordered_map<uint32_t, unordered_map<uint32_t, double>> totalAreMap;
    unordered_map<uint32_t, unordered_map<uint32_t, uint32_t>> totalCountMap;
    unordered_map<uint32_t, double> allAreMap;
    unordered_map<uint32_t, uint32_t> allCountMap;
    for (auto iter = realFlowInfo.begin(); iter != realFlowInfo.end(); iter ++) {
        unordered_map<uint32_t, double> areMap;
        unordered_map<uint32_t, uint32_t> countMap;
        string outputfilename = outputFilePath + "_" + std::to_string(iter->first) + ".txt";
        fout.open(outputfilename, ios::out);
        for (auto iter1 = realFlowInfo[iter->first].begin(); iter1 != realFlowInfo[iter->first].end(); iter1 ++) {
            uint32_t realspread = (iter1->second).size();
            uint32_t estimatedspread = skt->estimate(iter1->first, iter->first);
            fout << realspread << " " << estimatedspread << "\n";
            uint32_t index =  floor(log10(1.0 * realspread));
            allAreMap[iter->first] += (1.0 * abs(1.0 * realspread - estimatedspread)) / (1.0 * realspread);
            allCountMap[iter->first] += 1;
            areMap[index] += (1.0 * abs(1.0 * realspread - estimatedspread)) / (1.0 * realspread);
            countMap[index] += 1;
        }
        fout.close();
        totalAreMap[iter->first] = areMap;
        totalCountMap[iter->first] = countMap;
    }
    for (auto iter = allAreMap.begin(); iter != allAreMap.end(); iter ++) {
        allAreMap[iter->first] = iter->second / (1.0 * allCountMap[iter->first]);
    }
    for (auto iter = totalAreMap.begin(); iter != totalAreMap.end(); iter ++) {
        string outputfilename = outputFilePath + "_" + std::to_string(iter->first) + "_range.txt";
        fout.open(outputfilename, ios::out);
        for (auto iter1 = iter->second.begin(); iter1 != iter->second.end(); iter1 ++) {
            fout << "[" << "10^" << iter1->first << ", 10^" << iter1->first + 1 << "):" << 1.0 * iter1->second / (1.0 * totalCountMap[iter->first][iter1->first]) << "\n";
        }
        fout << "Total are is " << allAreMap[iter->first] << ".\n";
        fout.close();
    }
}

int main(int argc, char** argv) {
    //prepare the dataset
    string outputFilePath = "../records/spreads_";
    cout << "prepare the dataset" << endl;
    string dataDir = R"(../data/2019)";
    unsigned int numOfMinutes = 1;
    vector<pair<uint32_t, pair<uint32_t , uint32_t>>> dataset;
    unordered_map<uint32_t, unordered_map<uint32_t , unordered_set<uint32_t >>> realFlowInfo;
    getDataSet(dataDir, numOfMinutes, dataset, realFlowInfo);
    cout << endl;
    uint32_t v, total_memory_kb;
    for (int i = 1; i < argc; i ++) {
        if(strcmp(argv[i], "-total_mem") == 0) {
           string str_temp = string(argv[i + 1]);
           outputFilePath += string(argv[i + 1]) + "_";
           total_memory_kb = strtoul(str_temp.c_str(), NULL, 10); 
        } else if (strcmp(argv[i], "-v") == 0) {
           string str_temp = string(argv[i + 1]);
           outputFilePath += string(argv[i + 1]) + "_";
           v = strtoul(str_temp.c_str(), NULL, 10);
        }
    }
    unsigned int unitNum = (total_memory_kb * 1024 * 8) / (5 * v);
    cout << "Total memory is " << total_memory_kb << "KB" << endl;
    rSkt* skt = new rSkt(unitNum, v);
    cout << endl;
    cout << "Start processing..." << endl;
    processPackets(skt, dataset);
    //save the result in files
    cout << endl;
    cout << "save the result in spreads.txt ..." << endl;
    
    saveResults(outputFilePath, skt, realFlowInfo);
    return 0;
}