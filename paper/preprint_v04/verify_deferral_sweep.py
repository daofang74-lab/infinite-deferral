"""Check the finite Bellman calculation by independent path enumeration."""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

from run_deferral_sweep import GROWTH, DISCOUNT, CONTINUATION, solve


def enumerate_paths(rho, beta, horizon, opened):
    best = None
    first = set()
    examined = 0
    for path in product(range(5), repeat=horizon):
        capability = 0
        weight = F(1)
        total = F(0)
        for allocation in path:
            frontier = rho**capability if opened else F(1)
            total += weight * F(allocation, 4) * frontier
            capability += 4 - allocation
            weight *= beta
        examined += 1
        if best is None or total > best:
            best = total
            first = {path[0]}
        elif total == best:
            first.add(path[0])
    return best, sorted(first), examined


def main():
    cases = 0
    paths = 0
    for rho in GROWTH:
        for gamma in DISCOUNT:
            for p in CONTINUATION:
                for h in (1, 2, 4):
                    for opened in (False, True):
                        forward_value, forward_first, count = enumerate_paths(
                            rho, gamma * p, h, opened
                        )
                        value, _, first = solve(rho, gamma, p, h, opened)
                        assert forward_value == value
                        assert forward_first == first
                        cases += 1
                        paths += count
    result = {
        "method": "exact enumeration of realized action paths independent of the Bellman recursion",
        "horizons": [1, 2, 4],
        "checked_cases": cases,
        "enumerated_action_paths": paths,
        "value_mismatches": 0,
        "first_choice_mismatches": 0,
    }
    out = Path(__file__).resolve().parent / "experiments/independent_check.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
