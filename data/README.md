# Dataset Information

The raw datasets used by the simulations are not included in this repository.

The experiments use three publicly available IoT/IIoT network-traffic datasets. These datasets must be obtained separately from their original distribution sources if the simulations are to be re-executed.

## CIC DataSense IIoT 2025

CIC DataSense IIoT 2025 is used to evaluate the proposed framework on heterogeneous IIoT devices under both benign behavioral variation and malicious network traffic.

The experiment uses benign traffic to construct general device-type profiles, perform client enrollment, tune client-specific adaptation parameters, and evaluate false-positive behavior. Available attack traffic is used to calculate Fisher feature weights and evaluate attack-detection performance.

The corresponding simulation is located at:

simulations/datasense_2025/simulation.ipynb

## CIC IoT 2022

CIC IoT 2022 is used to evaluate the framework under behavioral differences between IoT clients and device types.

The feature-level CSV data used in this experiment contain benign device traffic. As a result, this experiment primarily evaluates false-positive behavior under client heterogeneity and behavioral variation rather than attack-detection performance.

The corresponding simulation is located at:

simulations/cic_iot_2022/simulation.ipynb

## N-BaIoT

N-BaIoT contains benign and malicious network traffic collected from multiple physical IoT devices.

The malicious traffic includes Mirai and BASHLITE attack families. The dataset is used to evaluate both false-positive reduction and attack detection while applying client-specific profile adaptation.

The corresponding simulation is located at:

simulations/n_baiot/simulation.ipynb

## Dataset Availability

The datasets remain subject to the terms and distribution requirements of their original publishers and are therefore not redistributed as part of this repository.

Raw dataset files are excluded from version control through the repository's `.gitignore` configuration.

Users wishing to re-execute the simulations should obtain the corresponding datasets separately and configure the dataset paths in the appropriate simulation notebook.

The simulation notebooks are provided primarily to document the implementation used for the experiments reported in the associated research paper.
