# Time log

| Date | Hours | What I did |
| :--- | :---: | :--- |
| 2026-10-16 | 1.0 | Initial thesis repository setup: virtual environment (Python 3.12, Qiskit 2.6.0, Qiskit Aer 0.17.2), dependency management, directory structure, and `00_setup_check.ipynb`. |
| 2026-10-16 | 2.0 | Implemented foundational quantum computing notebooks: four Bell states (`01_bell_states.ipynb`), Deutsch–Jozsa algorithm (`02_deutsch_jozsa.ipynb`), and 3-qubit Grover search (`03_grover.ipynb`). |
| 2026-10-16 | 1.5 | Developed classical Max-Cut baseline solvers (`src/maxcut.py`): exact brute force, random search, and greedy local search with self-tests on 4-cycle and $G(6, 0.6)$. |
| 2026-10-16 | 1.5 | Created and executed `00b_linear_algebra_review.ipynb`: pure NumPy validation of statevector norms, inner/outer products, unitary vs. Hermitian operators, Kronecker products, and single-edge Max-Cut cost Hamiltonian $C_{ij} = \frac{1}{2}(I_4 - Z \otimes Z)$. |
| 2026-10-16 | 2.0 | Created and executed `01b_single_qubit_gates.ipynb`: exact vs. 4096-shot Aer simulation of Pauli $X, Z$, Hadamard $H$, phase interferometry ($HZH=X$), phase gates $S, T$ on Bloch sphere, continuous rotations $R_Y, R_X, R_Z$, and connection to QAOA cost ($R_Z$) and mixer ($R_X$) layers. |
| 2026-10-16 | 2.0 | Implemented and executed `04_qaoa_maxcut_p1.ipynb`: QAOA depth $p=1$ on 4-cycle graph $C_4$, parameter landscape grid search over $(\gamma, \beta)$, optimal cut recovery ($\alpha = 0.75$), and Aer sampling. |
| 2026-10-16 | 1.5 | Implemented and executed `05_bell_noise.ipynb`: NISQ noise modeling with depolarizing gate noise and readout bit-flip error, demonstrating 8.5% error rate and two-qubit gate error sweep. |
| 2026-10-16 | 1.0 | Created Month 1 learning summary outline and numerical cheat sheet (`docs/month1_learning_summary_outline.md`) mapping executed results and literature to RQ1–RQ4. |
| 2026-10-16 | [1.5] | *[Planned / Arman]*: Draft 1–2 page Month 1 progress report prose from outline, review executed notebook outputs, and prepare discussion points for Dr. Isaac Woungang. |
| 2026-11-19 | 1.0 | Audited Month 1 references against original PDFs/arXiv records and updated verified titles and arXiv IDs in `docs/month1_learning_summary_outline.md` (commit `1992648`). |
| 2026-11-26 | 2.0 | Reran `src/maxcut.py` baselines, verified Python 3.12.16/Qiskit notebook outputs, compiled the Month 2 weekly log (`docs/weekly_progress_log.md`), and prepared the 3-page supervisor report. |

**Totals:** October completed `12.5` h (+ `[1.5]` h planned) · November completed `3.0` h · **Total completed:** `15.5` h.
