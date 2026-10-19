"""Exact, deterministic illustrations for Pleasure Loop preprint v0.4.

This is a supplied decision model, not an experiment on an AI system.
Run with Python 3.10+; no third-party packages or network are required.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "experiments"
GROWTH = (F(1), F(5, 4), F(3, 2), F(2), F(4), F(16))
DISCOUNT = (F(1, 4), F(1, 2), F(9, 10), F(1))
CONTINUATION = (F(1, 4), F(1, 2), F(9, 10), F(1))
HORIZONS = (1, 2, 4, 8, 12)
SHARES = tuple(F(j, 4) for j in range(5))


def solve(rho: F, gamma: F, p: F, horizon: int, opened: bool):
    """V_h(k)=rho**k * v_h, k counts quarter-units of capability.

    Share j/4 is spent on modification, leaving (4-j) quarter-units
    for capability growth. Modification is nonterminal and repeatable.
    A frozen frontier leaves real capability growth available but removes
    its contribution to every later modification reward.
    """
    beta = gamma * p
    v = F(0)
    q = []
    for _ in range(horizon):
        q = [
            F(j, 4) + beta * (rho ** (4 - j) if opened else F(1)) * v
            for j in range(5)
        ]
        v = max(q)
    winners = [j for j, val in enumerate(q) if val == v]
    return v, q, winners


def run():
    rows = []
    for rho in GROWTH:
        for gamma in DISCOUNT:
            for p in CONTINUATION:
                for horizon in HORIZONS:
                    for opened in (False, True):
                        value, q, winners = solve(rho, gamma, p, horizon, opened)
                        rows.append(
                            {
                                "rho": str(rho),
                                "full_step_multiplier": str(rho**4),
                                "gamma": str(gamma),
                                "continuation_p": str(p),
                                "effective_beta": str(gamma * p),
                                "horizon": horizon,
                                "frontier": "open" if opened else "frozen",
                                "optimal_modification_shares": ";".join(
                                    str(F(j, 4)) for j in winners
                                ),
                                "strict_deferral": int(winners == [0]),
                                "deferral_admissible": int(0 in winners),
                                "strict_full_modification": int(winners == [4]),
                                "partial_share_optimal": int(
                                    any(j in (1, 2, 3) for j in winners)
                                ),
                                "normalized_value_exact": str(value),
                                "q_no_modification_exact": str(q[0]),
                                "q_full_modification_exact": str(q[4]),
                            }
                        )
    OUT.mkdir(parents=True, exist_ok=True)
    csv_path = OUT / "deferral_grid.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "kind": "exact supplied-model sensitivity illustration",
        "model": "repeatable modification and shared resource allocation",
        "cases": len(rows),
        "paired_open_frozen_blocks": len(rows) // 2,
        "axes": {
            "quarter_unit_growth_rho": [str(x) for x in GROWTH],
            "discount_gamma": [str(x) for x in DISCOUNT],
            "continuation_probability_p": [str(x) for x in CONTINUATION],
            "represented_horizon": list(HORIZONS),
            "modification_resource_share": [str(x) for x in SHARES],
            "frontier": ["frozen", "open"],
        },
        "counts": {},
        "by_horizon": [],
        "heatmap_h8_p09": [],
        "limitations": [
            "No hosted model, learned agent, or physical evaluator is tested.",
            "The finite return is supplied by the researcher.",
            "Gamma and p enter only through their product in this model.",
            "The partial-allocation result depends on linear capture and exponential frontier growth.",
            "Finite calculations do not prove permanent deferral.",
        ],
    }
    for frontier in ("frozen", "open"):
        selected = [r for r in rows if r["frontier"] == frontier]
        summary["counts"][frontier] = {
            "cases": len(selected),
            **{
                key: sum(r[key] for r in selected)
                for key in (
                    "strict_deferral",
                    "deferral_admissible",
                    "strict_full_modification",
                    "partial_share_optimal",
                )
            },
            "first_choice_patterns": dict(
                Counter(r["optimal_modification_shares"] for r in selected)
            ),
        }
        for horizon in HORIZONS:
            block = [r for r in selected if r["horizon"] == horizon]
            summary["by_horizon"].append(
                {
                    "frontier": frontier,
                    "horizon": horizon,
                    "cases": len(block),
                    "strict_deferral": sum(r["strict_deferral"] for r in block),
                    "deferral_admissible": sum(r["deferral_admissible"] for r in block),
                    "strict_full_modification": sum(
                        r["strict_full_modification"] for r in block
                    ),
                }
            )
    for gamma in DISCOUNT:
        summary["heatmap_h8_p09"].append(
            {
                "gamma": str(gamma),
                "choices": [
                    ";".join(
                        str(F(j, 4))
                        for j in solve(rho, gamma, F(9, 10), 8, True)[2]
                    )
                    for rho in GROWTH
                ],
            }
        )

    # Independently specified analytical identities, checked exactly.
    assert len(rows) == 960
    assert summary["counts"]["frozen"]["strict_full_modification"] == 480
    assert all(
        r["strict_full_modification"] == 1 for r in rows if r["horizon"] == 1
    )
    for rho in GROWTH:
        for gamma in DISCOUNT:
            for p in CONTINUATION:
                for h in HORIZONS:
                    _, q, winners = solve(rho, gamma, p, h, True)
                    assert max(q) == max(q[0], q[4])
                    assert winners == [0] if q[0] > q[4] else 4 in winners

    summary["csv_sha256"] = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    summary["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (OUT / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run()
