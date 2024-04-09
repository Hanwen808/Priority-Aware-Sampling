# Priority-Aware-Sampling
## Introduction
Given switchs' limited on-chip memory, many sketches have been proposed to achieve accurate per-flow cardinality estimation for high-speed network streams.
Nevertheless, existing methods ignore the truth that different types of flows exhibit varying error tolerance to measurement, thus necessitating administrators to prioritize ensuring the estimation accuracy for error-sensitive flows.
In this paper, we investigate a new problem called \textbf{differential flow cardinality estimation} and propose \textbf{p}riority-\textbf{a}ware \textbf{s}ampling (\textit{PAS}), a novel hybrid framework to catch the line speed of switches while estimating different types of flows with different accuracy requirements.
In the on-chip memory, we elaborately designed a priority-aware filter that memorizes and removes duplicates based on priorities, \textit{i.e.}, error tolerance. 
This design not only alleviates hash conflicts between high-priority and low-priority elements but also assigns a higher sampling rate to high-priority flows, effectively reducing their estimation errors within the same memory.
Meanwhile, we utilize sufficient off-chip memory to record downloads from on-chip memory and provide unbiased cardinality estimation for each flow after the measurement.
Additionally, we demonstrate PAS is highly configurable for a variety of performance guarantees.
The experimental results based on real-world datasets show that PAS reduces estimation errors for high-priority flows by $96.41\%$ and $46.76\%$ compared to the vHLL and state-of-the-art (NDS), respectively, under uniform prioritization.
