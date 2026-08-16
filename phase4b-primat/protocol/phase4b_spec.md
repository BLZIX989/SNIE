# Phase 4B — PRIMAT Reproducibility, Convergence, and BBN Covariance Audit

## Scope

Strictly standard-physics numerical experiment on the homogeneous early
universe, executed with the public PRIMAT 0.3.1 Big Bang Nucleosynthesis
(BBN) solver (https://pypi.org/project/primat/). This experiment closes the
BBN baseline validation gate only. No counterfactual experiments, no
modification of ΩΛ/Ωc/Ωb/A_s/n_s, no recombination-era physics. See
`audit/PHASE4B_FINAL_REPORT.md` §18 for the explicit statement that no
counterfactual runs (R-001..R-005) were executed.

## Governing rule: verified interface before execution

Before any scientific run, the installed interface was inspected directly
(`primat --version`, `primat --help`, `python -c "import primat; print(primat.__file__)"`,
`pip show primat`, and the installed package source under
`<venv>/lib/python3.11/site-packages/primat/`). No previously suggested
command-line flag was assumed valid without confirming it in this `--help`
output. Findings for the 13 governing-rule checklist items:

1. **Exact PRIMAT version**: 0.3.1 (`primat --version` → `primat 0.3.1`;
   `pip show primat` → `Version: 0.3.1`).
2. **Python version**: 3.11.15.
3. **Operating system**: Linux (kernel 6.18.5-fc-v20), x86_64.
4. **Architecture**: x86_64.
5. **C compiler/backend availability**: A precompiled C extension
   (`primat._primat_c`, a `.so` built for `cp311-manylinux`) ships inside the
   wheel; `primat.backend.HAS_C_BACKEND == True`. No local compilation was
   needed or performed for this backend.
6. **Python backend availability**: Always available (`primat.main.PRIMAT`,
   pure-Python fallback); confirmed by successfully forcing
   `force_backend="python"` in `run_bbn`.
7. **Deterministic BBN execution interface**: CLI `primat [flags]`, and the
   documented (README, "Python API (recommended)") `primat.backend.run_bbn(params, force_backend=...)`.
8. **Monte Carlo interface**: CLI `--mc N [--mc-seed SEED] [--mc-jobs N]`,
   and `primat.backend.run_mc(...)` / `primat.main.mc_uncertainty(...)`.
9. **Numerical precision control**: `--numerical_precision RTOL`
   (PRIMATConfig key `numerical_precision`, default `1e-7`; `solve_ivp` rtol).
10. **n↔p weak-rate resolution control**: not exposed as a dedicated CLI
    flag, but present as a `PRIMATConfig` key `sampling_nTOp_per_decade`
    (default `80`), settable via the CLI's generic
    `--set sampling_nTOp_per_decade=VALUE` escape hatch, or directly as a
    `params` dict key through the Python API.
11. **Random-seed control**: `--mc-seed SEED` (CLI, default 0) /
    `seed=` (Python `mc_uncertainty`/`run_mc`); sample *i* uses `seed + i`.
12. **Raw Monte Carlo output capability**: `--output_mc_samples
    --output_mc_file FILE` (CLI; TSV via `primat.backend.dump_mc_samples`),
    and the Python `MCResult.samples_array()` / `MCResult[quantity].values`
    (full per-sample arrays, not just mean/std).
13. **Time-evolution output capability**: `--output_time_evolution
    --output_file FILE` (CLI; full ODE-solution time series), supported by
    both backends.

No requested governing-rule capability was found to be missing in the
installed 0.3.1 interface.

## Key interface facts discovered during inspection (used throughout this audit)

- **Documented reference-value provenance mismatch.** The task's boxed
  reference values (`Neff=3.04397730`, `YP(BBN)=0.24699808`,
  `D/H=2.4365389e-5`) are *not* produced by `PRIMATConfig` defaults. They are
  reproduced verbatim by the installed package's own bundled documentation
  (`primat-0.3.1.dist-info/METADATA`, i.e. the shipped README) under the
  worked CLI example:
  `primat --Omegabh2 0.02242 --network large --amax 8`
  — note `Omegabh2=0.02242` (5 significant figures, not `0.022425`) and
  `network=large, amax=8` (not the CLI/library default `network=small`).
  This is documented and reproduced explicitly in
  `runs/deterministic/documented_reference/` and analyzed in
  `results/reference_comparison.csv` / the final report §5. It is **not**
  treated as a discrepancy requiring investigation for a bug — the root
  cause is a network/parameter difference, identified directly from the
  installed documentation, not assumed.
- **Documented C/Python backend gap.** The installed package's own test
  suite (`tests/test_backend_parity.py`, fetched from the matching `v0.3.1`
  git tag for documentation purposes only) documents a known, accepted
  discrepancy for `network="small"` at default settings: C vs. Python agree
  on `YPBBN` to `abs≈1e-5`, `Neff` to `abs≈1e-3`, but differ in `D/H` by
  `≈1.7e-8` absolute (`≈7e-4` relative) — "outside CLAUDE.md's stated
  ±3e-9 D/H regression tolerance for the Python backend's own reference
  values" but budgeted at `rel=1e-3` for cross-backend comparison
  specifically because the gap is not yet root-caused upstream. This
  pre-existing, documented tolerance is used in §6 of the final report to
  distinguish an *observed execution difference* from a *documented
  software expectation*.
- **Documented high-precision reference configuration.** The installed
  wheel does **not** ship `runfiles/primat_reference_run.py` (confirmed:
  zero occurrences of `runfiles` in `primat-0.3.1.dist-info/RECORD`); the
  README only names it as a "development/source-only" example script. Per
  the explicit instruction not to reconstruct such a configuration from
  memory, its exact settings were retrieved from the matching tagged
  release `v0.3.1` of the upstream source repository (not from model
  memory, not a different/untagged commit) and are reproduced as documented
  in `runs/deterministic/high_precision/`.

## Absolute counterfactual lock

Per the task's explicit instruction, this protocol does **not** execute any
of R-001..R-005, does not vary ΩΛ, Ωc, Ωb, A_s, or n_s, does not alter
physical laws, and does not proceed to recombination-era physics. Only
`Omegabh2` (fixed at 0.022425) and `DeltaNeff` (fixed at 0) are the
cosmological inputs used, exactly as specified, across every run in this
audit.
