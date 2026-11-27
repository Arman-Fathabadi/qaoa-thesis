"""Reusable QAOA runner for Max-Cut under ideal, finite-shot, and noisy Aer simulation."""
import time
import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError, depolarizing_error

from src.maxcut import brute_force, cut_value

# Transpile into standard 1q + CNOT gates so 2-qubit noise applies to every RZZ decomposition
BASIS_GATES = ["h", "rx", "rz", "cx"]


def build_qaoa_circuit(G, gammas, betas, measure=False):
    """Build a depth-p QAOA circuit for Max-Cut on graph G."""
    nodes = list(G.nodes)
    idx = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)

    qc = QuantumCircuit(n)
    qc.h(range(n))
    for gamma, beta in zip(gammas, betas):
        for u, v, data in G.edges(data=True):
            w = data.get("weight", 1.0)
            qc.rzz(-gamma * w, idx[u], idx[v])
        qc.rx(2.0 * beta, range(n))
    if measure:
        qc.measure_all()
    return qc


def make_noise_model(p1=0.001, p2=0.01, p_ro=0.02):
    """Depolarizing gate noise (1q and 2q CNOT) plus symmetric readout bit-flip error."""
    nm = NoiseModel()
    if p1 > 0:
        nm.add_all_qubit_quantum_error(depolarizing_error(p1, 1), ["h", "rx", "rz"])
    if p2 > 0:
        nm.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ["cx"])
    if p_ro > 0:
        nm.add_all_qubit_readout_error(ReadoutError([[1 - p_ro, p_ro], [p_ro, 1 - p_ro]]))
    return nm


def _bitstring_cut(G, nodes, bitstring):
    # Qiskit returns little-endian bitstrings: reverse so index i matches nodes[i]
    assignment = {nodes[i]: int(b) for i, b in enumerate(reversed(bitstring))}
    return cut_value(G, assignment)


def circuit_stats(G, p):
    """Return (depth, cx_count) after transpiling a depth-p QAOA circuit to BASIS_GATES."""
    qc = build_qaoa_circuit(G, [0.5] * p, [0.5] * p, measure=True)
    tqc = transpile(qc, basis_gates=BASIS_GATES, optimization_level=1)
    return tqc.depth(), int(tqc.count_ops().get("cx", 0))


def evaluate_cut(G, gammas, betas, mode="statevector", shots=2048,
                 noise_model=None, seed=42, opt_val=None, sim=None):
    """Evaluate expected Max-Cut value and optimal-cut hit rate for given angles."""
    nodes = list(G.nodes)
    if mode == "statevector":
        qc = build_qaoa_circuit(G, gammas, betas, measure=False)
        probs = Statevector(qc).probabilities_dict()
        mean_cut = 0.0
        opt_prob = 0.0
        for s, prob in probs.items():
            c = _bitstring_cut(G, nodes, s)
            mean_cut += prob * c
            if opt_val is not None and c == opt_val:
                opt_prob += prob
        return float(mean_cut), float(opt_prob)

    qc = build_qaoa_circuit(G, gammas, betas, measure=True)
    if sim is None:
        sim = AerSimulator(noise_model=noise_model) if mode == "noisy" else AerSimulator()
    tqc = transpile(qc, sim, basis_gates=BASIS_GATES, optimization_level=1)
    counts = sim.run(tqc, shots=shots, seed_simulator=seed).result().get_counts()

    total_cut = 0.0
    opt_hits = 0
    for s, cnt in counts.items():
        c = _bitstring_cut(G, nodes, s)
        total_cut += cnt * c
        if opt_val is not None and c == opt_val:
            opt_hits += cnt
    return total_cut / shots, opt_hits / shots


def _run_spsa(objective, x0, maxiter=50, seed=42, a=0.25, c=0.12):
    """Basic SPSA optimizer (2 evaluations per step) for noisy or sampled objectives."""
    rng = np.random.default_rng(seed)
    x = np.array(x0, dtype=float)
    A = 0.1 * maxiter
    alpha, gamma_exp = 0.602, 0.101

    best_x = x.copy()
    best_val = objective(x)
    evals = 1

    for k in range(maxiter):
        ak = a / ((k + 1 + A) ** alpha)
        ck = c / ((k + 1) ** gamma_exp)
        delta = rng.choice([-1.0, 1.0], size=len(x))

        x_plus = x + ck * delta
        x_minus = x - ck * delta
        f_plus = objective(x_plus)
        f_minus = objective(x_minus)
        evals += 2

        for cand_x, cand_val in ((x_plus, f_plus), (x_minus, f_minus)):
            if cand_val < best_val:
                best_val = cand_val
                best_x = cand_x.copy()

        ghat = (f_plus - f_minus) / (2.0 * ck * delta)
        x = x - ak * ghat

    # Check final point too
    final_val = objective(x)
    evals += 1
    if final_val < best_val:
        best_val = final_val
        best_x = x.copy()
    return best_x, best_val, evals


def optimize_qaoa(G, p=1, optimizer="COBYLA", mode="statevector", shots=2048,
                  noise_model=None, maxiter=60, seed=42, opt_val=None):
    """Optimize QAOA parameters (gammas, betas) for Max-Cut on graph G."""
    if opt_val is None:
        opt_val, _ = brute_force(G)

    rng = np.random.default_rng(seed)
    x0 = rng.uniform(0.1, np.pi - 0.1, size=2 * p)

    sim = None
    if mode != "statevector":
        sim = AerSimulator(noise_model=noise_model) if mode == "noisy" else AerSimulator()

    eval_counter = [0]

    def loss(params):
        eval_counter[0] += 1
        gammas, betas = params[:p], params[p:]
        # Use a distinct shot seed per evaluation so stochastic optimizers see realistic variance
        shot_seed = seed * 10000 + eval_counter[0]
        val, _ = evaluate_cut(
            G, gammas, betas, mode=mode, shots=shots,
            noise_model=noise_model, seed=shot_seed, opt_val=opt_val, sim=sim
        )
        return -val

    t0 = time.perf_counter()
    if optimizer.upper() == "COBYLA":
        res = minimize(loss, x0, method="COBYLA", options={"maxiter": maxiter, "rhobeg": 0.4})
        best_params = res.x
        n_evals = eval_counter[0]
    elif optimizer.upper() == "SPSA":
        best_params, _, n_evals = _run_spsa(loss, x0, maxiter=maxiter, seed=seed)
    else:
        raise ValueError(f"Unsupported optimizer: {optimizer}")
    elapsed = time.perf_counter() - t0

    # Fresh evaluation of the best parameters to avoid selection bias on noisy estimates
    gammas, betas = best_params[:p], best_params[p:]
    final_cut, opt_prob = evaluate_cut(
        G, gammas, betas, mode=mode, shots=shots,
        noise_model=noise_model, seed=seed * 10000 + 9999, opt_val=opt_val, sim=sim
    )
    depth, cx_count = circuit_stats(G, p)

    return {
        "p": p,
        "optimizer": optimizer.upper(),
        "mode": mode,
        "opt_val": float(opt_val),
        "expected_cut": float(final_cut),
        "approx_ratio": float(final_cut / opt_val),
        "opt_prob": float(opt_prob),
        "evals": int(n_evals),
        "runtime_s": float(elapsed),
        "depth": int(depth),
        "cx_count": int(cx_count),
        "gammas": [float(g) for g in gammas],
        "betas": [float(b) for b in betas],
    }


if __name__ == "__main__":
    import networkx as nx
    C4 = nx.cycle_graph(4)
    val, prob = evaluate_cut(C4, [2.3561945], [2.7488936], mode="statevector", opt_val=4)
    print(f"C4 p=1 check: <cut>={val:.3f}, alpha={val/4:.3f}, P(opt)={prob:.3f}")
    assert abs(val - 3.0) < 1e-3

    nm = make_noise_model(p1=0.001, p2=0.01, p_ro=0.02)
    noisy_val, noisy_prob = evaluate_cut(
        C4, [2.3561945], [2.7488936], mode="noisy", shots=2048, noise_model=nm, seed=42, opt_val=4
    )
    depth, cx = circuit_stats(C4, 1)
    print(f"C4 p=1 noisy: <cut>={noisy_val:.3f}, alpha={noisy_val/4:.3f}, P(opt)={noisy_prob:.3f}, depth={depth}, cx={cx}")
    assert noisy_val < val
    print("qaoa self-check passed")
