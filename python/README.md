# C++ Codes for PipeFilter and Baselines

## Platform
On the CPU platform, the codes of priority-aware sampling and the baselines are compiled using g++ version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1) and run on a server equipped with two Intel(R) Xeon(R) Gold 6258R 2.70GHz CPUs and 754GB RAM.

## Descriptions
We evaluate the performance of our proposal and compared it with state-of-the-art algorithms. The compiling command is as follows.

```shell
python ../main.py --method pas --dataset 2019 --prior_num 7 --p $4 --mem_kb $5
./scripts 
```
