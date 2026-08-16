#!/usr/bin/env python3
"""
Section 5: baseline reference check.

Reads the already-saved raw baseline output and the task's boxed reference
values, computes Delta_X and delta_X (relative), and separately verifies
that the installed package's own documented worked example (reproduced in
runs/deterministic/documented_reference/) explains the reference values'
provenance. Writes results/reference_comparison.csv.

This script performs no new PRIMAT execution; it only reads files already
written by scripts/run_phase4b.py.
"""
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Task's boxed reference values (treated only as a comparison target, never
# forced).
TASK_REFERENCE = {
    "Neff": 3.04397730,
    "YPBBN": 0.24699808,
    "DoH": 2.4365389e-05,
}


def load(path):
    with open(path) as f:
        return json.load(f)


def main():
    baseline = load(os.path.join(ROOT, "runs/deterministic/baseline/raw_output.json"))
    doc_ref = load(os.path.join(ROOT, "runs/deterministic/documented_reference/raw_output.json"))

    out_csv = os.path.join(ROOT, "results/reference_comparison.csv")
    with open(out_csv, "w") as f:
        f.write("comparison,observable,X_run,X_reference,Delta_X,delta_X_relative\n")

        # (A) task-mandated baseline (Omegabh2=0.022425, network=small,
        # PRIMATConfig defaults) vs the task's boxed reference numbers.
        for k in TASK_REFERENCE:
            x_run = baseline[k]
            x_ref = TASK_REFERENCE[k]
            delta = x_run - x_ref
            rel = abs(delta) / abs(x_ref)
            f.write(f"baseline_vs_task_reference,{k},{x_run!r},{x_ref!r},"
                    f"{delta!r},{rel!r}\n")

        # (B) documented worked example (Omegabh2=0.02242, network=large,
        # amax=8, exactly as printed in the installed README) vs the same
        # boxed reference numbers -- this is the root-cause check: if (B)
        # agrees far more closely than (A), the difference in (A) is
        # explained by network/parameter choice, not a software defect.
        doc_ref_map = {"Neff": doc_ref["Neff"], "YPBBN": doc_ref["YPBBN"], "DoH": doc_ref["DoH"]}
        for k in TASK_REFERENCE:
            x_run = doc_ref_map[k]
            x_ref = TASK_REFERENCE[k]
            delta = x_run - x_ref
            rel = abs(delta) / abs(x_ref)
            f.write(f"documented_example_vs_task_reference,{k},{x_run!r},{x_ref!r},"
                    f"{delta!r},{rel!r}\n")

    print(f"wrote {out_csv}")
    print()
    print("baseline (network=small, Omegabh2=0.022425) vs boxed reference:")
    for k in TASK_REFERENCE:
        d = baseline[k] - TASK_REFERENCE[k]
        print(f"  {k}: Delta={d:.6e}  rel={abs(d)/abs(TASK_REFERENCE[k]):.6e}")
    print()
    print("documented example (network=large,amax=8, Omegabh2=0.02242) vs boxed reference:")
    for k in TASK_REFERENCE:
        d = doc_ref_map[k] - TASK_REFERENCE[k]
        print(f"  {k}: Delta={d:.6e}  rel={abs(d)/abs(TASK_REFERENCE[k]):.6e}")


if __name__ == "__main__":
    main()
