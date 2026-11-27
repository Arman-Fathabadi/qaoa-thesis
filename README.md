# QAOA Thesis

Quantum computing experiments (Qiskit + Aer) leading to QAOA for Max-Cut.

- `notebooks/` – learning and baseline notebooks (`00`–`05`, `00b`, `01b`)
- `src/` – reusable code (`maxcut.py`, `qaoa.py`, `run_experiments.py`)
- `results/` – generated CSV benchmark tables and figures
- `time_log.md` – work log

Setup: `python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`  
Run experiments: `.venv/bin/python -m src.run_experiments`
