# CPS40A/B – Weekly Research Log, Progress Reports & Evidence

**Thesis Title:** Design and Performance Evaluation of Noise-Aware Quantum Optimization Algorithms Using Hybrid Quantum–Classical Computing  
**Course:** CPS40A/B — Computer Science Thesis (Toronto Metropolitan University, 2026–2027)  
**Student:** Arman Fathabadi (Toronto Metropolitan University)  
**Supervisors:** Dr. Isaac Woungang (TMU) & Dr. Ajmery Sultana (Algoma University)  
**Code & Experiment Repository:** [https://github.com/Arman-Fathabadi/qaoa-thesis](https://github.com/Arman-Fathabadi/qaoa-thesis)  
**Verified Environment:** Python `3.12.16` | Qiskit `2.6.0` | Qiskit Aer `0.17.2` | NetworkX | NumPy/SciPy | Matplotlib | JupyterLab `4.6.4`

---

## Course & Research Milestone Tracker

| Milestone / Phase | Target Window | Official Status | Key Deliverables |
| :--- | :--- | :--- | :--- |
| **Phase 1 / Month 1** *(Fall Report #1)* | Oct 2026 | **Completed (Code & Outline)** | Environment setup, linear algebra validation, basic quantum circuit demos (`00`–`05`, `00b`, `01b`), initial QAOA `p=1` & noise sweep |
| **Phase 2 / Month 2** *(Fall Report #2 — Due Nov 27)* | Nov 2026 | **In Progress / Ready for Review** | QAOA & NISQ noise literature review, formal Max-Cut Ising formulation, classical baseline solvers (`src/maxcut.py`) |
| **Phase 3 / Month 3** | Dec 2026 | Upcoming | Scale QAOA (`p = 1, 2`; `3` if feasible) to 6- and 8-node graphs; validate against exact brute-force solutions |
| **Phase 3–4 / Month 4** *(Mid-Term Assessment)* | Jan 2027 | Upcoming | Full benchmarking across depth & optimizers; Semester 1 progress report & mid-year review |
| **Months 5–8** *(Winter Term)* | Feb–Apr 2027 | Upcoming | Gate/readout/shot noise sweeps, noise-aware depth/configuration strategy, Winter reports (Feb 26, Mar 26), Final thesis & seminar |

---

# Weekly Update 2: Nov 20 – Nov 27, 2026 *(Fall Monthly Report #2 / Month 2)*

## 1. Summary of Work Completed This Week
- **Literature Review & Formulation Write-Up:** Synthesized the 5 QAOA and NISQ noise research papers (arXiv citations verified Nov 19, commit [`1992648`](https://github.com/Arman-Fathabadi/qaoa-thesis/commit/1992648c612c0dba71ce32a6cad166fefe738ece)) plus IBM Quantum documentation, and formalized the Max-Cut Ising mapping for the Month 2 report.
- **Re-Verification of Existing Baselines:** Reran the existing classical Max-Cut baseline tests in [`src/maxcut.py`](https://github.com/Arman-Fathabadi/qaoa-thesis/blob/main/src/maxcut.py) (originally committed Oct 16, commit [`6079836`](https://github.com/Arman-Fathabadi/qaoa-thesis/commit/6079836136f64edd2f812742d386b34d5d0e0230)), confirming reproducible results on $C_4$ (`4/4/4`) and seeded $G(6, 0.6)$ (`8/8/8`).
- **Consolidation of Evidence:** Compiled all executed notebooks, verified simulator metrics, extracted figures, and original commit history into this running weekly progress log ahead of the **November 27** checkpoint.

---

## 2. Literature Review Summary (Month 2 Deliverable)

1. **Farhi, E., Goldstone, J., & Gutmann, S. (2014).** *A Quantum Approximate Optimization Algorithm.* [`arXiv:1411.4028`](https://arxiv.org/abs/1411.4028)  
   - **Summary:** Introduces QAOA using alternating parameterized cost unitaries $U(C, \gamma) = e^{-i\gamma C}$ and mixer unitaries $U(B, \beta) = e^{-i\beta B}$ over circuit depth $p$. Proves a worst-case approximation ratio bound of $\alpha \ge 0.6924$ on 3-regular graphs at $p=1$ and that the best ideal expected objective is nondecreasing with depth $p$ when parameters are globally optimized (converging toward the optimum as $p \to \infty$), while framing comparison against classical approximation bounds such as Goemans–Williamson ($0.878$).  
   - **Relevance to Thesis:** Directly defines our **RQ1** ideal baseline ansatz and **RQ4** classical-vs-quantum comparison criteria.

2. **Blekos, K., Brand, D., Ceschini, A., Chou, C.-H., Li, R.-H., Pandya, K., & Summer, A. (2024).** *A Review on Quantum Approximate Optimization Algorithm and its Variants.* *Physics Reports*, Vol. 1068, pp. 1–66. [`arXiv:2306.09198`](https://arxiv.org/abs/2306.09198)  
   - **Summary:** Comprehensive survey analyzing QAOA performance on Max-Cut/QUBO instances, extensions of cost and mixer operators, classical parameter optimization techniques (COBYLA, Nelder-Mead, SPSA, gradient methods), barren plateaus, and noise vulnerability on NISQ hardware.  
   - **Relevance to Thesis:** Guides classical optimizer selection and experimental variables across **RQ1, RQ2, and RQ3**.

3. **Sturm, A. (2023).** *Theory and Implementation of the Quantum Approximate Optimization Algorithm: A Comprehensible Introduction and Case Study Using Qiskit and IBM Quantum Computers.* [`arXiv:2301.09535`](https://arxiv.org/abs/2301.09535)  
   - **Summary:** Pedagogical guide pairing QAOA mathematical formulation directly with IBM Qiskit implementation code, supplemented by real hardware experiments executed on a 27-qubit IBM processor (`ibmq_ehningen`), illustrating practical circuit transpilation and fidelity loss under real device noise.  
   - **Relevance to Thesis:** Provides direct Qiskit implementation patterns (**RQ1**) and hardware-fidelity context (**RQ2, RQ3**).

4. **Resch, S. (2021).** *Introductory Tutorial for SPSA and the Quantum Approximation Optimization Algorithm.* [`arXiv:2106.01578`](https://arxiv.org/abs/2106.01578)  
   - **Summary:** Concise, implementation-focused tutorial (~100 lines in Qiskit/Python and R) solving graph Max-Cut end-to-end with QAOA using the **SPSA** (Simultaneous Perturbation Stochastic Approximation) optimizer, which estimates gradients with only two function evaluations per iteration regardless of parameter dimension.  
   - **Relevance to Thesis:** Motivates evaluating SPSA alongside standard grid search / COBYLA under noisy sampling (**RQ2, RQ3**).

5. **Marshall, J., Wudarski, F., Hadfield, S., & Hogg, T. (2020).** *Characterizing local noise in QAOA circuits.* *IOP SciNotes*, Vol. 1, No. 2, 025208. [`arXiv:2002.11682`](https://arxiv.org/abs/2002.11682)  
   - **Summary:** Derives approximate closed-form analytical expressions for output state fidelity and cost-function degradation in QAOA as explicit functions of gate error rate, qubit count $n$, and circuit depth $p$. Demonstrates why noisy execution creates an accuracy–depth trade-off where deeper circuits can underperform shallower ones.  
   - **Relevance to Thesis:** Provides the core theoretical justification for **RQ2** (depth vs. noise degradation) and **RQ3** (noise-aware circuit-depth selection).

6. **IBM Quantum Documentation & Learning Resources:** *Basics of Quantum Information*, *QAOA Tutorial*, and *Build Noise Models* (`qiskit_aer.noise`).  
   - **Relevance to Thesis:** Defines the simulation infrastructure (`AerSimulator`, `NoiseModel`, `depolarizing_error`, `ReadoutError`) used throughout Phases 1–4.

---

## 3. Max-Cut Mathematical Formulation & Classical Baselines

### Problem Formulation
Given an undirected graph $G = (V, E)$ with $|V| = n$ vertices and edge weights $w_{ij}$ ($w_{ij} = 1$ for unweighted graphs), Max-Cut partitions $V$ into two subsets $S_0, S_1$ ($x_i \in \{0, 1\}$) to maximize the weight of edges crossing between subsets:
$$C(x) = \sum_{(i, j) \in E} w_{ij} \, x_i (1 - x_j) + (1 - x_i) x_j$$

Mapping binary labels $x_i \in \{0, 1\}$ to spin variables $z_i = 1 - 2x_i \in \{+1, -1\}$ yields the diagonal Ising cost Hamiltonian used in QAOA:
$$H_C = \sum_{(i, j) \in E} \frac{w_{ij}}{2} \left(I - Z_i Z_j\right)$$
Because $z_i z_j = -1$ when vertices $i$ and $j$ lie on opposite sides of the cut and $+1$ when on the same side, each cut edge contributes $+w_{ij}$ and each uncut edge contributes $0$. In `notebooks/00b_linear_algebra_review.ipynb`, we verified numerically for a single edge that $C_{ij} = \frac{1}{2}(I_4 - Z \otimes Z)$ has diagonal eigenvalues `[0, 1, 1, 0]` across `{|00⟩, |01⟩, |10⟩, |11⟩}`.

### Classical Baseline Results (`src/maxcut.py` — Verified Execution)
Implemented and verified three classical solvers (`brute_force`, `random_search`, and `greedy_local_search` with multiple random restarts):

| Graph Instance | $|V|$ | $|E|$ | Exact (`brute_force`) | `random_search` | `greedy_local_search` (10 restarts) | Key Observation |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **4-Cycle ($C_4$)** | 4 | 4 | **4** (`0101`/`1010`) | **4** (200 samples) | **4** (test asserts $\ge 2$) | Simple bipartite graph; all baselines recover optimum |
| **Random $G(6, 0.6)$** (`seed=42`) | 6 | 10 | **8** | **8** (500 samples) | **8** (10 restarts) | Validated exact, random, and multi-restart greedy baselines (`all maxcut tests passed`) |

---

## 4. Evidence & Artifacts Checklist (Week of Nov 20–27)

- **Code Files:** [`src/maxcut.py`](https://github.com/Arman-Fathabadi/qaoa-thesis/blob/main/src/maxcut.py), [`docs/month1_learning_summary_outline.md`](https://github.com/Arman-Fathabadi/qaoa-thesis/blob/main/docs/month1_learning_summary_outline.md)
- **GitHub Commit Links:**
  - `1992648`: Fixed verified arXiv titles/IDs in literature cheat sheet ([commit](https://github.com/Arman-Fathabadi/qaoa-thesis/commit/1992648c612c0dba71ce32a6cad166fefe738ece))
  - `6079836`: Added classical Max-Cut baselines with self-tests ([commit](https://github.com/Arman-Fathabadi/qaoa-thesis/commit/6079836136f64edd2f812742d386b34d5d0e0230))
- **Verified Outputs & Figures:**
  - Classical self-tests (`src/maxcut.py`): `C4 exact/random/greedy: 4 4 4`; `G(6,0.6) edges=10 exact/random/greedy: 8 8 8` (`all maxcut tests passed`).
  - Depth-1 QAOA `C4` parameter landscape & 2,048-shot histogram (`notebooks/04_qaoa_maxcut_p1.ipynb`).
  - Bell-state depolarizing + readout noise error & 2-qubit sweep (`notebooks/05_bell_noise.ipynb`).
- **Time Logged:** See [`time_log.md`](https://github.com/Arman-Fathabadi/qaoa-thesis/blob/main/time_log.md) (`12.5` completed hours in October + `1.5` planned; `3.0` completed hours in November — **`15.5` completed hours total**).

---

## 5. Questions & Plan for Next Week (Nov 27 – Dec 4, 2026)

### Discussion Questions for Supervisors (Nov 27 Meeting)
1. Should our Phase 2–3 Max-Cut benchmark graphs (`n = 4, 6, 8`) include **weighted edges** as well as unweighted cycle and Erdős–Rényi random graphs?
2. For Phase 3 noise experiments, should we focus primarily on **controlled parameterized models** (`depolarizing_error` + `ReadoutError` in `qiskit_aer`) or also benchmark against a simulated IBM hardware profile (e.g., `FakeBackend`)?

### Action Plan for Next Week (Month 3 Start)
- Extend classical baseline evaluation to **8-node** benchmark graphs (`G(8, 0.5)`) and log comparison timings.
- Scale the QAOA implementation from $C_4$ ($p=1$) to **6-node and 8-node graphs** at depths **$p = 1$ and $p = 2$**, replacing grid search with classical optimizers (COBYLA / SPSA) and validating approximation ratio $\alpha = \langle C \rangle / C^*$ against `brute_force`.

---
---

# Prior Baseline Log: Oct 16 – Nov 19, 2026 *(Phase 1 / Month 1 Foundation)*

## 1. Environment Installation & Verification
- Set up dedicated local repository with Python `3.12.16` (`.venv`), Git version control, and `requirements.txt` (107 pinned dependencies).
- Installed and verified **Qiskit `2.6.0`**, **Qiskit Aer `0.17.2`**, **NumPy**, **SciPy**, **NetworkX**, **Matplotlib**, **pylatexenc**, and **JupyterLab `4.6.4`**.
- Executed `00_setup_check.ipynb` (`1000` shots on `AerSimulator`) yielding `{'11': 514, '00': 486}`.

---

## 2. Working Quantum Circuit Demonstrations & Empirical Results

All 8 foundational notebooks were implemented, executed, and committed to `notebooks/`:

| Notebook | Focus & Quantum Concepts Verified | Key Executed Results (`AerSimulator`) | GitHub Link |
| :--- | :--- | :--- | :--- |
| `00_setup_check.ipynb` | Toolchain verification & ideal Bell circuit | `1000` shots: `'11': 514`, `'00': 486` | [link](https://github.com/Arman-Fathabadi/qaoa-thesis/blob/main/notebooks/00_setup_check.ipynb) |
| `00b_linear_algebra_review.ipynb` | Norm preservation, orthogonality, Unitary vs. Hermitian gates, Kronecker products, $C_{ij}$ Hamiltonian | Confirmed $X,Y,Z,H$ are Unitary+Hermitian; $S,T,R_Y$ Unitary only; $\text{diag}(C_{ij})=[0,1,1,0]$ | [link](https://github.com/Arman-Fathabadi/qaoa-thesis/blob/main/notebooks/00b_linear_algebra_review.ipynb) |
| `01_bell_states.ipynb` | Entanglement across all 4 Bell states ($\Phi^\pm, \Psi^\pm$) | `1000` shots each: `0%` parity error (`phi+`: `526/474`, `phi-`: `528/472`, `psi+`: `504/496`, `psi-`: `499/501`) | [link](https://github.com/Arman-Fathabadi/qaoa-thesis/blob/main/notebooks/01_bell_states.ipynb) |
| `01b_single_qubit_gates.ipynb` | Pauli $X, Z$, Hadamard $H$, phase interferometry ($HZH=X$), $S/T$ gates, rotations $R_X, R_Y, R_Z$ (`shots=4096`) | $HZH$ on ket-0 $\to$ `'1': 4096` (`100%`); $R_Y(\pi/3) \to$ `'0': 3083 (75.27%)`, `'1': 1013 (24.73%)` | [link](https://github.com/Arman-Fathabadi/qaoa-thesis/blob/main/notebooks/01b_single_qubit_gates.ipynb) |
| `02_deutsch_jozsa.ipynb` | Quantum parallelism & single-query oracle classification ($n=3$, `shots=1000`) | Constant oracles $\to$ `'000': 1000`; Balanced oracle $\to$ `'111': 1000` (`100%` accuracy in 1 query) | [link](https://github.com/Arman-Fathabadi/qaoa-thesis/blob/main/notebooks/02_deutsch_jozsa.ipynb) |
| `03_grover.ipynb` | Amplitude amplification ($n=3, N=8$, target `101`, $R=2$ iterations, `shots=2000`) | Target `'101'`: `1873/2000` (**`93.65%`** vs. `12.5%` classical random baseline) | [link](https://github.com/Arman-Fathabadi/qaoa-thesis/blob/main/notebooks/03_grover.ipynb) |
| `04_qaoa_maxcut_p1.ipynb` | QAOA depth $p=1$ on 4-cycle $C_4$, $41 \times 41$ parameter grid search over $(\gamma,\beta) \in [0,\pi]^2$ | $\gamma^*=2.356$ ($3\pi/4$), $\beta^*=2.749$ ($7\pi/8$); $\langle C \rangle = 3.000/4.0$ ($\alpha = \mathbf{0.750}$); optimal cuts `'1010'` (559) + `'0101'` (520) = `52.69%` of 2048 shots | [link](https://github.com/Arman-Fathabadi/qaoa-thesis/blob/main/notebooks/04_qaoa_maxcut_p1.ipynb) |
| `05_bell_noise.ipynb` | NISQ `NoiseModel` (`depolarizing_error` + `ReadoutError`, `shots=4000`) & 2-qubit error sweep | Ideal: `0.0%` error $\to$ Noisy ($p_1=0.1\%, p_2=1.0\%, p_{\text{ro}}=2.0\%$): `'01': 157, '10': 182` (`339/4000` = **`8.475%` error**); 2-qubit sweep ($p_2 \in [0, 0.20]$): `0.0%` $\to$ `~10.5%` | [link](https://github.com/Arman-Fathabadi/qaoa-thesis/blob/main/notebooks/05_bell_noise.ipynb) |

---

## 3. GitHub Commit History & Time Log Evidence

| Commit | Date | Summary of Deliverable |
| :--- | :--- | :--- |
| [`be09fd3`](https://github.com/Arman-Fathabadi/qaoa-thesis/commit/be09fd39201249917d05ff4902529a3098d2ed8d) | 2026-10-16 | Initial thesis environment setup (`.gitignore`, pinned `requirements.txt`) |
| [`459956f`](https://github.com/Arman-Fathabadi/qaoa-thesis/commit/459956fd67b031f0759667e993dde423aa268896) | 2026-10-16 | Created repository layout (`notebooks/`, `src/`, `results/`, `README.md`, `time_log.md`) |
| [`04917a4`](https://github.com/Arman-Fathabadi/qaoa-thesis/commit/04917a4141b2adb0e1ba2cea3478e0d3ce251c7c) | 2026-10-16 | Added executed `00_setup_check.ipynb` |
| [`7bd4993`](https://github.com/Arman-Fathabadi/qaoa-thesis/commit/7bd4993ea035384e8bc81c6fdb6e3a9a3801ca48) | 2026-10-16 | Added executed notebooks `01`–`05` (Bell states, Deutsch–Jozsa, Grover, QAOA `p=1`, Bell noise) |
| [`6079836`](https://github.com/Arman-Fathabadi/qaoa-thesis/commit/6079836136f64edd2f812742d386b34d5d0e0230) | 2026-10-16 | Added classical Max-Cut baseline solvers (`src/maxcut.py`) with self-tests |
| [`2b13138`](https://github.com/Arman-Fathabadi/qaoa-thesis/commit/2b13138a35d5ae7aa8dc19d130e032ba41b9048a) | 2026-10-16 | Added executed `01b_single_qubit_gates.ipynb` (Bloch sphere & rotation validation) |
| [`7562fb3`](https://github.com/Arman-Fathabadi/qaoa-thesis/commit/7562fb3d8b063e6ddca8040127e0811c914fe088) | 2026-10-16 | Added executed `00b_linear_algebra_review.ipynb` (NumPy & $C_{ij}$ validation) |
| [`4987761`](https://github.com/Arman-Fathabadi/qaoa-thesis/commit/49877618a09cc88785f4fb0e944e413a61f660b3) | 2026-10-16 | Added Month 1 summary outline & numerical cheat sheet |
| [`5229f9f`](https://github.com/Arman-Fathabadi/qaoa-thesis/commit/5229f9f35876655c71c5a738a6c007e8180d764f) | 2026-10-16 | Updated `time_log.md` (`12.5` completed hours + `1.5` planned prose hour for Month 1) |
| [`1992648`](https://github.com/Arman-Fathabadi/qaoa-thesis/commit/1992648c612c0dba71ce32a6cad166fefe738ece) | 2026-11-19 | Verified and corrected literature reference titles and arXiv IDs in `docs/month1_learning_summary_outline.md` |
