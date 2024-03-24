# Priority-Aware-Sampling
## Introduction
Under the limited memory, many sketches have been proposed to achieve accurate per-flow cardinality estimation, which has wide applications.
Nevertheless, existing methods ignore the truth that different types of flows exhibit varying error tolerance to measurement, thus necessitating administrators to prioritize ensuring the estimation accuracy for error-sensitive flows.
In this paper, we investigate a new problem called differential flow cardinality estimation and propose priority-aware sampling, a novel hybrid framework to catch the line speed of switches while estimating different types of flows with different accuracy requirements.
In the on-chip memory, we elaborately designed a priority-aware filter that memorizes and removes duplicates based on priorities, i.e., error tolerance. 
This design not only alleviates hash conflicts between high-priority and low-priority elements but also assigns a higher sampling rate to high-priority flows, effectively reducing their estimation errors within the same memory.
Additionally, we utilize sufficient off-chip memory to record downloads from on-chip memory and provide unbiased cardinality estimation for each flow after the measurement.
The experimental results, obtained from real-world datasets and rigorously analyzed mathematically, show that our proposal reduces estimation errors for high-priority flows by 29.52% in uniform priority distribution and 32.03% in Zipf priority distribution compared to the state-of-the-art (NDS).
