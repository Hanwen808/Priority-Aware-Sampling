#!/bin/bash
echo "nds is running..."
./exp_nds.sh > ./log_nds.txt
echo "vhll is running..."
./exp_vhll.sh > ./log_vhll.txt
echo "rskt is running..."
./exp_rSkt.sh > ./log_rskt.txt
echo "pas is running..."
./exp_pas.sh > ./log_pas.txt
