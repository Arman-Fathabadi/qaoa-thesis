# Month 1 Learning Summary Outline & Numerical Cheat Sheet
**Thesis:** CPS40A/B: Noise-Aware QAOA for Max-Cut  
**Student:** Arman Fathabadi  
**Supervisor:** Dr. Isaac Woungang  
**Date:** October 16, 2026  
**Environment:** Python 3.12.15 | Qiskit 2.6.0 | Qiskit Aer 0.17.2 | AerSimulator (seed=42, shots=4096)

---

## Instructions for Arman
Use this outline and pre-populated numerical cheat sheet to write your 1–2 page Month 1 Progress Summary for Dr. Woungang. 
- **Academic Integrity Note:** Do not copy-paste generated prose. Instead, review the completed code cells in `notebooks/00` through `05`, `00b`, and `01b`, and synthesize the findings into your own words using the guiding prompts below.
- All numbers below reflect the exact executions from your committed repository notebooks.

---

## Section 1: Qubits, Superposition & Measurement

### Writing Prompts & Conceptual Guide
- [ ] Define the physical and mathematical model of a single qubit in $\mathbb{C}^2$ ($|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$).
- [ ] Explain the Born rule and why statevectors must satisfy unit norm ($\|\psi\|_2 = 1.0$).
- [ ] Contrast deterministic classical bits with quantum superposition created via the Hadamard gate ($H$).
- [ ] Discuss the role of the quantum phase on the Bloch sphere, specifically explaining why Z-basis measurement yields identical 50/50 statistics for $|+\rangle$ and $|-\rangle$, and how interference ($HZH = X$) converts relative phase into observable bit-flips.
- [ ] Explain continuous rotations ($R_Y, R_X, R_Z$) and how probability amplitudes map to trigonometric functions ($\cos^2(\theta/2), \sin^2(\theta/2)$).

### Exact Numerical Data from Notebooks (`00`, `00b`, `01b`)
| Experiment / State | Mathematical State / Gate | Analytical Prediction | Executed Aer Counts / Probs (`seed=42`, `shots=4096`) | Empirical vs. Exact Delta |
| :--- | :--- | :--- | :--- | :--- |
| **Normalization** (`00b`) | $\|\|0\rangle\|_2, \|\|1\rangle\|_2, \|\|+\rangle\|_2, \|\|-\rangle\|_2$ | $1.000000$ | Calculated via `np.linalg.norm`: `1.000000` | $0.000000$ |
| **Inner Products** (`00b`) | $\langle 0\|1\rangle$ (Orthogonality) | $0.0$ | Exact inner product: `0.0` | $0.0000$ |
| **Inner Products** (`00b`) | $\langle 0\|+\rangle$ (Overlap) | $1/\sqrt{2} \approx 0.707107$ | Exact inner product: `0.707107` | $0.0000$ |
| **Completeness** (`00b`) | $P_0 + P_1 = \|0\rangle\langle 0\| + \|1\rangle\langle 1\|$ | Identity $I_2$ | `np.allclose(P0 + P1, np.eye(2))` = `True` | $0.0000$ |
| **Bit Flip** (`01b`) | $X\|0\rangle \to \|1\rangle$ | $P(0)=0.0, P(1)=1.0$ | `'1': 4096` ($100.0\%$), `'0': 0` ($0.0\%$) | $0.0000$ |
| **Superposition** (`01b`) | $H\|0\rangle \to \|+\rangle$ | $P(0)=0.5, P(1)=0.5$ | `'0': 2022` ($49.37\%$), `'1': 2074` ($50.63\%$) | $\Delta = 0.0063$ ($0.63\%$) |
| **Phase Flip** (`01b`) | $Z\|0\rangle \to \|0\rangle$ | $P(0)=1.0, P(1)=0.0$ | `'0': 4096` ($100.0\%$), `'1': 0` ($0.0\%$) | $0.0000$ |
| **Phase in Z-basis** (`01b`) | $H \to Z\|0\rangle \to \|-\rangle$ | $P(0)=0.5, P(1)=0.5$ | `'0': 2022` ($49.37\%$), `'1': 2074` ($50.63\%$) | $\Delta = 0.0063$ ($0.63\%$) |
| **Interferometry** (`01b`) | $H \to Z \to H\|0\rangle$ ($HZH=X$) | $P(0)=0.0, P(1)=1.0$ | `'1': 4096` ($100.0\%$), `'0': 0` ($0.0\%$) | $0.0000$ (Deterministic) |
| **Phase Gate S** (`01b`) | $H \to S\|0\rangle \to \|+i\rangle$ | $P(0)=0.5, P(1)=0.5$ | `'0': 2022` ($49.37\%$), `'1': 2074` ($50.63\%$) | $\Delta = 0.0063$ (+Y axis) |
| **Phase Gate T** (`01b`) | $H \to T\|0\rangle$ | $P(0)=0.5, P(1)=0.5$ | `'0': 2022` ($49.37\%$), `'1': 2074` ($50.63\%$) | $\Delta = 0.0063$ ($\pi/4$ phase) |
| **Rotation $R_Y(\pi/3)$** (`01b`) | $R_Y(\pi/3)\|0\rangle$ | $P(0)=\cos^2(\pi/6)=0.75$<br>$P(1)=\sin^2(\pi/6)=0.25$ | `'0': 3083` ($75.27\%$), `'1': 1013` ($24.73\%$) | $\Delta = 0.0027$ ($0.27\%$) |
| **Rotation $R_X(\pi/3)$** (`01b`) | $R_X(\pi/3)\|0\rangle$ | $P(0)=0.75, P(1)=0.25$ | `'0': 3083` ($75.27\%$), `'1': 1013` ($24.73\%$) | $\Delta = 0.0027$ ($0.27\%$) |
| **Rotation $R_Z(\pi/3)$** (`01b`) | $H \to R_Z(\pi/3)\|0\rangle$ | $P(0)=0.5, P(1)=0.5$ | `'0': 2022` ($49.37\%$), `'1': 2074` ($50.63\%$) | $\Delta = 0.0063$ |

---

## Section 2: Quantum Gates, Linear Algebra & Entanglement

### Writing Prompts & Conceptual Guide
- [ ] Detail the mathematical distinction between **Unitary operators** ($U^\dagger U = I$, norm-preserving evolution) and **Hermitian operators** ($M^\dagger = M$, real eigenvalues/observables). Note why Pauli and Hadamard gates belong to both classes, whereas phase and rotation gates are unitary only.
- [ ] Explain the Kronecker product ($\otimes$) for building multi-qubit composite Hilbert spaces ($\mathbb{C}^2 \otimes \mathbb{C}^2 = \mathbb{C}^4$).
- [ ] Describe the generation and properties of the four maximally entangled Bell states ($|\Phi^+\rangle, |\Phi^-\rangle, |\Psi^+\rangle, |\Psi^-\rangle$). Highlight how local operations ($X, Z$) on one qubit map between all four states.
- [ ] Summarize early quantum speedup demonstrations:
  - **Deutsch–Jozsa:** Distinguishing constant vs. balanced oracles in a single query ($O(1)$ vs. $O(2^{n-1}+1)$ classical queries).
  - **Grover Search:** Amplitude amplification in $O(\sqrt{N})$ iterations vs. $O(N)$ classical unstructured search.

### Exact Numerical Data from Notebooks (`00b`, `01`, `02`, `03`)
- **Unitary vs. Hermitian Gate Classification (`00b`):**
  - $X, Y, Z, H$: `is_unitary = True`, `is_hermitian = True` (Gates AND Observables).
  - $S, T, R_Y(\pi/3)$: `is_unitary = True`, `is_hermitian = False` (State Preparation Gates only).
- **Two-Qubit Operators (`00b`):**
  - $Z \otimes Z$ eigenvalues on $\{|00\rangle, |01\rangle, |10\rangle, |11\rangle\}$: $\text{diag}(Z \otimes Z) = [+1, -1, -1, +1]$.
  - Single-edge cut Hamiltonian: $C_{ij} = \frac{1}{2}(I_4 - Z \otimes Z)$ with diagonal $[0, 1, 1, 0]$.
  - Basis expectation values: $\langle 00|C_{ij}|00\rangle = 0.0$, $\langle 01|C_{ij}|01\rangle = 1.0$, $\langle 10|C_{ij}|10\rangle = 1.0$, $\langle 11|C_{ij}|11\rangle = 0.0$.
- **The Four Bell States (`01_bell_states.ipynb`, 1000 shots):**
  - $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$: statevector `[0.7071, 0, 0, 0.7071]`; counts: `{'00': 526, '11': 474}` ($0\%$ error).
  - $|\Phi^-\rangle = \frac{|00\rangle - |11\rangle}{\sqrt{2}}$: statevector `[0.7071, 0, 0, -0.7071]`; counts: `{'00': 528, '11': 472}` ($0\%$ error).
  - $|\Psi^+\rangle = \frac{|01\rangle + |10\rangle}{\sqrt{2}}$: statevector `[0, 0.7071, 0.7071, 0]`; counts: `{'01': 504, '10': 496}` ($0\%$ error).
  - $|\Psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}}$: statevector `[0, 0.7071, -0.7071, 0]`; counts: `{'01': 509, '10': 491}` ($0\%$ error).
- **Deutsch–Jozsa Algorithm (`02_deutsch_jozsa.ipynb`, $n=3$, 1000 shots, 1 query):**
  - `constant0`: `{'000': 1000}` ($100\%$ zero state $\implies$ classified Constant).
  - `constant1`: `{'000': 1000}` ($100\%$ zero state $\implies$ classified Constant).
  - `balanced`: `{'111': 1000}` ($0\%$ zero state $\implies$ classified Balanced).
- **Grover Search (`03_grover.ipynb`, $n=3$, $N=8$, target $= |101\rangle$, 1000 shots):**
  - Optimal Grover iterations: $R = \lfloor \frac{\pi}{4}\sqrt{8} \rfloor = 2$.
  - Target state `'101'` counts: **945 / 1000** ($94.5\%$ empirical success rate).
  - Classical random guess baseline: $1/8 = 12.5\%$. Quantum speedup amplification factor: $\approx 7.56\times$.
  - Non-target background leakage: 55 counts ($5.5\%$) distributed across all remaining 7 states.

---

## Section 3: Max-Cut & QAOA $p=1$ Baseline

### Writing Prompts & Conceptual Guide
- [ ] Formulate the NP-hard Max-Cut problem on an undirected graph $G=(V, E)$.
- [ ] Map binary vertex partitions $x_i \in \{0, 1\}$ to Ising spin variables $z_i \in \{+1, -1\}$ via $x_i = (1 - z_i)/2$, leading to the Hamiltonian $C = \sum_{(i,j) \in E} \frac{1}{2}(I - Z_i Z_j)$.
- [ ] Explain the two alternating layers of the QAOA ansatz at depth $p=1$:
  - Problem/Cost unitary: $U(C, \gamma) = e^{-i\gamma C} = \prod_{(i,j)} e^{-i\frac{\gamma}{2}(I - Z_i Z_j)}$ ($CNOT \to R_Z \to CNOT$).
  - Mixer unitary: $U(B, \beta) = e^{-i\beta B} = \prod_{i \in V} R_X(2\beta)_i$.
- [ ] Describe the classical optimization loop over parameter space $(\gamma, \beta)$ to maximize the expected cut $\langle C(\gamma, \beta) \rangle = \langle \psi(\gamma, \beta)| C |\psi(\gamma, \beta)\rangle$.
- [ ] Define the Approximation Ratio ($\alpha = \langle C \rangle / C^*$) and compare QAOA against classical benchmark solvers.

### Exact Numerical Data from Notebooks (`04`, `src/maxcut.py`)
- **Classical Benchmark Solvers (`src/maxcut.py`):**
  - 4-cycle graph $C_4$ ($|V|=4, |E|=4$):
    - Exact Brute Force: Max Cut = **4** (optimal partitions: `0101` and `1010`).
    - Random Search (200 samples): Max Cut = **4**.
    - Greedy Local Search (10 restarts): Max Cut = **4**.
  - Erdős-Rényi random graph $G(6, 0.6)$ (6 nodes, 9 edges, seed=42):
    - Exact Brute Force: Max Cut = **7**.
    - Random Search (500 samples): Max Cut = **7**.
    - Greedy Local Search (10 restarts): Max Cut = **6** (illustrating local optima trapping).
- **QAOA $p=1$ on 4-Cycle Graph $C_4$ (`04_qaoa_maxcut_p1.ipynb`):**
  - Grid search resolution: $41 \times 41 = 1681$ parameter points over $\gamma \in [0, \pi]$, $\beta \in [0, \pi]$.
  - Optimal parameter angles:
    - $\gamma^* = 2.356$ radians ($3\pi/4 \approx 2.35619$).
    - $\beta^* = 2.749$ radians ($7\pi/8 \approx 2.74889$).
  - Optimal expected cut value: $\langle C \rangle = \mathbf{3.000}$ (out of maximum 4.0).
  - QAOA $p=1$ Approximation Ratio: $\alpha = \frac{3.000}{4.0} = \mathbf{0.750}$ ($75.0\%$).
  - Sampling distribution at $(\gamma^*, \beta^*)$ (2048 Aer shots):
    - Optimum cut partition `'1010'`: **559** counts ($27.29\%$).
    - Optimum cut partition `'0101'`: **520** counts ($25.39\%$).
    - Combined probability of measuring optimal cut: $\mathbf{1079 / 2048 = 52.69\%}$.
    - Suboptimal cut partitions (cut value = 2): `'0011'`: 172 ($8.40\%$), `'1001'`: 162 ($7.91\%$), etc.
    - Zero-cut partitions (`'0000'`, `'1111'`): negligible / suppressed.

---

## Section 4: Initial Noise Observations & Next Steps

### Writing Prompts & Conceptual Guide
- [ ] Discuss the physical noise mechanisms affecting NISQ (Noisy Intermediate-Scale Quantum) devices:
  - 1-qubit depolarizing gate errors ($p_1$).
  - 2-qubit entangling gate errors ($p_2$), noting that 2-qubit CNOT gates are typically an order of magnitude noisier than single-qubit gates.
  - Measurement readout errors ($p_{\text{ro}}$) caused by thermal fluctuations and state decay during readout.
- [ ] Analyze how noise corrupts quantum correlation, transforming pure Bell states into mixed density states and producing spurious non-parity measurement outcomes.
- [ ] Connect the noise sweep results to the primary thesis research questions (RQ1–RQ4): why scaling QAOA depth ($p > 1$) can decrease performance under realistic hardware noise unless noise-aware mitigation is applied.
- [ ] Outline Month 2 deliverables (noise-aware QAOA modeling, depth scaling $p=2, 3$, and zero-noise extrapolation).

### Exact Numerical Data from Notebooks (`05_bell_noise.ipynb`)
- **Baseline Ideal Simulation (4000 shots):**
  - Outcome counts: `{'00': 2018, '11': 1982}`.
  - Erroneous outcomes (`'01'`, `'10'`): 0 counts.
  - **Wrong-outcome rate: 0.000 ($0.0\%$)**.
- **Realistic NISQ Noise Model Specification:**
  - Single-qubit depolarizing error: $p_1 = 0.001$ ($0.1\%$).
  - Two-qubit depolarizing error: $p_2 = 0.010$ ($1.0\%$).
  - Readout bit-flip probability: $p_{\text{ro}} = 0.020$ ($2.0\%$).
- **Noisy Simulation Results (4000 shots):**
  - Entangled parity counts: `'00': 1852`, `'11': 1809` (Total valid = 3661 / 4000 = $91.525\%$).
  - Corrupted leakage counts: `'01': 157`, `'10': 182` (Total invalid = 339 / 4000 = $8.475\%$).
  - **Wrong-outcome error rate: 0.085 ($8.5\%$)**.
- **Two-Qubit Error Rate Sweep ($p_2 \in [0.0, 0.10]$):**
  - At $p_2 = 0.00$: Wrong-outcome rate $\approx 4.0\%$ (represents the inescapable measurement readout error floor: $2 \times p_{\text{ro}}(1 - p_{\text{ro}}) \approx 3.92\%$).
  - At $p_2 = 0.02$: Wrong-outcome rate $\approx 6.0\%$.
  - At $p_2 = 0.06$: Wrong-outcome rate $\approx 10.1\%$.
  - At $p_2 = 0.10$: Wrong-outcome rate $\approx 14.2\%$.
  - Key finding: Error rate scales approximately linearly with two-qubit gate error rate, establishing that multi-qubit entangling gates and circuit depth are the primary bottlenecks in NISQ circuits.

---

## Literature Reference Cheat-Sheet: Mapping to Thesis Research Questions (RQ1–RQ4)

### Thesis Research Questions (Context)
- **RQ1 (Algorithmic Scaling):** How does ideal QAOA approximation ratio ($\alpha$) scale with circuit depth $p$ and graph structure for Max-Cut?
- **RQ2 (Hardware Noise Vulnerability):** How do physical NISQ noise channels (depolarizing, dephasing, readout) distort QAOA landscapes and degrade cut expectation?
- **RQ3 (Noise-Aware Mitigation):** Can noise-aware parameter optimization, error mitigation (ZNE, readout correction), and compilation preserve QAOA performance?
- **RQ4 (Classical vs. Quantum Comparison):** Under what noise thresholds and graph topologies does QAOA maintain an advantage or parity over classical heuristics?

### Core Reference Matrix
1. **Farhi, Goldstone, & Gutmann (2014)** — *A Quantum Approximate Optimization Algorithm* (arXiv:1411.4028)
   - **Connection to RQ1:** Introduced the alternating cost-mixer ansatz $U(B,\beta)U(C,\gamma)$; proved that QAOA achieves approximation ratio $\alpha \ge 0.6924$ on 3-regular graphs at $p=1$, and $\lim_{p \to \infty} \alpha = 1$.
   - **Connection to RQ4:** Established the theoretical framework for comparing quantum combinatorial optimization bounds against classical approximation algorithms (e.g., Goemans-Williamson 0.878 bound).

2. **Blekos et al. (2024)** — *A Review on Quantum Approximate Optimization Algorithm and its Variants* (*Physics Reports*, Vol. 1068, pp. 1–66; `arXiv:2306.09198`)
   - **Connection to RQ1 & RQ3:** Comprehensive survey of QAOA parameter landscapes, ansatz variants, and classical optimization strategies (COBYLA, Nelder-Mead, gradient-based).
   - **Connection to RQ2 & RQ3:** Analyzes barren plateaus, reachability deficits, and hardware noise susceptibility and mitigation in NISQ execution.

3. **Sturm (2023)** — *Theory and Implementation of the Quantum Approximate Optimization Algorithm: A Comprehensible Introduction and Case Study Using Qiskit and IBM Quantum Computers* (`arXiv:2301.09535`)
   - **Connection to RQ1 & RQ2:** Connects QAOA mathematical formulation directly to step-by-step Qiskit code and includes case-study hardware experiments on a 27-qubit IBM quantum processor (`ibmq_ehningen`).
   - **Connection to RQ3:** Highlights practical fidelity and compilation limitations encountered when moving QAOA from ideal simulation to NISQ hardware.

4. **Resch (2021)** — *Introductory Tutorial for SPSA and the Quantum Approximation Optimization Algorithm* (`arXiv:2106.01578`)
   - **Connection to RQ1 & RQ3:** Provides a practical, minimal (~100-line) Python/Qiskit Max-Cut implementation using SPSA (Simultaneous Perturbation Stochastic Approximation) as the classical optimizer.
   - **Connection to RQ3:** Serves as a clean classical-optimizer reference for comparing noisy optimizer behavior in Phase 3.

5. **Marshall, Wudarski, Hadfield, & Hogg (2020)** — *Characterizing local noise in QAOA circuits* (*IOP SciNotes*, Vol. 1, No. 2, 025208; `arXiv:2002.11682`)
   - **Connection to RQ2 & RQ3:** Derives approximate closed-form equations for output state fidelity and cost-function degradation in terms of noise rate, number of qubits, and circuit depth $p$.
   - **Connection to RQ2:** Explains the core NISQ depth–noise trade-off, where deeper circuits improve theoretical expressiveness while accelerating exponential/power-law performance decay under local noise.

6. **IBM Quantum Learning / Qiskit Documentation**
   - **Connection to RQ2 & RQ3:** Provides formal specifications for modeling quantum noise via `qiskit_aer.noise` (`NoiseModel`, `depolarizing_error`, `ReadoutError`) and applying M3 matrix-free readout mitigation.
   - **Connection to RQ1 & RQ4:** Supplies standardized statevector simulation and transpilation pipelines for reproducible benchmarking against classical graph algorithms.
