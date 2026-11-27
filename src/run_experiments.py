"""Run reproducible classical, QAOA depth, noise sweep, and optimizer benchmarks.

Saves CSV tables and plots to results/.
"""
import csv
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.maxcut import benchmark_graphs, brute_force, greedy_local_search, random_search
from src.qaoa import circuit_stats, evaluate_cut, make_noise_model, optimize_qaoa

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def write_csv(filename, fieldnames, rows):
    path = RESULTS_DIR / filename
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Saved {path} ({len(rows)} rows)")


def run_classical_benchmarks(graphs):
    rows = []
    for name, G in graphs.items():
        t0 = time.perf_counter()
        opt, _ = brute_force(G)
        t_bf = (time.perf_counter() - t0) * 1000

        n_samples = 200 if G.number_of_nodes() == 4 else (500 if G.number_of_nodes() == 6 else 1000)
        t0 = time.perf_counter()
        rs, _ = random_search(G, n_samples=n_samples, seed=1)
        t_rs = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        gr, _ = greedy_local_search(G, restarts=10, seed=1)
        t_gr = (time.perf_counter() - t0) * 1000

        rows.append({
            "graph": name,
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "exact_opt": opt,
            "random_cut": rs,
            "random_samples": n_samples,
            "greedy_cut": gr,
            "exact_ms": round(t_bf, 3),
            "random_ms": round(t_rs, 3),
            "greedy_ms": round(t_gr, 3),
        })
    write_csv(
        "classical_baselines.csv",
        ["graph", "nodes", "edges", "exact_opt", "random_cut", "random_samples",
         "greedy_cut", "exact_ms", "random_ms", "greedy_ms"],
        rows,
    )
    return {r["graph"]: r["exact_opt"] for r in rows}


def run_depth_and_noise_comparison(graphs, exact_opts):
    """Compare ideal statevector, finite-shot noiseless, and noisy QAOA across graphs and depths."""
    nm = make_noise_model(p1=0.001, p2=0.01, p_ro=0.02)
    seeds = [0, 1, 2]
    rows = []
    best_ideal_params = {}  # (graph_name, p) -> (gammas, betas)

    for name, G in graphs.items():
        opt = exact_opts[name]
        depths = [1, 2, 3] if G.number_of_nodes() <= 6 else [1, 2]
        for p in depths:
            # Find strong ideal angles across seeds first (statevector)
            ideal_runs = [
                optimize_qaoa(G, p=p, optimizer="COBYLA", mode="statevector", maxiter=90, seed=s, opt_val=opt)
                for s in seeds
            ]
            best_run = max(ideal_runs, key=lambda r: r["expected_cut"])
            best_ideal_params[(name, p)] = (best_run["gammas"], best_run["betas"])

            # Evaluate finite-shot noiseless and noisy performance at optimized parameters
            shot_runs = []
            noisy_runs = []
            for s in seeds:
                r_shots = optimize_qaoa(
                    G, p=p, optimizer="COBYLA", mode="shots", shots=2048,
                    maxiter=50, seed=s, opt_val=opt
                )
                r_noisy = optimize_qaoa(
                    G, p=p, optimizer="COBYLA", mode="noisy", shots=2048,
                    noise_model=nm, maxiter=50, seed=s, opt_val=opt
                )
                shot_runs.append(r_shots)
                noisy_runs.append(r_noisy)

            for mode, runs in [("statevector", ideal_runs), ("shots_2048", shot_runs), ("noisy_aer", noisy_runs)]:
                alphas = [r["approx_ratio"] for r in runs]
                cuts = [r["expected_cut"] for r in runs]
                probs = [r["opt_prob"] for r in runs]
                times = [r["runtime_s"] for r in runs]
                rows.append({
                    "graph": name,
                    "nodes": G.number_of_nodes(),
                    "edges": G.number_of_edges(),
                    "p": p,
                    "mode": mode,
                    "exact_opt": opt,
                    "mean_cut": round(float(np.mean(cuts)), 4),
                    "mean_alpha": round(float(np.mean(alphas)), 4),
                    "std_alpha": round(float(np.std(alphas)), 4),
                    "max_alpha": round(float(np.max(alphas)), 4),
                    "mean_opt_prob": round(float(np.mean(probs)), 4),
                    "depth": runs[0]["depth"],
                    "cx_count": runs[0]["cx_count"],
                    "mean_runtime_s": round(float(np.mean(times)), 3),
                })

    write_csv(
        "qaoa_ideal_vs_noisy.csv",
        ["graph", "nodes", "edges", "p", "mode", "exact_opt", "mean_cut",
         "mean_alpha", "std_alpha", "max_alpha", "mean_opt_prob", "depth", "cx_count", "mean_runtime_s"],
        rows,
    )
    return rows, best_ideal_params


def run_noise_sweep(graphs, exact_opts, best_ideal_params):
    """Sweep 2-qubit depolarizing error p2 on G(6,0.6) and G(8,0.5) to test depth vs. noise tradeoff."""
    p2_values = [0.0, 0.005, 0.01, 0.02, 0.04, 0.06, 0.10]
    sweep_targets = [("G(6,0.6)", [1, 2, 3]), ("G(8,0.5)", [1, 2])]
    rows = []

    for name, depths in sweep_targets:
        G = graphs[name]
        opt = exact_opts[name]
        for p in depths:
            gammas, betas = best_ideal_params[(name, p)]
            depth, cx_count = circuit_stats(G, p)
            for p2 in p2_values:
                p1 = p2 / 10.0
                p_ro = 0.0 if p2 == 0.0 else 0.02
                nm = make_noise_model(p1=p1, p2=p2, p_ro=p_ro) if p2 > 0 else None
                mode = "noisy" if p2 > 0 else "shots"
                alphas = []
                probs = []
                for s in (10, 11, 12):
                    cut, prob = evaluate_cut(
                        G, gammas, betas, mode=mode, shots=2048,
                        noise_model=nm, seed=s, opt_val=opt
                    )
                    alphas.append(cut / opt)
                    probs.append(prob)
                rows.append({
                    "graph": name,
                    "p": p,
                    "p1": round(p1, 5),
                    "p2": p2,
                    "p_ro": p_ro,
                    "depth": depth,
                    "cx_count": cx_count,
                    "mean_alpha": round(float(np.mean(alphas)), 4),
                    "std_alpha": round(float(np.std(alphas)), 4),
                    "mean_opt_prob": round(float(np.mean(probs)), 4),
                })

    write_csv(
        "qaoa_noise_sweep.csv",
        ["graph", "p", "p1", "p2", "p_ro", "depth", "cx_count", "mean_alpha", "std_alpha", "mean_opt_prob"],
        rows,
    )
    return rows


def run_optimizer_comparison(graphs, exact_opts):
    """Compare COBYLA vs SPSA on G(6,0.6) (p=1, 2) under statevector, finite shots, and noise."""
    G = graphs["G(6,0.6)"]
    opt = exact_opts["G(6,0.6)"]
    nm = make_noise_model(p1=0.001, p2=0.01, p_ro=0.02)
    seeds = [0, 1, 2]
    rows = []

    for p in (1, 2):
        for mode in ("statevector", "shots", "noisy"):
            for opt_name, maxiter in [("COBYLA", 60), ("SPSA", 30)]:
                runs = [
                    optimize_qaoa(
                        G, p=p, optimizer=opt_name, mode=mode, shots=1024,
                        noise_model=(nm if mode == "noisy" else None),
                        maxiter=maxiter, seed=s, opt_val=opt
                    )
                    for s in seeds
                ]
                alphas = [r["approx_ratio"] for r in runs]
                evals = [r["evals"] for r in runs]
                times = [r["runtime_s"] for r in runs]
                rows.append({
                    "graph": "G(6,0.6)",
                    "p": p,
                    "mode": mode,
                    "optimizer": opt_name,
                    "mean_alpha": round(float(np.mean(alphas)), 4),
                    "std_alpha": round(float(np.std(alphas)), 4),
                    "mean_evals": round(float(np.mean(evals)), 1),
                    "mean_runtime_s": round(float(np.mean(times)), 3),
                })

    write_csv(
        "optimizer_comparison.csv",
        ["graph", "p", "mode", "optimizer", "mean_alpha", "std_alpha", "mean_evals", "mean_runtime_s"],
        rows,
    )
    return rows


def plot_depth_and_noise(rows):
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), sharey=True)
    graph_order = ["C4", "G(6,0.6)", "C8", "G(8,0.5)"]
    modes = [("statevector", "Ideal (statevector)", "#1a73e8"),
             ("shots_2048", "Noiseless (2048 shots)", "#34a853"),
             ("noisy_aer", "Noisy Aer (p2=1%, ro=2%)", "#ea4335")]

    x = np.arange(len(graph_order))
    width = 0.25

    for ax, p in zip(axes, [1, 2]):
        for k, (mode, label, color) in enumerate(modes):
            vals = []
            errs = []
            for g in graph_order:
                match = [r for r in rows if r["graph"] == g and r["p"] == p and r["mode"] == mode][0]
                vals.append(match["mean_alpha"])
                errs.append(match["std_alpha"])
            ax.bar(x + (k - 1) * width, vals, width, yerr=errs, capsize=3, label=label, color=color, alpha=0.9)
        ax.set_title(f"QAOA Depth p = {p} (COBYLA, 3 seeds)")
        ax.set_xticks(x)
        ax.set_xticklabels(graph_order)
        ax.set_ylim(0.5, 1.02)
        ax.grid(axis="y", alpha=0.3)

    axes[0].set_ylabel("Approximation ratio  α = <C> / C*")
    axes[0].legend(fontsize=8.5, loc="lower right")
    fig.tight_layout()
    out = RESULTS_DIR / "fig_depth_noise_comparison.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    print(f"Saved {out}")


def plot_noise_sweep(rows):
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), sharey=True)
    colors = {1: "#1a73e8", 2: "#e37400", 3: "#d93025"}

    for ax, graph_name in zip(axes, ["G(6,0.6)", "G(8,0.5)"]):
        depths = sorted({r["p"] for r in rows if r["graph"] == graph_name})
        for p in depths:
            sub = [r for r in rows if r["graph"] == graph_name and r["p"] == p]
            ps = [r["p2"] for r in sub]
            ys = [r["mean_alpha"] for r in sub]
            es = [r["std_alpha"] for r in sub]
            cx = sub[0]["cx_count"]
            ax.errorbar(ps, ys, yerr=es, marker="o", capsize=3, linewidth=1.8,
                        color=colors[p], label=f"p={p} ({cx} CNOTs)")
        ax.set_title(f"Noise Degradation on {graph_name}")
        ax.set_xlabel("2-qubit depolarizing error rate (p2)")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8.5)

    axes[0].set_ylabel("Approximation ratio  α = <C> / C*")
    axes[0].set_ylim(0.5, 0.96)
    fig.tight_layout()
    out = RESULTS_DIR / "fig_qaoa_noise_sweep.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    print(f"Saved {out}")


def plot_optimizer_comparison(rows):
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.0), sharey=True)
    mode_order = ["statevector", "shots", "noisy"]
    mode_labels = ["Ideal\n(statevector)", "Finite shots\n(1024)", "Noisy Aer\n(p2=1%, ro=2%)"]
    x = np.arange(len(mode_order))
    width = 0.34

    for ax, p in zip(axes, [1, 2]):
        for k, (opt_name, color) in enumerate([("COBYLA", "#1a73e8"), ("SPSA", "#34a853")]):
            vals = [next(r["mean_alpha"] for r in rows if r["p"] == p and r["mode"] == m and r["optimizer"] == opt_name) for m in mode_order]
            errs = [next(r["std_alpha"] for r in rows if r["p"] == p and r["mode"] == m and r["optimizer"] == opt_name) for m in mode_order]
            ax.bar(x + (k - 0.5) * width, vals, width, yerr=errs, capsize=3, label=opt_name, color=color, alpha=0.9)
        ax.set_title(f"G(6,0.6) Optimizer Comparison (p = {p})")
        ax.set_xticks(x)
        ax.set_xticklabels(mode_labels)
        ax.set_ylim(0.5, 0.95)
        ax.grid(axis="y", alpha=0.3)

    axes[0].set_ylabel("Approximation ratio  α = <C> / C*")
    axes[0].legend(fontsize=9)
    fig.tight_layout()
    out = RESULTS_DIR / "fig_optimizer_comparison.png"
    fig.savefig(out, dpi=180)
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    graphs = benchmark_graphs()
    exact_opts = run_classical_benchmarks(graphs)
    depth_rows, best_ideal_params = run_depth_and_noise_comparison(graphs, exact_opts)
    sweep_rows = run_noise_sweep(graphs, exact_opts, best_ideal_params)
    opt_rows = run_optimizer_comparison(graphs, exact_opts)

    plot_depth_and_noise(depth_rows)
    plot_noise_sweep(sweep_rows)
    plot_optimizer_comparison(opt_rows)
    print("All QAOA and noise experiments completed.")
