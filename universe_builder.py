#!/usr/bin/env python3
"""Build stratified Project Gamma universes for 100+, 250+, and 500+ asset tests.

The generator keeps the original seed universe intact, expands it with a mix of
core infrastructure, adjacent infrastructure, and hard-negative names, and
writes stratified train/holdout splits for each requested universe size.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
SEED_PATH = ROOT / "snie_universe.csv"
OUTPUT_ROOT = ROOT / "universe"

REQUIRED_COLUMNS = [
    "Ticker",
    "Sector",
    "MarketCap_B",
    "OpMargin",
    "RD_Intensity",
    "CapEx_to_Assets",
    "Rev_Growth",
    "Ecosystem_Proxy",
    "Type",
]

CORE_SECTORS = {
    "Semiconductors",
    "Tech / Cloud",
    "Tech/Infra",
    "Software/Infra",
    "Software / AI",
    "Cloud/Logistics",
    "Enterprise Soft",
    "Data Infra",
}

ADJACENT_SECTORS = {
    "Consumer Tech",
    "Communication",
    "Tech/Consulting",
    "Payments",
    "Observability",
}

CORE_TEMPLATES = [
    {"sector": "Semiconductors", "type": "Core Infrastructure", "market_cap": (120, 4200), "op_margin": (0.18, 0.66), "rd": (0.08, 0.32), "capex": (0.03, 0.24), "rev_growth": (0.00, 0.42), "eco": (65, 99)},
    {"sector": "Cloud Infrastructure", "type": "Core Infrastructure", "market_cap": (45, 1800), "op_margin": (0.12, 0.48), "rd": (0.10, 0.28), "capex": (0.05, 0.18), "rev_growth": (0.08, 0.38), "eco": (60, 97)},
    {"sector": "Enterprise Software", "type": "Core Infrastructure", "market_cap": (40, 900), "op_margin": (0.10, 0.42), "rd": (0.12, 0.30), "capex": (0.02, 0.10), "rev_growth": (0.06, 0.35), "eco": (55, 95)},
    {"sector": "Cybersecurity", "type": "Core Infrastructure", "market_cap": (25, 500), "op_margin": (0.04, 0.28), "rd": (0.14, 0.34), "capex": (0.02, 0.08), "rev_growth": (0.10, 0.40), "eco": (50, 94)},
    {"sector": "Payments Infrastructure", "type": "Core Infrastructure", "market_cap": (60, 1200), "op_margin": (0.16, 0.52), "rd": (0.05, 0.18), "capex": (0.01, 0.08), "rev_growth": (0.05, 0.24), "eco": (55, 96)},
    {"sector": "Data Infrastructure", "type": "Core Infrastructure", "market_cap": (30, 850), "op_margin": (0.08, 0.36), "rd": (0.12, 0.32), "capex": (0.03, 0.12), "rev_growth": (0.08, 0.36), "eco": (58, 95)},
    {"sector": "Developer Tools", "type": "Core Infrastructure", "market_cap": (20, 420), "op_margin": (0.05, 0.26), "rd": (0.15, 0.35), "capex": (0.01, 0.08), "rev_growth": (0.08, 0.39), "eco": (50, 92)},
    {"sector": "Networking / Edge", "type": "Core Infrastructure", "market_cap": (35, 600), "op_margin": (0.10, 0.38), "rd": (0.08, 0.26), "capex": (0.04, 0.16), "rev_growth": (0.05, 0.28), "eco": (55, 94)},
    {"sector": "AI Infrastructure", "type": "Core Infrastructure", "market_cap": (40, 1100), "op_margin": (0.08, 0.34), "rd": (0.16, 0.34), "capex": (0.03, 0.14), "rev_growth": (0.12, 0.44), "eco": (60, 98)},
]

ADJACENT_TEMPLATES = [
    {"sector": "Observability", "type": "Adjacent Infrastructure", "market_cap": (12, 220), "op_margin": (0.02, 0.24), "rd": (0.10, 0.26), "capex": (0.01, 0.06), "rev_growth": (0.06, 0.30), "eco": (35, 80)},
    {"sector": "Workflow Automation", "type": "Adjacent Infrastructure", "market_cap": (10, 180), "op_margin": (0.04, 0.22), "rd": (0.08, 0.22), "capex": (0.01, 0.05), "rev_growth": (0.04, 0.24), "eco": (30, 76)},
    {"sector": "Payments", "type": "Adjacent Infrastructure", "market_cap": (18, 500), "op_margin": (0.08, 0.32), "rd": (0.03, 0.12), "capex": (0.01, 0.06), "rev_growth": (0.03, 0.18), "eco": (30, 78)},
    {"sector": "Logistics Software", "type": "Adjacent Infrastructure", "market_cap": (8, 120), "op_margin": (0.02, 0.18), "rd": (0.06, 0.18), "capex": (0.02, 0.08), "rev_growth": (0.04, 0.20), "eco": (25, 72)},
    {"sector": "Commerce Enablement", "type": "Adjacent Infrastructure", "market_cap": (8, 160), "op_margin": (0.02, 0.18), "rd": (0.05, 0.16), "capex": (0.01, 0.05), "rev_growth": (0.03, 0.18), "eco": (25, 70)},
    {"sector": "Telecom / Edge", "type": "Adjacent Infrastructure", "market_cap": (15, 260), "op_margin": (0.04, 0.20), "rd": (0.04, 0.16), "capex": (0.04, 0.18), "rev_growth": (0.01, 0.12), "eco": (20, 68)},
    {"sector": "Analytics", "type": "Adjacent Infrastructure", "market_cap": (10, 200), "op_margin": (0.02, 0.20), "rd": (0.08, 0.22), "capex": (0.01, 0.05), "rev_growth": (0.03, 0.22), "eco": (28, 74)},
    {"sector": "Collaboration", "type": "Adjacent Infrastructure", "market_cap": (8, 180), "op_margin": (0.02, 0.18), "rd": (0.04, 0.16), "capex": (0.01, 0.04), "rev_growth": (0.02, 0.16), "eco": (25, 68)},
]

NEGATIVE_TEMPLATES = [
    {"sector": "Retail", "type": "Hard Negative", "market_cap": (3, 220), "op_margin": (-0.02, 0.18), "rd": (0.01, 0.08), "capex": (0.03, 0.12), "rev_growth": (-0.08, 0.10), "eco": (5, 38)},
    {"sector": "Healthcare Services", "type": "Hard Negative", "market_cap": (5, 240), "op_margin": (-0.02, 0.20), "rd": (0.01, 0.10), "capex": (0.02, 0.10), "rev_growth": (-0.05, 0.12), "eco": (4, 42)},
    {"sector": "Industrials", "type": "Hard Negative", "market_cap": (4, 260), "op_margin": (0.00, 0.16), "rd": (0.01, 0.08), "capex": (0.04, 0.18), "rev_growth": (-0.06, 0.10), "eco": (3, 36)},
    {"sector": "Energy", "type": "Hard Negative", "market_cap": (6, 400), "op_margin": (-0.04, 0.18), "rd": (0.00, 0.06), "capex": (0.05, 0.20), "rev_growth": (-0.15, 0.08), "eco": (2, 34)},
    {"sector": "Utilities", "type": "Hard Negative", "market_cap": (8, 280), "op_margin": (0.02, 0.20), "rd": (0.00, 0.05), "capex": (0.05, 0.18), "rev_growth": (-0.04, 0.05), "eco": (2, 30)},
    {"sector": "Consumer Brands", "type": "Hard Negative", "market_cap": (4, 260), "op_margin": (0.01, 0.20), "rd": (0.00, 0.06), "capex": (0.02, 0.08), "rev_growth": (-0.02, 0.12), "eco": (2, 34)},
    {"sector": "Travel", "type": "Hard Negative", "market_cap": (3, 160), "op_margin": (-0.05, 0.14), "rd": (0.00, 0.05), "capex": (0.02, 0.10), "rev_growth": (-0.20, 0.15), "eco": (1, 28)},
    {"sector": "Banking", "type": "Hard Negative", "market_cap": (20, 700), "op_margin": (0.02, 0.20), "rd": (0.01, 0.05), "capex": (0.01, 0.06), "rev_growth": (-0.05, 0.12), "eco": (2, 30)},
    {"sector": "Insurance", "type": "Hard Negative", "market_cap": (15, 420), "op_margin": (0.03, 0.18), "rd": (0.01, 0.05), "capex": (0.01, 0.05), "rev_growth": (-0.04, 0.10), "eco": (2, 28)},
    {"sector": "Media", "type": "Hard Negative", "market_cap": (5, 240), "op_margin": (-0.02, 0.16), "rd": (0.00, 0.07), "capex": (0.01, 0.06), "rev_growth": (-0.12, 0.10), "eco": (1, 26)},
]

ADJECTIVES = [
    "Atlas", "Nova", "Vertex", "Meridian", "Pioneer", "Summit", "Cipher", "Helix",
    "Vector", "Strata", "Pillar", "Prism", "Quantum", "Apex", "Catalyst", "Signal",
    "Orbit", "Nexus", "Pulse", "Fusion"
]

NOUNS = [
    "Systems", "Networks", "Labs", "Data", "Cloud", "Stack", "Grid", "Works",
    "Dynamics", "Layer", "Fabric", "Engine", "Bridge", "Core", "Loop", "Flow",
    "Mesh", "Pulse", "Forge", "Edge"
]


def load_seed_universe() -> pd.DataFrame:
    if not SEED_PATH.exists():
        raise FileNotFoundError(f"Seed universe missing: {SEED_PATH}")

    df = pd.read_csv(SEED_PATH)
    df.columns = df.columns.str.strip()

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise KeyError(f"Seed universe is missing required columns: {', '.join(missing)}")

    return df


def sector_bucket(sector: str) -> str:
    if sector in CORE_SECTORS:
        return "core"
    if sector in ADJACENT_SECTORS:
        return "adjacent"
    return "adjacent" if any(keyword in sector.lower() for keyword in ["tech", "software", "cloud", "data", "infra"]) else "negative"


def clamp(value: float, low: float, high: float) -> float:
    return float(np.clip(value, low, high))


def pick_name(rng: np.random.Generator, sector: str, index: int) -> str:
    adjective = rng.choice(ADJECTIVES)
    noun = rng.choice(NOUNS)
    suffix = sector.replace("/", " ").replace(" ", "")[:8]
    return f"{adjective} {noun} {suffix} {index:03d}"


def sample_metric(rng: np.random.Generator, low: float, high: float, skew: float = 1.0) -> float:
    if high <= low:
        return float(low)
    draw = rng.beta(skew, skew) if skew != 1.0 else rng.random()
    return float(low + (high - low) * draw)


def seed_profile(df: pd.DataFrame, bucket: str) -> Dict[str, float]:
    subset = df[df["Bucket"] == bucket]
    if subset.empty:
        subset = df
    numeric_cols = ["MarketCap_B", "OpMargin", "RD_Intensity", "CapEx_to_Assets", "Rev_Growth", "Ecosystem_Proxy"]
    return subset[numeric_cols].mean(numeric_only=True).to_dict()


def classify_seed_rows(df: pd.DataFrame) -> pd.DataFrame:
    classified = df.copy()
    classified["Bucket"] = classified["Sector"].apply(sector_bucket)
    classified["Source"] = "seed"
    classified["Universe_Level"] = len(classified)
    classified["Holdout_Flag"] = False
    return classified


def build_synthetic_row(
    rng: np.random.Generator,
    bucket: str,
    template: Dict[str, object],
    anchor: Dict[str, float],
    index: int,
) -> Dict[str, object]:
    name = pick_name(rng, str(template["sector"]), index)

    cap_low, cap_high = template["market_cap"]
    margin_low, margin_high = template["op_margin"]
    rd_low, rd_high = template["rd"]
    capex_low, capex_high = template["capex"]
    growth_low, growth_high = template["rev_growth"]
    eco_low, eco_high = template["eco"]

    if bucket == "core":
        cap_anchor = float(anchor.get("MarketCap_B", (cap_low + cap_high) / 2.0))
        margin_anchor = float(anchor.get("OpMargin", (margin_low + margin_high) / 2.0))
        rd_anchor = float(anchor.get("RD_Intensity", (rd_low + rd_high) / 2.0))
        capex_anchor = float(anchor.get("CapEx_to_Assets", (capex_low + capex_high) / 2.0))
        growth_anchor = float(anchor.get("Rev_Growth", (growth_low + growth_high) / 2.0))
        eco_anchor = float(anchor.get("Ecosystem_Proxy", (eco_low + eco_high) / 2.0))
    elif bucket == "adjacent":
        cap_anchor = float(anchor.get("MarketCap_B", (cap_low + cap_high) / 2.0)) * 0.55
        margin_anchor = float(anchor.get("OpMargin", (margin_low + margin_high) / 2.0)) * 0.8
        rd_anchor = float(anchor.get("RD_Intensity", (rd_low + rd_high) / 2.0)) * 0.9
        capex_anchor = float(anchor.get("CapEx_to_Assets", (capex_low + cap_high) / 2.0)) * 0.9
        growth_anchor = float(anchor.get("Rev_Growth", (growth_low + growth_high) / 2.0))
        eco_anchor = float(anchor.get("Ecosystem_Proxy", (eco_low + eco_high) / 2.0))
    else:
        cap_anchor = (cap_low + cap_high) / 2.0
        margin_anchor = (margin_low + margin_high) / 2.0
        rd_anchor = (rd_low + rd_high) / 2.0
        capex_anchor = (capex_low + capex_high) / 2.0
        growth_anchor = (growth_low + growth_high) / 2.0
        eco_anchor = (eco_low + eco_high) / 2.0

    market_cap = clamp(rng.lognormal(mean=np.log(max(cap_anchor, 1.0)), sigma=0.25), cap_low, cap_high)
    op_margin = clamp(margin_anchor + rng.normal(0, 0.05), margin_low, margin_high)
    rd_intensity = clamp(rd_anchor + rng.normal(0, 0.03), rd_low, rd_high)
    capex_to_assets = clamp(capex_anchor + rng.normal(0, 0.02), capex_low, capex_high)
    rev_growth = clamp(growth_anchor + rng.normal(0, 0.04), growth_low, growth_high)
    eco_proxy = clamp(eco_anchor + rng.normal(0, 6.0), eco_low, eco_high)

    ticker = f"{bucket[0].upper()}{index:03d}"

    return {
        "Ticker": ticker,
        "Sector": str(template["sector"]),
        "MarketCap_B": round(market_cap, 2),
        "OpMargin": round(op_margin, 4),
        "RD_Intensity": round(rd_intensity, 4),
        "CapEx_to_Assets": round(capex_to_assets, 4),
        "Rev_Growth": round(rev_growth, 4),
        "Ecosystem_Proxy": round(eco_proxy, 2),
        "Type": str(template["type"]),
        "Bucket": bucket,
        "Source": "synthetic",
        "Universe_Level": 0,
        "Holdout_Flag": False,
        "Name": name,
    }


def build_universe(seed_df: pd.DataFrame, target_size: int) -> pd.DataFrame:
    if target_size < len(seed_df):
        raise ValueError(f"Target size {target_size} is smaller than the {len(seed_df)}-row seed universe.")

    classified_seed = classify_seed_rows(seed_df)
    synthetic_needed = target_size - len(classified_seed)

    if target_size not in {100, 250, 500}:
        raise KeyError("Unsupported target size. Supported sizes: 100, 250, 500")

    if target_size == 100:
        synth_weights = {"core": 0.34, "adjacent": 0.33, "negative": 0.33}
    elif target_size == 250:
        synth_weights = {"core": 0.32, "adjacent": 0.34, "negative": 0.34}
    else:
        synth_weights = {"core": 0.30, "adjacent": 0.35, "negative": 0.35}

    raw_counts = {bucket: int(np.floor(synthetic_needed * weight)) for bucket, weight in synth_weights.items()}
    remainder = synthetic_needed - sum(raw_counts.values())
    for bucket in ["negative", "adjacent", "core"]:
        if remainder <= 0:
            break
        raw_counts[bucket] += 1
        remainder -= 1

    synth_counts = raw_counts

    rng = np.random.default_rng(seed=target_size)
    core_anchor = seed_profile(classified_seed, "core")
    adjacent_anchor = seed_profile(classified_seed, "adjacent")
    negative_anchor = seed_profile(classified_seed, "negative")

    all_rows: List[Dict[str, object]] = classified_seed.to_dict(orient="records")
    counters = {"core": 1, "adjacent": 1, "negative": 1}

    bucket_templates = {
        "core": CORE_TEMPLATES,
        "adjacent": ADJACENT_TEMPLATES,
        "negative": NEGATIVE_TEMPLATES,
    }
    anchors = {
        "core": core_anchor,
        "adjacent": adjacent_anchor,
        "negative": negative_anchor,
    }

    for bucket, count in synth_counts.items():
        templates = bucket_templates[bucket]
        anchor = anchors[bucket]
        for _ in range(count):
            template = templates[(counters[bucket] - 1) % len(templates)]
            row = build_synthetic_row(rng, bucket, template, anchor, counters[bucket])
            counters[bucket] += 1
            all_rows.append(row)

    universe = pd.DataFrame(all_rows)
    universe = universe.drop_duplicates(subset=["Ticker"], keep="first").reset_index(drop=True)

    if len(universe) != target_size:
        raise RuntimeError(f"Generated {len(universe)} rows but expected {target_size}.")

    universe["Universe_Level"] = target_size
    return universe


def stratified_split(df: pd.DataFrame, holdout_fraction: float, seed: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    holdout_indices: List[int] = []

    group_columns = ["Bucket", "Sector"] if "Bucket" in df.columns else ["Sector"]
    for _, group in df.groupby(group_columns, dropna=False):
        if len(group) == 1:
            continue

        desired = int(round(len(group) * holdout_fraction))
        if desired == 0:
            desired = 1
        if desired >= len(group):
            desired = len(group) - 1

        chosen = rng.choice(group.index.to_numpy(), size=desired, replace=False)
        holdout_indices.extend(chosen.tolist())

    holdout = df.loc[sorted(set(holdout_indices))].copy()
    train = df.drop(index=holdout.index).copy()

    train["Holdout_Flag"] = False
    holdout["Holdout_Flag"] = True
    return train.reset_index(drop=True), holdout.reset_index(drop=True)


def write_bundle(df: pd.DataFrame, target_size: int, output_root: Path, holdout_fraction: float, seed: int) -> None:
    size_dir = output_root / str(target_size)
    size_dir.mkdir(parents=True, exist_ok=True)

    universe_path = size_dir / "universe.csv"
    train_path = size_dir / "train.csv"
    holdout_path = size_dir / "holdout.csv"

    train_df, holdout_df = stratified_split(df, holdout_fraction=holdout_fraction, seed=seed)

    df.to_csv(universe_path, index=False)
    train_df.to_csv(train_path, index=False)
    holdout_df.to_csv(holdout_path, index=False)

    core_count = int((df["Bucket"] == "core").sum()) if "Bucket" in df.columns else 0
    adjacent_count = int((df["Bucket"] == "adjacent").sum()) if "Bucket" in df.columns else 0
    negative_count = int((df["Bucket"] == "negative").sum()) if "Bucket" in df.columns else 0

    print(f"[+] Wrote {universe_path.relative_to(ROOT)} ({len(df)} rows)")
    print(f"    Core / Adjacent / Negative: {core_count} / {adjacent_count} / {negative_count}")
    print(f"    Train / Holdout: {len(train_df)} / {len(holdout_df)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build larger, stratified Project Gamma universes.")
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=[100, 250, 500],
        help="Universe sizes to generate. Defaults to 100 250 500.",
    )
    parser.add_argument(
        "--holdout-fraction",
        type=float,
        default=0.2,
        help="Fraction of each stratified group to reserve for holdout.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=OUTPUT_ROOT,
        help="Root folder for generated universes.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    seed_df = load_seed_universe()
    print(f"[*] Loaded seed universe from {SEED_PATH.relative_to(ROOT)} ({len(seed_df)} rows)")

    for size in args.sizes:
        universe_df = build_universe(seed_df, size)
        write_bundle(universe_df, size, args.output_root, args.holdout_fraction, seed=size)

    print("[+] Universe expansion complete.")


if __name__ == "__main__":
    main()
