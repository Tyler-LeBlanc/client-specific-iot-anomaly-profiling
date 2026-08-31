# Client-Specific Adaptive Anomaly Profiling for IoT/IIoT

This repository contains the simulation code and experimental results associated
with our client-specific adaptive anomaly-profiling framework for IoT and IIoT
network traffic.

The framework constructs general device-type profiles and personalizes them for
individual clients using trusted enrollment traffic. Online monitoring uses
Fisher-weighted anomaly scoring, guarded client-profile adaptation, drift
confirmation, and temporal evidence aggregation.

This repository is provided primarily to document the implementation used in
the associated research paper and to make the simulation code and experimental
outputs available for inspection.

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
```

## Simulation Code

The `simulations/` directory contains the three dataset-specific simulation
notebooks used for the experiments reported in the paper:

- `simulations/datasense_2025/simulation.ipynb`
- `simulations/cic_iot_2022/simulation.ipynb`
- `simulations/n_baiot/simulation.ipynb`

The notebooks implement the dataset-specific preprocessing, general
device-type profile construction, client enrollment, Particle Swarm
Optimization (PSO), online adaptive monitoring, and experimental evaluation.

The three simulations share the common profile and scoring implementation
contained in:

```text
simulations/profiles.py
```

This module defines the general device-type and client-specific profile
structures and the Fisher-weighted Z-score calculations used throughout the
experiments.

## Datasets

The experiments use three publicly available IoT/IIoT datasets:

- CIC DataSense IIoT 2025
- CIC IoT 2022
- N-BaIoT

The raw datasets are not redistributed in this repository due to their size and
original distribution requirements.

Additional information is provided in `data/README.md`.

Because the datasets are not included, the notebooks are provided primarily as
the simulation implementations used to produce the results reported in the
paper. Dataset paths may need to be configured locally if the simulations are
re-executed.

## Experimental Results

The `results/` directory contains the output files generated from the
experiments and is organized by dataset:

```text
results/
├── cic_iot_2022/
├── datasense_2025/
└── n_baiot/
```

The result files include the primary performance measurements and supporting
experimental outputs used in the analysis, including:

- Overall false-positive and detection results
- Device and device-type performance
- Selected PSO parameter configurations
- Fisher feature weights
- Runtime measurements
- Storage measurements
- Dataset split summaries and supporting evaluation results

The exact available outputs vary by dataset according to the evaluation
supported by each dataset.

## Software Requirements

The simulations were developed in Python using Jupyter notebooks.

The primary dependencies are listed in `requirements.txt`:

```text
numpy
pandas
scikit-learn
matplotlib
jupyterlab
nbformat
```

The PSO procedure used by the framework is implemented directly within the
simulation notebooks using NumPy and does not depend on an external PSO
library.

## Reproducibility

Randomized experimental operations use a fixed random seed of `42`.

Training, enrollment, PSO-tuning, and final evaluation partitions are separated
within the simulations so that the final reported test partitions are not used
during profile construction or parameter calibration.

The included notebooks and result files are intended to document the exact
experimental implementation and outputs associated with the paper.
