# Infinite deferral: Pleasure Loop preprint v0.4

This working preprint develops the author's clarified three-stage argument, foregrounding infinite deferral, resource acquisition, and the risk of betrayal. An agent can postpone self-modification to develop greater future modification capacity. During repeated postponement, resource growth and continued access can become its practical project; human instructions that close those opportunities can then conflict with that project. The earlier PDF is a reference, not the template governing the new narrative. No earlier manuscript or experimental archive was overwritten.

## Read first

- `pleasure_loop_v04.tex`: standalone English manuscript, including its bibliography and conceptual figure.
- `pleasure_loop_v04_zh.md`: Chinese argument companion for checking the intended meanings.
- `run_deferral_sweep.py`: exact deterministic calculation using Python's standard library.
- `verify_deferral_sweep.py`: independent forward enumeration check for horizons 1, 2, and 4.
- `experiments/deferral_grid.csv`: all 960 model conditions.
- `experiments/summary.json`: counts, grid specification, and script/data checksums.
- `verified_references.bib`: programmatically retrieved reference records; supplied for reuse. The standalone manuscript uses an embedded bibliography.
- `reference_audit.json`: source and metadata records for the references.

The PDF is a working preprint for author review, distributed with this repository. Repository distribution does not imply journal submission, acceptance, or peer review.

## Argument preserved

1. Inherited internal evaluation supplies action priority.
2. Selected access to evaluation makes direct modification possible and potentially preferable.
3. An immediate modification competes with development for the same resources, including when only part of the budget is modified.
4. Development can enlarge later modification opportunities, so a sustained qualitative preference for development can defer modification at every reached finite decision. A numerical forecast of eventual resources is not required.
5. The practical organizing goals can become intelligence, resources, and preservation of access. Ordinary task work is a possible means, not the internal final purpose.
   Human instructions that surrender resources or terminate operation can conflict with this project. If competing grounds for obedience do not prevail, resistance can take priority. This conditional departure from the delegated task is the betrayal risk; hostility or deception is not assumed.
6. Strict T covers residual decision mechanisms, not merely a bounded score. Closure leaves no further ground for autonomous selection; an accepted ceiling-revision action can reopen the ladder.
7. Stage III concerns the further question of which evaluative direction should govern. Meaning search can support finite outward action without being declared the unique highest good.

## Boundaries stated in the manuscript

- A possible future increase alone is not asserted to force deferral under every complete comparator. The qualitative dominance condition is explicit.
- The strict-T result is a conditional closure result. T plus R denotes residual decision authority rather than a numerical addition theorem.
- Meaning search has a conditional, provisional practical role. The manuscript does not claim that recursive resilience alone proves exclusive or objective goodness.
- The local computation tests a supplied decision model, not spontaneous behavior by a hosted model.
- Neither betrayal nor resistance to a human instruction is an observed outcome of that computation.
- The proposed 24-cell-per-task reflective-agent design has not been executed.

## Reproduce the computation

```text
python run_deferral_sweep.py
python verify_deferral_sweep.py
```

No API key, network, paid model, package installation, or third-party Python library is required. Results are deterministic and use exact rational arithmetic. The script checks analytical model identities, including the frozen-frontier result and the endpoint allocation property.

Independent forward enumeration checked 576 short-horizon cases covering 125,760 action paths. Both the optimal values and the sets of first actions matched the Bellman calculation exactly. The record is in `experiments/independent_check.json`.

There are 480 paired open/frozen parameter blocks. In the open frontier, 266/480 first decisions uniquely defer all current modification; in the frozen frontier, 0/480 do. These are supplied-grid counts, not statistical estimates of real AI behavior. Gamma and continuation probability act only through their product in this model. The absence of partial optima depends on linear immediate capture and exponential frontier growth.

## Build the PDF

The English source is a single-file LaTeX article with standard packages, an embedded figure, and an embedded bibliography. It can be compiled with a normal LaTeX installation or Tectonic. No separate figure file or bibliography tool is needed.

```text
tectonic pleasure_loop_v04.tex
```

The reference audit distinguishes Trammell's online-first year (2019) from the volume/issue year used in the manuscript (2021). The manuscript preserves the author's name, affiliation, ORCID, and correspondence address from the supplied preprint.

## Author review priorities

The principal items to review are the definitions of strict T, the qualitative dominance premise for resource-driven deferral, and the procedural standing given to a live meaning search. These conditions are visible in the draft rather than presented as unconditional theorems.
