# Client-Specific Adaptive Anomaly Profiling for IoT/IIoT

This repository contains the simulation code and experimental results
associated with our client-specific adaptive anomaly-profiling framework
for IoT and IIoT network traffic.

The framework constructs general device-type profiles and then
personalizes them for individual clients using trusted enrollment traffic.
Online monitoring uses Fisher-weighted anomaly scoring, guarded
client-profile adaptation, drift confirmation, and temporal evidence
aggregation.

The three simulation notebooks share the common device-type and client-profile
implementation in `simulations/profiles.py`.

## Repository Structure

```text
.
├── data/
│   └── README.md
│
├── results/
│   ├── cic_iot_2022/
│   ├── datasense_2025/
│   └── n_baiot/
│
├── simulations/
│   ├── profiles.py
│   ├── cic_iot_2022/
│   │   └── simulation.ipynb
│   ├── datasense_2025/
│   │   └── simulation.ipynb
│   └── n_baiot/
│       └── simulation.ipynb
│
├── .gitignore
├── README.md
└── requirements.txt
