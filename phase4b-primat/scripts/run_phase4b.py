#!/usr/bin/env python3
"""
Phase 4B execution driver.

Runs every deterministic/backend/tolerance/weak-rate/high-precision/Monte
Carlo computation specified by the Phase 4B protocol (protocol/phase4b_spec.md)
against the installed PRIMAT 0.3.1 package, and writes raw, full-precision
output to runs/, raw/, and results/ under the project root. This script
performs no statistical derivation beyond bookkeeping (deltas between two
already-computed observables) -- covariance, correlation, and likelihood
statistics are computed independently by scripts/audit.py, reading only the
files this script writes.

Usage:
    python3 scripts/run_phase4b.py [--skip-mc] [--skip-high-precision]
"""
import argparse
import json
import os
import platform
import subprocess
import sys
import time

import numpy as np

import primat
from primat.backend import run_bbn, run_mc, HAS_C_BACKEND, dump_mc_samples

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

BASELINE_PHYSICAL = {"Omegabh2": 0.022425, "DeltaNeff": 0.0}


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def env_metadata():
    return {
        "primat_version": primat.__version__,
        "python_version": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "has_c_backend": HAS_C_BACKEND,
        "numpy_version": np.__version__,
        "timestamp_utc": _now(),
    }


def save_run(outdir, label, params, force_backend, result, elapsed,
             extra_meta=None, exact_command=None):
    os.makedirs(outdir, exist_ok=True)
    meta = {
        "label": label,
        "params": params,
        "force_backend": force_backend,
        "runtime_seconds": elapsed,
        "exact_python_invocation": (
            f"primat.backend.run_bbn({params!r}, force_backend={force_backend!r})"
        ),
        "exact_cli_equivalent_command": exact_command,
        "environment": env_metadata(),
    }
    if extra_meta:
        meta.update(extra_meta)
    with open(os.path.join(outdir, "config.json"), "w") as f:
        json.dump(meta, f, indent=2, sort_keys=True)
    with open(os.path.join(outdir, "raw_output.json"), "w") as f:
        json.dump(result, f, indent=2, sort_keys=True)
    summary_keys = ["Neff", "YPBBN", "YPCMB", "DoH", "He3oH", "He3oHe4", "Li7oH"]
    summary = {k: result[k] for k in summary_keys if k in result}
    with open(os.path.join(outdir, "summary_rounded.txt"), "w") as f:
        f.write(f"{label}\n{'=' * len(label)}\n")
        for k, v in summary.items():
            if abs(v) < 1e-3 and v != 0:
                f.write(f"{k:12s} = {v:.6e}\n")
            else:
                f.write(f"{k:12s} = {v:.8f}\n")
        f.write(f"\nruntime: {elapsed:.3f} s\n")
    print(f"[{label}] runtime={elapsed:.3f}s "
          f"Neff={result.get('Neff')!r} YPBBN={result.get('YPBBN')!r} "
          f"DoH={result.get('DoH')!r}")
    return result


def do_run(label, outdir, params, force_backend="auto", exact_command=None,
           extra_meta=None):
    t0 = time.time()
    result = run_bbn(dict(params), force_backend=force_backend, progress=False)
    elapsed = time.time() - t0
    return save_run(outdir, label, params, force_backend, result, elapsed,
                     extra_meta=extra_meta, exact_command=exact_command)


# ---------------------------------------------------------------------
# Section 4/5: deterministic baseline + documented-reference reproduction
# ---------------------------------------------------------------------
def run_baseline():
    params = dict(BASELINE_PHYSICAL, network="small")
    cmd = "primat --Omegabh2 0.022425 --DeltaNeff 0 --output_final_result --output_time_evolution"
    return do_run(
        "deterministic_baseline",
        os.path.join(ROOT, "runs/deterministic/baseline"),
        params, force_backend="auto", exact_command=cmd,
        extra_meta={"note": "PRIMATConfig defaults; network=small is the "
                             "installed library default, not overridden."},
    )


def run_documented_reference():
    params = {"Omegabh2": 0.02242, "network": "large", "amax": 8}
    cmd = "primat --Omegabh2 0.02242 --network large --amax 8"
    return do_run(
        "documented_reference_example",
        os.path.join(ROOT, "runs/deterministic/documented_reference"),
        params, force_backend="auto", exact_command=cmd,
        extra_meta={
            "note": "Reproduction of the WORKED EXAMPLE in the installed "
                    "package's own README (primat-0.3.1.dist-info/METADATA, "
                    "'Command-line interface' section), used only to "
                    "explain the provenance of the task's boxed reference "
                    "values. This is NOT the Phase 4B physical baseline.",
            "source": "primat-0.3.1.dist-info/METADATA",
        },
    )


# ---------------------------------------------------------------------
# Section 6: backend reproducibility
# ---------------------------------------------------------------------
def run_backend_comparison():
    params = dict(BASELINE_PHYSICAL, network="small")
    r_c = do_run(
        "backend_c", os.path.join(ROOT, "runs/backend/c"),
        params, force_backend="c",
        exact_command="primat --Omegabh2 0.022425 --DeltaNeff 0 --backend c",
    )
    r_py = do_run(
        "backend_python", os.path.join(ROOT, "runs/backend/python"),
        params, force_backend="python",
        exact_command="primat --Omegabh2 0.022425 --DeltaNeff 0 --backend python",
    )
    keys = ["Neff", "YPBBN", "YPCMB", "DoH", "He3oH", "He3oHe4", "Li7oH"]
    rows = []
    for k in keys:
        xc, xpy = float(r_c[k]), float(r_py[k])
        delta = xc - xpy
        rel = abs(delta) / abs(xpy) if xpy != 0 else float("nan")
        rows.append((k, xc, xpy, delta, rel))
    out_csv = os.path.join(ROOT, "results/backend_comparison.csv")
    with open(out_csv, "w") as f:
        f.write("observable,X_C,X_Python,Delta_X,rel_delta_X\n")
        for k, xc, xpy, d, rel in rows:
            f.write(f"{k},{xc!r},{xpy!r},{d!r},{rel!r}\n")
    print(f"[backend_comparison] wrote {out_csv}")
    return rows


# ---------------------------------------------------------------------
# Section 7: numerical tolerance convergence
# ---------------------------------------------------------------------
def run_tolerance_sweep():
    params_base = dict(BASELINE_PHYSICAL, network="small")
    tolerances = [1e-6, 1e-7, 1e-8, 1e-9]
    results = {}
    for tol in tolerances:
        p = dict(params_base, numerical_precision=tol)
        label = f"tolerance_{tol:.0e}"
        r = do_run(
            label, os.path.join(ROOT, f"runs/tolerance/{label}"),
            p, force_backend="c",
            exact_command=f"primat --Omegabh2 0.022425 --DeltaNeff 0 "
                           f"--numerical_precision {tol:.0e} --backend c",
        )
        results[tol] = r

    keys = ["Neff", "YPBBN", "DoH", "He3oH", "Li7oH"]
    out_csv = os.path.join(ROOT, "results/tolerance_convergence.csv")
    with open(out_csv, "w") as f:
        f.write("observable,tolerance,value\n")
        for tol in tolerances:
            for k in keys:
                f.write(f"{k},{tol:.0e},{results[tol][k]!r}\n")
        f.write("\nobservable,eps_i,eps_i+1,Delta_X,rel_change_R\n")
        for i in range(len(tolerances) - 1):
            eps_i, eps_ip1 = tolerances[i], tolerances[i + 1]
            for k in keys:
                xi, xip1 = results[eps_i][k], results[eps_ip1][k]
                delta = xi - xip1
                rel = abs(delta) / abs(xip1) if xip1 != 0 else float("nan")
                f.write(f"{k},{eps_i:.0e},{eps_ip1:.0e},{delta!r},{rel!r}\n")
    print(f"[tolerance_convergence] wrote {out_csv}")
    return results


# ---------------------------------------------------------------------
# Section 8: weak-rate resolution convergence
# ---------------------------------------------------------------------
def run_weak_rate_sweep():
    params_base = dict(BASELINE_PHYSICAL, network="small")
    resolutions = [80, 160]
    results = {}
    for n in resolutions:
        p = dict(params_base, sampling_nTOp_per_decade=n)
        label = f"weak_rate_{n}"
        r = do_run(
            label, os.path.join(ROOT, f"runs/weak_rate/{label}"),
            p, force_backend="c",
            exact_command=f"primat --Omegabh2 0.022425 --DeltaNeff 0 "
                           f"--set sampling_nTOp_per_decade={n} --backend c",
        )
        results[n] = r

    keys = ["Neff", "YPBBN", "DoH", "He3oH", "Li7oH"]
    out_csv = os.path.join(ROOT, "results/weak_rate_convergence.csv")
    with open(out_csv, "w") as f:
        f.write("observable,points_per_decade,value\n")
        for n in resolutions:
            for k in keys:
                f.write(f"{k},{n},{results[n][k]!r}\n")
        f.write("\nobservable,Delta_X_160_minus_80\n")
        for k in keys:
            delta = results[160][k] - results[80][k]
            f.write(f"{k},{delta!r}\n")
    print(f"[weak_rate_convergence] wrote {out_csv}")
    return results


# ---------------------------------------------------------------------
# Section 9: documented high-precision reference run
# ---------------------------------------------------------------------
def run_high_precision():
    my_options = {
        "verbose": False,
        "debug": False,
        "show_progress": False,
        "T_start_cosmo_MeV": 100.0,
        "sampling_temperature_per_decade": 2000,
        "rate_grid_npts": 4000,
        "numerical_precision": 1e-10,
        "sampling_nTOp_per_decade": 125,
        "sampling_nTOp_thermal_per_decade": 25,
        "vegas_n_eval": 100000,
        "vegas_n_itn": 50,
        "Omegabh2": BASELINE_PHYSICAL["Omegabh2"],
        "output_time_evolution": False,
    }
    networks = [
        ("small_network", "small", None),
        ("large_amax8", "large", 8),
        ("large_network", "large", None),
    ]
    results = {}
    for label, network, amax in networks:
        extra = {"network": network}
        if amax is not None:
            extra["amax"] = amax
        params = {**my_options, **extra}
        r = do_run(
            f"high_precision_{label}",
            os.path.join(ROOT, f"runs/deterministic/high_precision/{label}"),
            params, force_backend="python",
            exact_command=None,
            extra_meta={
                "note": "Reproduction of runfiles/primat_reference_run.py "
                        "from upstream git tag v0.3.1 (commit "
                        "508c0ea460ff018228b19e6b4398cfa3b9208fb4). "
                        "force_backend='python' as documented in that script.",
                "source_file": "runfiles/primat_reference_run.py",
                "source_tag": "v0.3.1",
            },
        )
        results[label] = r

    # Compare high-precision small-network result against the baseline.
    baseline = json.load(open(os.path.join(ROOT, "runs/deterministic/baseline/raw_output.json")))
    keys = ["Neff", "YPBBN", "DoH", "He3oH", "Li7oH"]
    out_csv = os.path.join(ROOT, "results/high_precision_comparison.csv")
    with open(out_csv, "w") as f:
        f.write("observable,baseline_(network=small,C-or-auto-backend),"
                "high_precision_small_network_(python-backend),Delta_X\n")
        for k in keys:
            xb = baseline[k]
            xh = results["small_network"][k]
            f.write(f"{k},{xb!r},{xh!r},{(xb - xh)!r}\n")
    print(f"[high_precision] wrote {out_csv}")
    return results


# ---------------------------------------------------------------------
# Sections 10-13: fixed-seed Monte Carlo (x2 for reproducibility)
# ---------------------------------------------------------------------
MC_QUANTITIES = ["YPBBN", "DoH", "He3oH", "Li7oH", "Neff"]
MC_SEED = 20260816
MC_N = 1000


def _run_one_mc(run_label, outdir):
    params = dict(BASELINE_PHYSICAL, network="small", show_progress=False)
    t0 = time.time()
    mc = run_mc(MC_N, MC_QUANTITIES, params=params, seed=MC_SEED,
                force_backend="python", n_jobs=-1, progress=False)
    elapsed = time.time() - t0

    os.makedirs(outdir, exist_ok=True)
    # Raw, full-precision paired sample table (task-mandated minimum columns
    # sample_id,Yp,D_H, extended with every other saved quantity).
    names = mc.quantity_names()
    arr = mc.samples_array()
    csv_path = os.path.join(outdir, "mc_samples.csv")
    with open(csv_path, "w") as f:
        f.write("sample_id," + ",".join(
            {"YPBBN": "Yp", "DoH": "D_H"}.get(n, n) for n in names) + "\n")
        for i, row in enumerate(arr, start=1):
            f.write(f"{i}," + ",".join(repr(float(v)) for v in row) + "\n")

    # Also keep the library's own canonical TSV dump for cross-check.
    with open(os.path.join(outdir, "mc_samples_library_dump.tsv"), "w") as f:
        f.write(dump_mc_samples(mc))

    centrals = {q: mc[q].central for q in MC_QUANTITIES}
    means = {q: mc[q].mean for q in MC_QUANTITIES}
    stds = {q: mc[q].std for q in MC_QUANTITIES}
    meta = {
        "run_label": run_label,
        "num_mc": MC_N,
        "seed": MC_SEED,
        "backend_forced": "python",
        "quantities_requested": MC_QUANTITIES,
        "quantities_saved_actual": names,
        "params": params,
        "central_values": centrals,
        "sample_means": means,
        "sample_stds": stds,
        "runtime_seconds": elapsed,
        "environment": env_metadata(),
        "exact_python_invocation": (
            f"primat.backend.run_mc({MC_N}, {MC_QUANTITIES!r}, "
            f"params={params!r}, seed={MC_SEED}, force_backend='python', n_jobs=-1)"
        ),
        "uncertainty_sources_propagated": [
            "all active nuclear reaction rate offsets p_* ~ N(0,1) independently "
            "(documented default of primat.main.mc_uncertainty, every reaction "
            "in the 'small' network)",
            "neutron lifetime tau_n ~ N(878.4, 0.5) s "
            "(tau_n_normalization=True, PRIMATConfig default)",
        ],
        "per_sample_rate_lifetime_values_available": False,
        "per_sample_rate_lifetime_values_note": (
            "primat.main.MCResult / MCQuantityResult (the public run_mc/"
            "mc_uncertainty return type, inspected directly in the "
            "installed source) exposes only the resulting per-sample "
            "OBSERVABLE values (mc[quantity].values), not the underlying "
            "per-sample p_* rate offsets or the per-sample tau_n draw. "
            "This is a genuine interface limitation, not an omission by "
            "this script -- confirmed by reading primat/main.py's "
            "mc_uncertainty implementation."
        ),
    }
    with open(os.path.join(outdir, "config.json"), "w") as f:
        json.dump(meta, f, indent=2, sort_keys=True)
    print(f"[{run_label}] MC runtime={elapsed:.2f}s "
          f"YPBBN mean={means['YPBBN']!r} std={stds['YPBBN']!r} "
          f"DoH mean={means['DoH']!r} std={stds['DoH']!r}")
    return mc, csv_path


def run_monte_carlo():
    mc1, csv1 = _run_one_mc("mc_run1", os.path.join(ROOT, "runs/monte_carlo/run1"))
    mc2, csv2 = _run_one_mc("mc_run2", os.path.join(ROOT, "runs/monte_carlo/run2"))

    # Task-mandated canonical raw sample file (run1 is the primary MC result
    # used for the covariance/likelihood analysis in later sections).
    raw_path = os.path.join(ROOT, "raw/mc_1000_samples.csv")
    with open(csv1) as src, open(raw_path, "w") as dst:
        dst.write(src.read())
    print(f"[monte_carlo] canonical raw sample file: {raw_path}")

    # Reproducibility comparison (Section 13): compare raw sample vectors.
    arr1 = mc1.samples_array()
    arr2 = mc2.samples_array()
    names = mc1.quantity_names()
    assert names == mc2.quantity_names(), "quantity order mismatch between MC runs"
    out_json = os.path.join(ROOT, "results/mc_reproducibility.json")
    report = {}
    for j, q in enumerate(names):
        col1, col2 = arr1[:, j], arr2[:, j]
        absdiff = np.abs(col1 - col2)
        n_diff = int(np.sum(absdiff > 0))
        report[q] = {
            "max_abs_diff": float(np.max(absdiff)),
            "n_samples_differing": n_diff,
            "n_samples_total": len(col1),
        }
    with open(out_json, "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    print(f"[mc_reproducibility] wrote {out_json}")
    return mc1, mc2, report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-mc", action="store_true")
    ap.add_argument("--skip-high-precision", action="store_true")
    args = ap.parse_args()

    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "raw"), exist_ok=True)

    print("=== Section 4/5: deterministic baseline + documented reference ===")
    run_baseline()
    run_documented_reference()

    print("=== Section 6: backend comparison ===")
    run_backend_comparison()

    print("=== Section 7: tolerance convergence ===")
    run_tolerance_sweep()

    print("=== Section 8: weak-rate resolution convergence ===")
    run_weak_rate_sweep()

    if not args.skip_high_precision:
        print("=== Section 9: high-precision reference run ===")
        run_high_precision()

    if not args.skip_mc:
        print("=== Sections 10-13: fixed-seed Monte Carlo x2 ===")
        run_monte_carlo()

    print("Done.")


if __name__ == "__main__":
    main()
