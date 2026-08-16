# Phase 4B — PRIMAT Reproducibility, Convergence, and BBN Covariance Audit

Strictly standard-physics numerical experiment on the homogeneous early
universe (standard Big Bang nucleosynthesis), executed with the public
PRIMAT 0.3.1 BBN solver. This directory is the authoritative,
machine-generated record of that experiment: **the raw files here, plus
the associated Git commit, are the record — prose in the audit report is
only a summary of them.**

See `protocol/phase4b_spec.md` for the full protocol and the governing-rule
interface inspection that preceded any scientific run, and
`audit/PHASE4B_FINAL_REPORT.md` for the final report, including the
`BBN_BASELINE_STATUS` gate result.

## Layout

```
phase4b-primat/
├── README.md                    this file
├── protocol/phase4b_spec.md     protocol + interface-inspection findings
├── environment/                 environment.txt, pip_freeze.txt
├── configs/                     machine-readable run configurations (YAML)
├── scripts/                     execution + independent audit scripts
├── runs/                        per-run raw stdout/stderr/config/output
│   ├── smoke_test/              pre-protocol capability check (preserved separately)
│   ├── deterministic/           baseline, documented_reference, high_precision
│   ├── backend/                 c/ vs python/ backend comparison
│   ├── tolerance/                numerical_precision sweep
│   ├── weak_rate/                sampling_nTOp_per_decade sweep
│   └── monte_carlo/              run1/, run2/ (fixed-seed reproducibility pair)
├── raw/                          raw MC sample tables (full precision, unrounded)
├── results/                      derived CSV/JSON summaries (comparisons, covariance)
├── audit/                        PHASE4B_FINAL_REPORT.md + independent audit script output
└── provenance/                   input->config->software->execution->output->statistic chain + checksums
```

## Reproducing this audit

```bash
python3 -m venv venv && source venv/bin/activate
pip install primat==0.3.1
python3 scripts/run_phase4b.py      # executes all deterministic/backend/tolerance/weak-rate/high-precision/MC runs
python3 scripts/audit.py            # independently recomputes all statistics from the saved raw files
```
