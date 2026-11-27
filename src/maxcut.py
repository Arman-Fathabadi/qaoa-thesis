"""Max-Cut solvers: exact brute force, random search, and greedy local search."""
import itertools
import random

import networkx as nx


def cut_value(G, assignment):
    """Total weight of edges whose endpoints are on different sides.

    `assignment` maps node -> 0/1. Edges without a 'weight' attribute count as 1.
    """
    return sum(d.get("weight", 1) for u, v, d in G.edges(data=True)
               if assignment[u] != assignment[v])


def brute_force(G):
    """Exact solver: try all 2^(n-1) assignments (first node fixed to 0 by symmetry).

    Returns (best_value, best_assignment).
    """
    nodes = list(G.nodes)
    if not nodes:
        return 0, {}
    best_val, best = -1, None
    for bits in itertools.product([0, 1], repeat=len(nodes) - 1):
        assignment = dict(zip(nodes, (0,) + bits))
        val = cut_value(G, assignment)
        if val > best_val:
            best_val, best = val, assignment
    return best_val, best


def random_search(G, n_samples=1000, seed=None):
    """Baseline: sample random assignments and keep the best one."""
    rng = random.Random(seed)
    nodes = list(G.nodes)
    best_val, best = -1, None
    for _ in range(n_samples):
        assignment = {n: rng.randint(0, 1) for n in nodes}
        val = cut_value(G, assignment)
        if val > best_val:
            best_val, best = val, assignment
    return best_val, best


def greedy_local_search(G, restarts=10, seed=None):
    """Baseline: from a random start, flip any node that improves the cut until no flip helps.

    Repeats from several random starts and returns the best local optimum.
    """
    rng = random.Random(seed)
    nodes = list(G.nodes)
    best_val, best = -1, None
    for _ in range(restarts):
        assignment = {n: rng.randint(0, 1) for n in nodes}
        improved = True
        while improved:
            improved = False
            for n in nodes:
                # Flipping n gains the weight of its same-side edges and loses its cut edges
                gain = sum(G[n][m].get("weight", 1) * (1 if assignment[m] == assignment[n] else -1)
                           for m in G.neighbors(n) if m != n)
                if gain > 0:
                    assignment[n] ^= 1
                    improved = True
        val = cut_value(G, assignment)
        if val > best_val:
            best_val, best = val, assignment
    return best_val, best


def benchmark_graphs():
    """Standard small-scale unweighted Max-Cut benchmark graphs (n = 4, 6, 8)."""
    return {
        "C4": nx.cycle_graph(4),
        "G(6,0.6)": nx.gnp_random_graph(6, 0.6, seed=42),
        "C8": nx.cycle_graph(8),
        "G(8,0.5)": nx.gnp_random_graph(8, 0.5, seed=7),
    }


if __name__ == "__main__":
    # Test 1: 4-node cycle, optimum is 4 (alternate sides)
    C4 = nx.cycle_graph(4)
    assert brute_force(C4)[0] == 4
    assert random_search(C4, 200, seed=0)[0] == 4
    assert greedy_local_search(C4, 10, seed=0)[0] >= 2  # local optimum can be stuck at 2... or 4
    print("C4  exact/random/greedy:", brute_force(C4)[0],
          random_search(C4, 200, seed=0)[0], greedy_local_search(C4, 10, seed=0)[0])

    # Test 2: random 6-node graph; baselines can never beat the exact optimum
    G = nx.gnp_random_graph(6, 0.6, seed=42)
    opt = brute_force(G)[0]
    rs = random_search(G, 500, seed=1)[0]
    gr = greedy_local_search(G, 10, seed=1)[0]
    assert rs <= opt and gr <= opt
    assert rs == opt  # 64 states, 500 samples: all but certain to hit the optimum
    assert gr >= opt / 2  # local optima are always at least half the edges' worth
    print(f"G(6,0.6) edges={G.number_of_edges()}  exact/random/greedy:", opt, rs, gr)

    # Test 3: 8-node benchmarks (C8 and seeded random graph)
    for name in ("C8", "G(8,0.5)"):
        H = benchmark_graphs()[name]
        opt_h = brute_force(H)[0]
        rs_h = random_search(H, 1000, seed=1)[0]
        gr_h = greedy_local_search(H, 10, seed=1)[0]
        assert rs_h <= opt_h and gr_h <= opt_h
        assert gr_h >= opt_h / 2
        print(f"{name} edges={H.number_of_edges()}  exact/random/greedy:", opt_h, rs_h, gr_h)

    print("all maxcut tests passed")
