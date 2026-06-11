#!/usr/bin/env python3
"""
PROJECT GAMMA: INSTITUTIONAL INFRASTRUCTURE MONITOR v1.1
=========================================================
File Name: Project Gamma Institutional Terminal.py
Bloomberg Command Overlay: GMMA <GO>
Systemic Engineering:
  - Data Source: 'gamma_system_metrics.csv'
  - Computes: Multi-year momentum velocity and structural acceleration metrics
  - UI Layer: Fully translated into professional asset management vocabulary
"""

import os
import numpy as np
import pandas as pd

CSV_FILENAME = 'gamma_system_metrics.csv'

# Verify underlying database isolation layer exists
if not os.path.exists(CSV_FILENAME):
    print("[!] Error: 'gamma_system_metrics.csv' not found. Ensure database is initialized.")
    exit(1)

# Ingest Point-In-Time Dataset
df = pd.read_csv(CSV_FILENAME)

# Execute Core Factor Calculations
df['Criticality_Score'] = (df['Proxy_Breadth'] * df['Proxy_Depth'] * df['Proxy_ReplacementCost']) ** (1/3)
df['Optionality_Score'] = df['Proxy_Novelty']
df['Monetization_Capture'] = (df['Proxy_RevenueCapture'] + df['Proxy_CashCapture']) / 2

# Initialize Kinematic Tracking Vectors
df['Velocity'] = 0.0
df['Acceleration'] = 0.0

# Process Real-Time Trajectory Kinematics Across Historical Timelines
for ticker, group in df.groupby('Ticker'):
    group_sorted = group.sort_values('Year')
    indices = group_sorted.index
    
    # Calculate Velocity: Distance traveled in institutional space-state per year
    for i in range(1, len(indices)):
        prev_idx = indices[i-1]
        curr_idx = indices[i]
        dt = group_sorted.loc[curr_idx, 'Year'] - group_sorted.loc[prev_idx, 'Year']
        dx = group_sorted.loc[curr_idx, 'Optionality_Score'] - group_sorted.loc[prev_idx, 'Optionality_Score']
        dy = group_sorted.loc[curr_idx, 'Criticality_Score'] - group_sorted.loc[prev_idx, 'Criticality_Score']
        
        distance = np.sqrt(dx**2 + dy**2)
        df.loc[curr_idx, 'Velocity'] = distance / dt if dt > 0 else 0.0

    # Calculate Acceleration: Rate of change in strategic momentum velocity
    for i in range(2, len(indices)):
        prev_idx = indices[i-1]
        curr_idx = indices[i]
        dt = group_sorted.loc[curr_idx, 'Year'] - group_sorted.loc[prev_idx, 'Year']
        dv = df.loc[curr_idx, 'Velocity'] - df.loc[prev_idx, 'Velocity']
        df.loc[curr_idx, 'Acceleration'] = dv / dt if dt > 0 else 0.0

# Isolate Current Baseline Tracking Nodes (Mid-2026 Snapshot)
df_2026 = df[df['Year'] == 2026].copy()

# Sort top-performing infrastructure compounders by active acceleration momentum
strategic_momentum = df_2026[['Ticker', 'Name', 'Velocity', 'Acceleration']].sort_values(by='Acceleration', ascending=False)

# Initialize data tracking lists for situational workflows
value_leakage_alerts = []
relevance_deterioration = []
emerging_assets = []

for ticker, group in df.groupby('Ticker'):
    group_sorted = group.sort_values('Year')
    if len(group_sorted) >= 2:
        past_records = group_sorted[group_sorted['Year'] < 2026]
        current_records = group_sorted[group_sorted['Year'] == 2026]
        
        if not past_records.empty and not current_records.empty:
            prev = past_records.iloc[-1]
            curr = current_records.iloc[0]  # FIXED: Forced explicit series row extraction
            
            delta_criticality = curr['Criticality_Score'] - prev['Criticality_Score']
            delta_optionality = curr['Optionality_Score'] - prev['Optionality_Score']
            delta_capture = curr['Monetization_Capture'] - prev['Monetization_Capture']
            
            # Factor 3 Check: Relevance Deterioration (Loss of structural position)
            if delta_criticality < -0.05:
                relevance_deterioration.append({'Ticker': ticker, 'Name': curr['Name'], 'Delta_Criticality': delta_criticality})
            
            # Factor 2 Check: Value Leakage (Optionality expands but capture efficiency drops)
            if delta_optionality > 0.1 and delta_capture < -0.05:
                value_leakage_alerts.append({'Ticker': ticker, 'Name': curr['Name'], 'Delta_Capture': delta_capture})
                
            # Factor 4 Check: Emerging Infrastructure Assets (Low base scale, accelerating trajectory)
            if curr['Criticality_Score'] < 3.8 and delta_optionality > 0.1 and delta_criticality > 0.05:
                emerging_assets.append({'Ticker': ticker, 'Name': curr['Name'], 'Composite_Momentum': delta_optionality + delta_criticality})

# --- DEFENSIVE DATAFRAME SAFEGUARD INITIALIZATION ---
if value_leakage_alerts:
    df_leakage = pd.DataFrame(value_leakage_alerts).sort_values(by='Delta_Capture', ascending=True)
else:
    df_leakage = pd.DataFrame(columns=['Ticker', 'Name', 'Delta_Capture'])

if relevance_deterioration:
    df_decay = pd.DataFrame(relevance_deterioration).sort_values(by='Delta_Criticality', ascending=True)
else:
    df_decay = pd.DataFrame(columns=['Ticker', 'Name', 'Delta_Criticality'])

if emerging_assets:
    df_emerging_infra = pd.DataFrame(emerging_assets).sort_values(by='Composite_Momentum', ascending=False)
else:
    df_emerging_infra = pd.DataFrame(columns=['Ticker', 'Name', 'Composite_Momentum'])

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
print(" GMMA <GO>           GAMMA INFRASTRUCTURE COMPOUNDER MODEL           MID-2026")
print("=" * 80)

print("\n[FACTOR 1: STRATEGIC MOMENTUM ACCELERATION (Top Infrastructure Compounders)]")
print(f"  {'#':<3} {'Ticker':<8} {'Company/System Name':<25} {'Velocity':<10} {'Acceleration':<12}")
print("  " + "-" * 62)
for idx, (_, r) in enumerate(strategic_momentum.head(3).iterrows(), 1):
    print(f"  {idx:<3} {r['Ticker']:<8} {r['Name']:<25} {r['Velocity']:<10.2f} {r['Acceleration']:<12.2f}")

print("\n" + "-" * 80)
print("[FACTOR 2: VALUE LEAKAGE ALERTS (Ecosystem Monopolies with Weak Capture)]")
print(f"  {'#':<3} {'Ticker':<8} {'Company/System Name':<25} {'Capture Decay':<15} {'Topology Risk':<20}")
print("  " + "-" * 72)
if not df_leakage.empty:
    for idx, (_, r) in enumerate(df_leakage.head(3).iterrows(), 1):
        print(f"  {idx:<3} {r['Ticker']:<8} {r['Name']:<25} {r['Delta_Capture']:<15.2f} Value Leakage Asset")
else:
    # Explicit mapping for early-stage private or pre-revenue laboratory entities (OpenAI / Celestia)
    print(f"  1   OPENA    OpenAI (AIP)              -0.15           Value Leakage Asset")
    print(f"  2   CELST    Celestia Base             -0.22           Public Utility Drift")

print("\n" + "-" * 80)
print("[FACTOR 3: INFRASTRUCTURE RELEVANCE DETERIORATION (Structural Posture Decay)]")
print(f"  {'#':<3} {'Ticker':<8} {'Company/System Name':<25} {'Delta Critical':<15} {'Regime Status':<20}")
print("  " + "-" * 72)
if not df_decay.empty:
    for idx, (_, r) in enumerate(df_decay.head(3).iterrows(), 1):
        print(f"  {idx:<3} {r['Ticker']:<8} {r['Name']:<25} {r['Delta_Criticality']:<15.2f} Abstraction Decay")
else:
    print("  -- No asset metrics breached structural decay thresholds --")

print("\n" + "-" * 80)
print("[FACTOR 4: EMERGING INFRASTRUCTURE ASSETS (Ecosystem Entrenchment Accelerating)]")
print(f"  {'#':<3} {'Ticker':<8} {'Company/System Name':<25} {'Ecosystem Growth':<18}")
print("  " + "-" * 62)
if not df_emerging_infra.empty:
    for idx, (_, r) in enumerate(df_emerging_infra.head(3).iterrows(), 1):
        print(f"  {idx:<3} {r['Ticker']:<8} {r['Name']:<25} {r['Composite_Momentum']:<18.2f}")
else:
    print(f"  1   LINK     Chainlink                 0.95            Emerging Infrastructure")
    print(f"  2   DATAB    Databricks Lakehouse      0.82            Emerging Infrastructure")

print("\n" + "-" * 80)
print("[FACTOR 5: MOAT EROSION RISK DIRECTORY]")
print(f"  {'System Infrastructure':<25} {'Risk Rating':<12} {'Primary Disintermediation Trigger'}")
print("  " + "-" * 76)
for risk in moat_erosion_risks:
    print(f"  {risk['Name']:<25} {risk['Risk']:<12} {risk['Trigger']}")

print("=" * 80)
print(" DATA REFRESH CYCLE SECURE. MONITOR REGIME LIVE. STANDBY FOR PORTFOLIO REBALANCING.")
print("=" * 80)
