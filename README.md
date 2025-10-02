# chain-tools
This repository contains a suite of Python scripts designed to facilitate the rapid generation of customized, high-quality test data on a local Anvil development network.

## Anvil Data Generator (Python/Web3)

## 🚨 Security & Ethical Use Disclaimer
This repository is strictly intended for ethical security research, vulnerability analysis, and local, controlled testing environments.

The tools provided here interact with blockchain infrastructure to simulate transactions and generate state data. DO NOT use these scripts or techniques against public mainnets, shared testnets, or any environment where you do not have explicit permission from the owner. Misuse of these tools against unauthorized targets is unethical and potentially illegal.

We promote responsible disclosure and rigorous security testing within legal and ethical boundaries.

## 💡 Overview

This repository contains a suite of Python scripts designed to facilitate the rapid generation of customized, high-quality test data on a local Anvil development network.

By leveraging the powerful combination of the web3.py library and eth-account, these tools allow researchers and developers to create complex, repeatable blockchain scenarios necessary for in-depth security analysis and development testing.

## Prerequisites

Create a Python 3 environment and install the required libraries.

```
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Run the tests with `pytest`:

```
pytest
```

The file `.env.example` contains a list of environment variables. 
Create a `.env` in the root directory and populate the variables accordingly.
