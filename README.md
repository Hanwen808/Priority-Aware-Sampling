# Priority-Aware-Sampling
VLDB'2025
Spread estimation, which counts the number of non-duplicates in
each flow, has wide applications. Under the limited memory, admin-
istrators have to prioritize achieving higher estimation accuracy for
error-sensitive flows while maintaining acceptable performance for
others to fulfill measurement requirements. In this paper, we inves-
tigate a new problem called differential flow spread estimation
and propose priority-aware sampling, a novel hybrid framework to
catch the line speed of switches while estimating different types
of flows with different accuracy demands. In the on-chip memory,
we elaborately designed a priority-aware filter that memorizes and
removes duplicates based on priorities, i.e., error tolerance. This
design not only alleviates hash conflicts between high-priority and
low-priority elements but also assigns a higher sampling rate to
high-priority flows, effectively reducing their estimation errors
within the same memory. Additionally, we utilize sufficient off-chip
memory to record downloads from on-chip memory and provide
unbiased spread estimation for each flow after the measurement.
The experimental results, obtained from real-world datasets and rig-
orously analyzed mathematically, show that our proposal reduces
estimation errors for high-priority flows by 29.52% in uniform pri-
ority distribution and 32.03% in Zipf priority distribution compared
to the state-of-the-art (NDS).
