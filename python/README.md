# C++ Codes for PipeFilter and Baselines

## Platform
On the CPU platform, the codes of priority-aware sampling and the baselines are compiled using g++ version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1) and run on a server equipped with two Intel(R) Xeon(R) Gold 6258R 2.70GHz CPUs and 754GB RAM.

## Descriptions
We evaluate the estimation performance of our proposal and compared it with state-of-the-art algorithms. The run command is as follows.

```shell
./scripts/exp_accuracy.sh
```

We can also evaluate the estimation accuracy for different algorithms with different memory configurations and other parameters. The run command is as follows.

```shell
python -W ignore ../main.py --method "nds" --dataset ${_dataset} --prior_num ${_prior} --p ${probs2016[$i]} --mem_kb ${mems[$i]} --high_prior ${H[0]} --low_prior ${L[0]} ${L[1]}
or
python -W ignore ../main.py --method "nds" --dataset ${_dataset} --prior_num ${_prior} --p ${probs2016[$i]} --mem_kb ${mems[$i]} --high_prior ${H[0]} ${H[1]} --low_prior ${L[0]} ${L[1]} ${L[2]} ${L[3]} ${L[4]}
```
