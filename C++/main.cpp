#include <vector>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <unordered_set>
#include <time.h>
//#include "Headers/nds.h"
//#include "Headers/pas.h"
//#include "Headers/CSE.h"
#include "Headers/vHLL.h"
using namespace std;
// Updating sketch and testing the processing throughput.
void processPackets(Sketch* sketch, vector<pair<pair<char*, char*>, uint32_t>>& dataset) {
    clock_t start = clock(); // The start time of processing packet stream
    for (int i = 0; i < dataset.size(); i++)
        sketch->update(dataset[i].first.first, dataset[i].first.second, dataset[i].second);
    clock_t current = clock(); // The end time of processing packet stream
    cout << dataset.size() << " lines: have used " << ((double)current - start) / CLOCKS_PER_SEC << " seconds" << endl;
    double throughput = (dataset.size() / 1000000.0) / (((double)current - start) / CLOCKS_PER_SEC);
    cout << "throughput: " << throughput << "Mpps" << endl;
}

/*
 *  Function: Generate the dataset and real flow spreads dict.
 *  dataDir: the directory of dataset.
 *  numOfMinutes: the measurement periods.
 *  dataset: records triple (source, destination, port)
 * */
void getDataSet(string dataDir, unsigned int numOfMinutes, vector<pair<pair<char*, char*>, uint32_t>>& dataset,
                unordered_map<uint32_t, unordered_map<char*, unordered_set<char*, HashFunc, Cmp>, HashFunc, Cmp>>& realFlowInfo) {
    char dataFileName[20]; // The filename of dataset
    char* src;            // flow label
    char* dst;            // element label
    uint32_t priority;       // priority
    string line, source, destination, prioritys;
    clock_t start = clock();
    for (unsigned int i = 0; i < numOfMinutes; i++) {
        sprintf(dataFileName, "%02d.txt ", i);
        string oneDataFilePath = "../data/00_p4.txt";
        cout << oneDataFilePath << endl;
        fstream fin(oneDataFilePath);
        while (fin.is_open() && fin.peek() != EOF) {
            src = new char[KEY_LEN] {0};
            dst = new char[KEY_LEN] {0};
            getline(fin, line);
            stringstream ss(line.c_str());
            ss >> source >> destination >> prioritys;
            memcpy(src, source.c_str(), KEY_LEN);
            memcpy(dst, destination.c_str(), KEY_LEN);
            priority = atoi(prioritys.c_str());
            // building the dataset, real flow spreads dicts
            dataset.push_back(make_pair(make_pair(src, dst), priority));
            realFlowInfo[priority][src].insert(dst);
            if (dataset.size() % 5000000 == 0) {
                clock_t current = clock();
                cout << "have added " << dataset.size() << " packets, have used " << ((double)current - start) / CLOCKS_PER_SEC << " seconds." << endl;
            }
        }
        if (!fin.is_open()) {
            cout << "dataset file " << oneDataFilePath << " closed unexpectedlly"<<endl;
            exit(-1);
        } else {
            fin.close();
        }
    }
    clock_t current = clock();
    cout << "have added " << dataset.size() << " packets, have used " << ((double)current - start) / CLOCKS_PER_SEC << " seconds" << endl;
    // count the totol number of flows and distinct elements
    auto iter = realFlowInfo.begin();
    unsigned int totalSpread = 0;
    while (iter != realFlowInfo.end()) {
        totalSpread += (iter->second).size();
        iter++;
    }
    cout << "Per-source destination flow estimation:" << totalSpread << " distinct elements" << endl;
}

void saveResults(string outputFilePath, Sketch* sketch, unordered_map<uint32_t ,unordered_map<char*, unordered_set<char*, HashFunc, Cmp>, HashFunc, Cmp>>& realFlowInfo) {
    ofstream fout;
    vector<int> realSpreads, estimatedSpreads;
    for (int i = 1; i < MAX_PRIORITY + 1; ++i) {
        auto iter = realFlowInfo[i].begin();
        fout.open(outputFilePath + "_" + std::to_string(i) + ".txt", ios::out);
        while (fout.is_open() && iter != realFlowInfo[i].end()) {
            if (iter != realFlowInfo[i].begin())
                fout << endl;
            unsigned int realSpread = (iter->second).size();
            unsigned int estimatedSpread = sketch->estimate(iter->first);
            realSpreads.push_back(realSpread);
            estimatedSpreads.push_back(estimatedSpread);
            fout << realSpread << " " << estimatedSpread;
            iter++;
        }
        if (!fout.is_open())
            cout << outputFilePath << " closed unexpectedlly";
        else
            fout.close();
        sort(realSpreads.begin(), realSpreads.end(), greater<unsigned int>());
        cout << "";
        realSpreads.clear();
        estimatedSpreads.clear();
    }
}

int main() {
    //prepare the dataset
    cout << "prepare the dataset" << endl;
    string dataDir = R"(./data/)";
    unsigned int numOfMinutes = 1;
    vector<pair<pair<char*, char*>, uint32_t>> dataset;
    std::unordered_map<uint32_t ,std::unordered_map<char*, std::unordered_set<char*, HashFunc, Cmp>, HashFunc, Cmp>> realFlowInfo;
    getDataSet(dataDir, numOfMinutes, dataset, realFlowInfo);
    //prepare the sampling
    cout << endl;
    cout << "prepare the sampling" << endl;
    unsigned int bitsNum = 100 * 1024 * 8;
    cout << "Total space is " << 1.0 * bitsNum / 8 / 1024 << "KB" << endl;
    /*
    float parray[3] = {0.0825, 0.1235, 0.1744};
    unsigned int regNum = 100 * 1024 * 8 / 2;
    cout << "Total space is " << regNum * 2 / 8 / 1024 << "KB" << endl;
     Sketch* sketch = new PAS(regNum, parray, 0.3);
    */
    //Sketch* sketch = new NDS(bitsNum, 0.1);
    //CSE* sketch = new CSE(8000000, 1000);
    VHLL* sketch = new VHLL(bitsNum / 5, 32);
    cout << endl;
    cout << "start sampling" << endl;
    processPackets(sketch, dataset);
    //save the result in files
    //sketch->setVn();
    cout << endl;
    cout << "save the result in spreads.txt ..." << endl;
    string outputFilePath = "../records/spreads_vhll_";
    sketch->updateParams();
    saveResults(outputFilePath, sketch, realFlowInfo);
    cout << "Save processing finished." << endl;
    return 0;
}