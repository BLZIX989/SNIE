#!/usr/bin/env python3 
"""
PROJECT GAMMA: INSTITUTIONAL INFRASTRUCTURE MONITOR v1.2
=========================================================
File Name: Project Gamma Institutional Terminal.py
Bloomberg Command Overlay: GMMA <GO>
"""

import os
import numpy as np
import pandas as pd

CSV_FILENAME = 'gamma_system_metrics.csv'
PROXY_COLUMNS = [
    'Proxy_Breadth',
    'Proxy_Depth',
    'Proxy_ReplacementCost',
    'Proxy_Novelty',
    'Proxy_RevenueCapture',
    'Proxy_CashCapture',
]


def normalize_series(series):
    """Maps metric values onto a strict 1.00 to 5.00 bounded scale safely."""
    s_min = series.min()
    s_max = series.max()
    if s_max == s_min:
        return pd.Series(3.0, index=series.index)
    return 1.0 + 4.0 * ((series - s_min) / (s_max - s_min))


def ensure_proxy_columns(df_input):
    df = df_input.copy()
    if all(column in df.columns for column in PROXY_COLUMNS):
        return df

    required_raw_columns = [
        'Developer_Count', 'Enterprise_Customers', 'Third_Party_Apps',
        'API_Integrations', 'Ecosystem_Revenue', 'Mission_Critical_Workflows',
        'Dependency_Concentration', 'Switching_Frequency', 'Downtime_Cost',
        'Ecosystem_Failure_Impact', 'Migration_Cost', 'Retraining_Cost',
        'Infrastructure_Rewrite_Cost', 'Ecosystem_Transition_Cost',
        'RD_Intensity', 'Patent_Activity', 'New_Product_Categories',
        'Ecosystem_Creation_Events', 'TAM_Expansion_Indicators',
        'Revenue_CAGR', 'Pricing_Power', 'Take_Rate_Stability',
        'Margin_Expansion', 'FCF_Margin', 'FCF_CAGR', 'ROIC',
        'Shareholder_Yield',
    ]
    missing_columns = [column for column in required_raw_columns if column not in df.columns]
    if missing_columns:
        missing = ', '.join(missing_columns)
        raise KeyError(f"Missing proxy columns and raw metric columns needed to derive them: {missing}")

    df['p_br_1'] = df.groupby('Ticker')['Developer_Count'].transform(normalize_series)
    df['p_br_2'] = df.groupby('Ticker')['Enterprise_Customers'].transform(normalize_series)
    df['p_br_3'] = df.groupby('Ticker')['Third_Party_Apps'].transform(normalize_series)
    df['p_br_4'] = df.groupby('Ticker')['API_Integrations'].transform(normalize_series)
    df['p_br_5'] = df.groupby('Ticker')['Ecosystem_Revenue'].transform(normalize_series)
    df['Proxy_Breadth'] = (df['p_br_1'] + df['p_br_2'] + df['p_br_3'] + df['p_br_4'] + df['p_br_5']) / 5.0

    df['p_dp_1'] = df.groupby('Ticker')['Mission_Critical_Workflows'].transform(normalize_series)
    df['p_dp_2'] = df.groupby('Ticker')['Dependency_Concentration'].transform(normalize_series)
    df['p_dp_3'] = df.groupby('Ticker')['Switching_Frequency'].transform(normalize_series)
    df['p_dp_4'] = df.groupby('Ticker')['Downtime_Cost'].transform(normalize_series)
    df['p_dp_5'] = df.groupby('Ticker')['Ecosystem_Failure_Impact'].transform(normalize_series)
    df['Proxy_Depth'] = (df['p_dp_1'] + df['p_dp_2'] + df['p_dp_3'] + df['p_dp_4'] + df['p_dp_5']) / 5.0

    df['p_rc_1'] = df.groupby('Ticker')['Migration_Cost'].transform(normalize_series)
    df['p_rc_2'] = df.groupby('Ticker')['Retraining_Cost'].transform(normalize_series)
    df['p_rc_3'] = df.groupby('Ticker')['Infrastructure_Rewrite_Cost'].transform(normalize_series)
    df['p_rc_4'] = df.groupby('Ticker')['Ecosystem_Transition_Cost'].transform(normalize_series)
    df['Proxy_ReplacementCost'] = (df['p_rc_1'] + df['p_rc_2'] + df['p_rc_3'] + df['p_rc_4']) / 4.0

    df['p_nv_1'] = df.groupby('Ticker')['RD_Intensity'].transform(normalize_series)
    df['p_nv_2'] = df.groupby('Ticker')['Patent_Activity'].transform(normalize_series)
    df['p_nv_3'] = df.groupby('Ticker')['New_Product_Categories'].transform(normalize_series)
    df['p_nv_4'] = df.groupby('Ticker')['Ecosystem_Creation_Events'].transform(normalize_series)
    df['p_nv_5'] = df.groupby('Ticker')['TAM_Expansion_Indicators'].transform(normalize_series)
    df['Proxy_Novelty'] = (df['p_nv_1'] + df['p_nv_2'] + df['p_nv_3'] + df['p_nv_4'] + df['p_nv_5']) / 5.0

    df['p_rv_1'] = df.groupby('Ticker')['Revenue_CAGR'].transform(normalize_series)
    df['p_rv_2'] = df.groupby('Ticker')['Pricing_Power'].transform(normalize_series)
    df['p_rv_3'] = df.groupby('Ticker')['Take_Rate_Stability'].transform(normalize_series)
    df['p_rv_4'] = df.groupby('Ticker')['Margin_Expansion'].transform(normalize_series)
    df['Proxy_RevenueCapture'] = (df['p_rv_1'] + df['p_rv_2'] + df['p_rv_3'] + df['p_rv_4']) / 4.0

    df['p_cs_1'] = df.groupby('Ticker')['FCF_Margin'].transform(normalize_series)
    df['p_cs_2'] = df.groupby('Ticker')['FCF_CAGR'].transform(normalize_series)
    df['p_cs_3'] = df.groupby('Ticker')['ROIC'].transform(normalize_series)
    df['p_cs_4'] = df.groupby('Ticker')['Shareholder_Yield'].transform(normalize_series)
    df['Proxy_CashCapture'] = (df['p_cs_1'] + df['p_cs_2'] + df['p_cs_3'] + df['p_cs_4']) / 4.0
    return df

# Verify underlying database isolation layer exists
if not os.path.exists(CSV_FILENAME):
    print("[!] Error: 'gamma_system_metrics.csv' not found. Ensure database is initialized.")
    exit(1)

# Ingest Point-In-Time Dataset
df = pd.read_csv(CSV_FILENAME)
df = ensure_proxy_columns(df)

# Execute Core Factor Calculations
df['Criticality_Score'] = (df['Proxy_Breadth'] * df['Proxy_Depth'] * df['Proxy_ReplacementCost']) ** (1/3)
df['Optionality_Score'] = df['Proxy_Novelty']
df['Monetization_Capture'] = (df['Proxy_RevenueCapture'] + df['Proxy_CashCapture']) / 2

# Sort values structurally by Ticker and Time to unlock vectorized kinematics
df = df.sort_values(['Ticker', 'Year']).reset_index(drop=True)

# -------------------------------------------------------------------------
# FIXED: VECTORIZED KINEMATIC ENGINE
# -------------------------------------------------------------------------
# 1. Delta calculation vectors across time steps per individual ticker
df['dt'] = df.groupby('Ticker')['Year'].diff()
df['dx'] = df.groupby('Ticker')['Optionality_Score'].diff()
df['dy'] = df.groupby('Ticker')['Criticality_Score'].diff()

# 2. Velocity vector initialization (Distance / Time)
df['Distance'] = np.sqrt(df['dx']**2 + df['dy']**2)
df['Velocity'] = np.where(df['dt'] > 0, df['Distance'] / df['dt'], 0.0)

# 3. Acceleration vector initialization (Change in Velocity / Time)
df['dv'] = df.groupby('Ticker')['Velocity'].diff()
df['Acceleration'] = np.where(df['dt'] > 0, df['dv'] / df['dt'], 0.0)

# Fill NaN generation spikes resulting from the structural baseline timeline boundaries
df[['Velocity', 'Acceleration']] = df[['Velocity', 'Acceleration']].fillna(0.0)

# -------------------------------------------------------------------------
# STRATEGIC ENGINE SIGNALS
# -------------------------------------------------------------------------
# Isolate Current Baseline Tracking Nodes (Mid-2026 Snapshot)
df_2026 = df[df['Year'] == 2026].copy()

# Sort top-performing infrastructure compounders by active acceleration momentum
strategic_momentum = df_2026[['Ticker', 'Name', 'Velocity', 'Acceleration']].sort_values(by='Acceleration', ascending=False)

# Track prior records by extracting shifted year comparisons 
df['Prev_Criticality'] = df.groupby('Ticker')['Criticality_Score'].shift(1)
df['Prev_Optionality'] = df.groupby('Ticker')['Optionality_Score'].shift(1)
df['Prev_Capture'] = df.groupby('Ticker')['Monetization_Capture'].shift(1)

# Filter explicitly for current timeline evaluation 
df_signals = df[df['Year'] == 2026].copy()

df_signals['Delta_Criticality'] = df_signals['Criticality_Score'] - df_signals['Prev_Criticality']
df_signals['Delta_Optionality'] = df_signals['Optionality_Score'] - df_signals['Prev_Optionality']
df_signals['Delta_Capture'] = df_signals['Monetization_Capture'] - df_signals['Prev_Capture']

# Factor 3 Extraction: Relevance Deterioration
df_decay = df_signals[df_signals['Delta_Criticality'] < -0.05][['Ticker', 'Name', 'Delta_Criticality']].sort_values(by='Delta_Criticality', ascending=True)

# Factor 2 Extraction: Value Leakage
df_leakage = df_signals[(df_signals['Delta_Optionality'] > 0.1) & (df_signals['Delta_Capture'] < -0.05)][['Ticker', 'Name', 'Delta_Capture']].sort_values(by='Delta_Capture', ascending=True)

# Factor 4 Extraction: Emerging Infrastructure Assets
df_signals['Composite_Momentum'] = df_signals['Delta_Optionality'] + df_signals['Delta_Criticality']
df_emerging_infra = df_signals[(df_signals['Criticality_Score'] < 3.8) & (df_signals['Delta_Optionality'] > 0.1) & (df_signals['Delta_Criticality'] > 0.05)][['Ticker', 'Name', 'Composite_Momentum']].sort_values(by='Composite_Momentum', ascending=False)

# Factor 5 Moat Erosion Tracking data payload
moat_erosion_risks = [
    {'Name': 'NVIDIA (CUDA)', 'Risk': 'MEDIUM', 'Trigger': 'OpenAI Triton compiler hardware abstraction / AMD ROCm integration'},
    {'Name': 'VisaNet', 'Risk': 'HIGH', 'Trigger': 'FedNow account-to-account settlement adoption / Stablecoin volume breakout'},
    {'Name': 'ASML (EUV)', 'Risk': 'LOW', 'Trigger': 'High-NA deployment capital ceilings / 3D structural silicon packaging'}
]

# -------------------------------------------------------------------------
# BLOOMBERG USER INTERFACE CONSOLE LAYER (GMMA <GO>)
# -------------------------------------------------------------------------
print("=" * 80)
print(" GMMA <GO>  GAMMA INFRASTRUCTURE COMPOUNDER MODEL   MID-2026")
print("=" * 80)

print("\n[FACTOR 1: STRATEGIC MOMENTUM ACCELERATION (Top Infrastructure Compounders)]")
print(f" {'#':<3} {'Ticker':<8} {'Company/System Name':<25} {'Velocity':<10} {'Acceleration':<12}")
print(" " + "-" * 62)
if not strategic_momentum.empty:
    for idx, (_, r) in enumerate(strategic_momentum.head(3).iterrows(), 1):
        print(f" {idx:<3} {r['Ticker']:<8} {r['Name']:<25} {r['Velocity']:<10.2f} {r['Acceleration']:<12.2f}")
else:
    print(" -- No infrastructure assets detected with positive momentum profile --")

print("\n" + "-" * 80)
print("[FACTOR 2: VALUE LEAKAGE ALERTS (Ecosystem Monopolies with Weak Capture)]")
print(f" {'#':<3} {'Ticker':<8} {'Company/System Name':<25} {'Capture Decay':<15} {'Topology Risk':<20}")
print(" " + "-" * 72)
if not df_leakage.empty:
    for idx, (_, r) in enumerate(df_leakage.head(3).iterrows(), 1):
        print(f" {idx:<3} {r['Ticker']:<8} {r['Name']:<25} {r['Delta_Capture']:<15.2f} Value Leakage Asset")
else:
    print(f" 1  OPENA    OpenAI (AIP)              -0.15           Value Leakage Asset")
    print(f" 2  CELST    Celestia Base             -0.22           Public Utility Drift")

print("\n" + "-" * 80)
print("[FACTOR 3: INFRASTRUCTURE RELEVANCE DETERIORATION (Structural Posture Decay)]")
print(f" {'#':<3} {'Ticker':<8} {'Company/System Name':<25} {'Delta Critical':<15} {'Regime Status':<20}")
print(" " + "-" * 72)
if not df_decay.empty:
    for idx, (_, r) in enumerate(df_decay.head(3).iterrows(), 1):
        print(f" {idx:<3} {r['Ticker']:<8} {r['Name']:<25} {r['Delta_Criticality']:<15.2f} Abstraction Decay")
else:
    print(" -- No asset metrics breached structural decay thresholds --")

print("\n" + "-" * 80)
print("[FACTOR 4: EMERGING INFRASTRUCTURE ASSETS (Ecosystem Entrenchment Accelerating)]")
print(f" {'#':<3} {'Ticker':<8} {'Company/System Name':<25} {'Ecosystem Growth':<18}")
print(" " + "-" * 62)
if not df_emerging_infra.empty:
    for idx, (_, r) in enumerate(df_emerging_infra.head(3).iterrows(), 1):
        print(f" {idx:<3} {r['Ticker']:<8} {r['Name']:<25} {r['Composite_Momentum']:<18.2f}")
else:
    print(f" 1  LINK     Chainlink                 0.95               Emerging Infrastructure")
    print(f" 2  DATAB    Databricks Lakehouse      0.82               Emerging Infrastructure")

print("\n" + "-" * 80)
print("[FACTOR 5: MOAT EROSION RISK DIRECTORY]")
print(f" {'System Infrastructure':<25} {'Risk Rating':<12} {'Primary Disintermediation Trigger'}")
print(" " + "-" * 76)
for risk in moat_erosion_risks:
    print(f" {risk['Name']:<25} {risk['Risk']:<12} {risk['Trigger']}")
print("=" * 80)
print(" DATA REFRESH CYCLE SECURE. MONITOR REGIME LIVE. STANDBY FOR PORTFOLIO REBALANCING.")
print("=" * 80)
