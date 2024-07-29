# Python Codes for PAS and Baselines

## Descriptions
We evaluate the estimation performance of our proposal and compared it with state-of-the-art algorithms. The run command is as follows.

```shell
./scripts/exp_accuracy.sh
```

We can also evaluate the estimation accuracy for different algorithms with different memory configurations and other parameters. The run command is as follows.

```shell
python -W ignore ../main.py --method "nds" --dataset ${_dataset} --prior_num ${_prior} --p ${probs2016[$i]} --mem_kb ${mems[$i]} --high_prior ${H[0]} --low_prior ${L[0]} ${L[1]}
python -W ignore ../main.py --method "nds" --dataset ${_dataset} --prior_num ${_prior} --p ${probs2016[$i]} --mem_kb ${mems[$i]} --high_prior ${H[0]} ${H[1]} --low_prior ${L[0]} ${L[1]} ${L[2]} ${L[3]} ${L[4]}
python ../main.py --method "vhll" --dataset ${_dataset} --prior_num ${_prior} --mem_kb ${mems[$i]} --v 16 --high_prior ${H[0]} --low_prior ${L[0]} ${L[1]}
python ../main.py --method "vhll" --dataset ${_dataset} --prior_num ${_prior} --mem_kb ${mems[$i]} --v 16 --high_prior ${H[0]} ${H[1]} --low_prior ${L[0]} ${L[1]} ${L[2]} ${L[3]} ${L[4]}
python ../main.py --method "rskt" --dataset ${_dataset} --prior_num ${_prior} --mem_kb ${mems[$i]} --v 32 --high_prior ${H[0]} --low_prior ${L[0]} ${L[1]}
python ../main.py --method "rskt" --dataset ${_dataset} --prior_num ${_prior} --mem_kb ${mems[$i]} --v 32 --high_prior ${H[0]} ${H[1]} --low_prior ${L[0]} ${L[1]} ${L[2]} ${L[3]} ${L[4]}
python -W ignore ../main.py --method "pas" --dataset "${_dataset}" --prior_num "${_prior}" --mem_kb "${mems[$i]}" --pre ${param0[0]} ${param0[1]} ${param0[2]} --post ${param00[0]} ${param00[1]} ${param00[2]} --high_prior ${H[0]} --low_prior ${L[0]} ${L[1]}
python -W ignore ../main.py --method "pas" --dataset "${_dataset}" --prior_num "${_prior}" --mem_kb "${mems[$i]}" --pre ${param0[0]} ${param0[1]} ${param0[2]} ${param0[3]} ${param0[4]} ${param0[5]} ${param0[6]} --post ${param00[0]} ${param00[1]} ${param00[2]} ${param00[3]} ${param00[4]} ${param00[5]} ${param00[6]} --high_prior ${H[0]} ${H[1]} --low_prior ${L[0]} ${L[1]} ${L[2]} ${L[3]} ${L[4]}
```
