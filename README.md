# Priority-aware sampling
## Introduction
Given the switch's limited on-chip memory, many sketches have been proposed for efficient spread estimation for high-speed network streams.
Nevertheless, existing methods ignore the truth that different types of flows exhibit varying error tolerance to measurement, thus necessitating administrators to prioritize ensuring the estimation accuracy for error-sensitive flows.
In this paper, we investigate a new problem called Differential Flow Spread Estimation and propose priority-aware sampling (PAS), a novel hybrid framework to catch up with the line speed of switches while estimating different types of flows with different accuracy requirements.
In on-chip memory, we elaborately design a priority-aware filter that removes duplicate elements and memorizes as many high-priority elements as possible. 
This design enables reallocating on-chip resources from low-priority elements to higher-priority elements, thereby improving estimation accuracy for high-priority flows.
Meanwhile, we deploy a one-access hash table to efficiently record distinct elements and provide unbiased spread estimation in real-time.
Additionally, we demonstrate that our proposal is flexible and configurable for a variety of performance guarantees.
We implement PAS in hardware using NetFPGA.
The experimental results based on real Internet traces show that PAS reduces estimation errors for high-priority flows by 96.41%, 92.22% and 46.76% compared to the vHLL, rSkt, and state-of-the-art (NDS), respectively, under uniform prioritization.

## About this repo

- `C++ Implementation` contains source code for C++ implementations of PAS and related work, which includes vHLL, rSkt(HLL), and NDS.
- `Python Implementation` contains source code for python implementations of PAS and related work, which includes vHLL, rSkt(HLL), and NDS.
- `FPGA Implementation` contains the source code for NetFPGA implementation.
