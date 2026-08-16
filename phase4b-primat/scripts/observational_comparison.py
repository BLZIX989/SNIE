#!/usr/bin/env python3
"""
Sections 12, 14, 15: BBN covariance export + observational comparison +
joint likelihood.

Reads audit/audit_results.json (produced by scripts/audit.py, itself
reading only the raw MC sample CSVs) and combines it with the
task-specified observational values to compute chi^2. No new PRIMAT
execution happens here.
"""
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# --- Observational values, exactly as specified by the task -----------------
# Source: as given verbatim in the Phase 4B task instructions (Section 14),
# attributed there to PDG primordial-abundance compilation values. This
# script does not download or substitute alternative observational values;
# it records only what the task specified, with that provenance made
# explicit here rather than left implicit.
OBSERVATIONAL = {
    "YPBBN": {"value": 0.245, "sigma": 0.003},
    "DoH": {"value": 25.08e-6, "sigma": 0.29e-6},
}
OBS_PROVENANCE = {
    "source": "Value and 1-sigma uncertainty as specified verbatim in the "
              "Phase 4B task instructions (Section 14), attributed there to "
              "'the specified PDG primordial abundance values'.",
    "publication_version": "NOT INDEPENDENTLY VERIFIED IN THIS AUDIT -- no "
              "specific PDG Review of Particle Physics edition/year or "
              "section number was supplied with the task's boxed values, "
              "and none was looked up or substituted. This is recorded as "
              "an explicit provenance limitation, not filled in from memory.",
    "retrieval_date": "2026-08-16 (date these values were transcribed into "
              "this audit from the task instructions, not a PDG access date)",
    "observational_covariance_available": False,
    "observational_covariance_note": "No Y_P-D/H observational covariance "
              "was supplied or is used. Per task Section 14/15, this is an "
              "explicit, stated limitation: C_obs is diagonal only.",
}


def invert_2x2(m):
    (a, b), (c, d) = m
    det = a * d - b * c
    if det == 0:
        raise ValueError("Singular covariance matrix")
    inv = [[d / det, -b / det], [-c / det, a / det]]
    return inv, det


def main():
    audit = json.load(open(os.path.join(ROOT, "audit/audit_results.json")))
    mc = audit["mc_statistics"]

    C_theory = mc["C_theory"]  # [[sigma_Y^2, Cov], [Cov, sigma_D^2]], order [Yp, D_H]
    Yp_bbn = mc["Yp_mean"]
    D_bbn = mc["D_H_mean"]

    C_obs = [[OBSERVATIONAL["YPBBN"]["sigma"] ** 2, 0.0],
             [0.0, OBSERVATIONAL["DoH"]["sigma"] ** 2]]

    C_total = [[C_theory[0][0] + C_obs[0][0], C_theory[0][1] + C_obs[0][1]],
               [C_theory[1][0] + C_obs[1][0], C_theory[1][1] + C_obs[1][1]]]

    d_vec = [OBSERVATIONAL["YPBBN"]["value"], OBSERVATIONAL["DoH"]["value"]]
    m_vec = [Yp_bbn, D_bbn]
    residual = [d_vec[0] - m_vec[0], d_vec[1] - m_vec[1]]

    C_total_inv, det = invert_2x2(C_total)
    # chi^2 = residual^T C_total_inv residual
    chi2 = 0.0
    for i in range(2):
        s = sum(C_total_inv[i][j] * residual[j] for j in range(2))
        chi2 += residual[i] * s

    out = {
        "observational_values": OBSERVATIONAL,
        "observational_provenance": OBS_PROVENANCE,
        "C_theory": {"matrix": C_theory, "row_order": ["Yp", "D_H"],
                     "source": "sample covariance of N=1000 fixed-seed MC "
                               "run1 (raw/mc_1000_samples.csv), computed "
                               "independently by scripts/audit.py"},
        "C_obs": {"matrix": C_obs, "row_order": ["Yp", "D_H"],
                  "note": "diagonal only -- no observational covariance "
                          "available (see observational_provenance)"},
        "C_total": {"matrix": C_total, "row_order": ["Yp", "D_H"]},
        "d_observed": {"Yp": d_vec[0], "D_H": d_vec[1]},
        "m_bbn": {"Yp": m_vec[0], "D_H": m_vec[1]},
        "residual_d_minus_m": {"Yp": residual[0], "D_H": residual[1]},
        "chi2": chi2,
        "degrees_of_freedom": 2,
        "likelihood_assumptions": [
            "Gaussian theory uncertainty, characterized fully by the N=1000 "
            "MC sample covariance C_theory (no distributional test beyond "
            "mean/covariance was performed).",
            "Gaussian, uncorrelated (diagonal) observational uncertainty, "
            "per the task-specified sigma values; independence between "
            "Y_P^obs and (D/H)^obs is assumed only because no observational "
            "covariance was supplied -- NOT because independence was "
            "verified.",
            "C_theory and C_obs are added directly (no additional "
            "correlation between theory and observational errors assumed).",
            "chi^2 is reported as a raw statistic; per task Section 15 it is "
            "NOT converted to a sigma-level or p-value here, since that "
            "conversion requires distributional assumptions (e.g. exact "
            "chi^2_2 distribution of the residual) not independently "
            "verified in this audit.",
        ],
    }

    out_json = os.path.join(ROOT, "results/bbn_covariance.json")
    with open(out_json, "w") as f:
        json.dump({"C_theory": out["C_theory"], "chi2_analysis": out}, f, indent=2, sort_keys=True)

    out_csv = os.path.join(ROOT, "results/bbn_covariance.csv")
    with open(out_csv, "w") as f:
        f.write("matrix,row,Yp,D_H\n")
        for name, mat in [("C_theory", C_theory), ("C_obs", C_obs), ("C_total", C_total)]:
            for i, rowname in enumerate(["Yp", "D_H"]):
                f.write(f"{name},{rowname},{mat[i][0]!r},{mat[i][1]!r}\n")

    print(f"wrote {out_json}")
    print(f"wrote {out_csv}")
    print()
    print("C_theory (from N=1000 MC):", C_theory)
    print("C_obs (diagonal, task-specified):", C_obs)
    print("C_total:", C_total)
    print("residual (d - m):", residual)
    print("chi2 =", chi2, " dof =", 2)


if __name__ == "__main__":
    main()
