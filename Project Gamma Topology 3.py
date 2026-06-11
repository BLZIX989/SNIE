#!/usr/bin/env python3
"""
PROJECT GAMMA: SEPARATED DISCIPLINE OBSERVER v5.0
=================================================
File Name: Project Gamma Topology 2.py
Design Paradigm:
  - Data Isolation: Sourced via external 'gamma_system_metrics.csv'
  - Chart 1 (Observation Engine): Strict empirical metrics only. purges all theory.
  - Chart 2 (Explanatory Field): Strategic hypotheses mapping Selector Regimes.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CSV_FILENAME = 'gamma_system_metrics.csv'

# Initialize the standardized database if it is missing
if not os.path.exists(CSV_FILENAME):
    raw_data = [
        ['NVDA', 'NVIDIA (CUDA)', 2012, 'thermodynamic', 1.5, 1.2, 1.1, 2.0, 2.5, 2.5, 0.9],
        ['NVDA', 'NVIDIA (CUDA)', 2016, 'thermodynamic', 3.4, 3.0, 2.5, 3.8, 3.2, 3.2, 0.95],
        ['NVDA', 'NVIDIA (CUDA)', 2021, 'thermodynamic', 4.5, 4.2, 3.9, 4.5, 4.0, 4.0, 0.95],
        ['NVDA', 'NVIDIA (CUDA)', 2026, 'thermodynamic', 5.0, 4.8, 4.9, 4.6, 4.8, 4.8, 0.95],
        ['NVDA', 'NVIDIA (CUDA)', 2030, 'thermodynamic', 5.0, 5.2, 5.4, 4.9, 4.9, 4.8, 0.85],
        ['STRIP', 'Stripe', 2011, 'coordination', 2.0, 1.1, 1.0, 3.2, 2.0, 2.0, 0.7],
        ['STRIP', 'Stripe', 2016, 'coordination', 3.5, 2.2, 1.9, 3.8, 2.8, 2.8, 0.8],
        ['STRIP', 'Stripe', 2021, 'coordination', 4.4, 3.0, 2.8, 4.2, 3.5, 3.5, 0.85],
        ['STRIP', 'Stripe', 2026, 'coordination', 4.8, 3.5, 3.4, 4.4, 3.8, 3.8, 0.85],
        ['STRIP', 'Stripe', 2030, 'coordination', 4.9, 4.2, 4.0, 4.6, 4.2, 4.2, 0.75],
        ['ASML', 'ASML (EUV)', 2010, 'thermodynamic', 1.2, 3.0, 2.5, 3.5, 3.0, 3.0, 0.9],
        ['ASML', 'ASML (EUV)', 2016, 'thermodynamic', 1.5, 4.2, 3.8, 3.8, 3.8, 3.8, 0.95],
        ['ASML', 'ASML (EUV)', 2021, 'thermodynamic', 2.8, 4.9, 4.8, 3.8, 4.4, 4.4, 0.95],
        ['ASML', 'ASML (EUV)', 2026, 'thermodynamic', 3.3, 5.0, 5.0, 3.8, 4.5, 4.5, 0.95],
        ['ASML', 'ASML (EUV)', 2030, 'thermodynamic', 3.5, 5.4, 5.5, 4.0, 4.5, 4.5, 0.85],
        ['V', 'VisaNet', 1995, 'coordination', 3.5, 4.0, 4.4, 2.2, 4.8, 4.8, 0.95],
        ['V', 'VisaNet', 2010, 'coordination', 4.0, 4.4, 4.6, 2.2, 4.8, 4.8, 0.95],
        ['V', 'VisaNet', 2018, 'coordination', 4.3, 4.6, 4.8, 2.2, 4.8, 4.8, 0.95],
        ['V', 'VisaNet', 2026, 'coordination', 4.3, 4.8, 4.9, 2.2, 4.8, 4.8, 0.95],
        ['V', 'VisaNet', 2030, 'coordination', 4.2, 4.9, 4.9, 2.1, 4.7, 4.7, 0.9],
        ['LIN', 'Linde plc', 2005, 'coordination', 2.0, 3.5, 3.8, 1.5, 4.0, 4.0, 0.9],
        ['LIN', 'Linde plc', 2015, 'coordination', 2.4, 4.0, 4.2, 1.6, 4.0, 4.0, 0.95],
        ['LIN', 'Linde plc', 2022, 'coordination', 2.6, 4.2, 4.4, 1.6, 4.0, 4.0, 0.95],
        ['LIN', 'Linde plc', 2026, 'coordination', 2.6, 4.4, 4.4, 1.6, 4.0, 4.0, 0.95],
        ['LIN', 'Linde plc', 2030, 'coordination', 2.5, 4.4, 4.5, 1.5, 3.8, 3.8, 0.85],
        ['WM', 'Waste Mgmt', 2000, 'coordination', 1.8, 2.0, 2.4, 1.2, 4.2, 4.2, 0.9],
        ['WM', 'Waste Mgmt', 2012, 'coordination', 2.1, 2.2, 2.5, 1.3, 4.2, 4.2, 0.95],
        ['WM', 'Waste Mgmt', 2020, 'coordination', 2.3, 2.5, 2.7, 1.4, 4.3, 4.3, 0.95],
        ['WM', 'Waste Mgmt', 2026, 'coordination', 2.3, 2.67, 2.7, 1.4, 4.3, 4.3, 0.95],
        ['WM', 'Waste Mgmt', 2030, 'coordination', 2.2, 2.7, 2.7, 1.3, 4.2, 4.2, 0.85],
        ['OPENA', 'OpenAI (AIP)', 2016, 'thermodynamic', 2.5, 0.5, 0.5, 4.5, 1.0, 1.0, 0.5],
        ['OPENA', 'OpenAI (AIP)', 2020, 'thermodynamic', 3.2, 1.0, 1.2, 4.6, 1.5, 1.5, 0.6],
        ['OPENA', 'OpenAI (AIP)', 2023, 'thermodynamic', 3.6, 1.5, 1.9, 4.7, 2.0, 2.0, 0.7],
        ['OPENA', 'OpenAI (AIP)', 2026, 'thermodynamic', 3.8, 2.2, 2.7, 4.8, 2.5, 2.5, 0.75],
        ['OPENA', 'OpenAI (AIP)', 2030, 'thermodynamic', 4.2, 3.5, 4.0, 4.9, 3.5, 3.5, 0.65],
        ['META', 'Meta (Llama)', 2016, 'reflexive', 2.0, 1.5, 2.0, 2.2, 4.5, 4.5, 0.9],
        ['META', 'Meta (Llama)', 2020, 'reflexive', 2.2, 1.2, 1.7, 2.5, 4.5, 4.5, 0.9],
        ['META', 'Meta (Llama)', 2023, 'reflexive', 3.2, 1.8, 2.2, 3.5, 4.2, 4.2, 0.95],
        ['META', 'Meta (Llama)', 2026, 'reflexive', 4.5, 2.6, 3.0, 4.7, 4.5, 4.5, 0.95],
        ['META', 'Meta (Llama)', 2030, 'reflexive', 4.8, 4.0, 4.4, 4.9, 4.6, 4.6, 0.85],
        ['AAPL', 'Apple (iOS)', 2012, 'reflexive', 3.5, 4.0, 4.4, 3.8, 4.8, 4.8, 0.95],
        ['AAPL', 'Apple (iOS)', 2018, 'reflexive', 3.4, 3.6, 4.0, 3.5, 4.8, 4.8, 0.95],
        ['AAPL', 'Apple (iOS)', 2022, 'reflexive', 3.2, 3.2, 3.7, 3.2, 4.8, 4.8, 0.95],
        ['AAPL', 'Apple (iOS)', 2026, 'reflexive', 2.8, 2.8, 3.2, 2.8, 4.8, 4.8, 0.95],
        ['AAPL', 'Apple (iOS)', 2030, 'reflexive', 2.2, 2.2, 2.7, 2.4, 4.5, 4.5, 0.85],
        ['LINUX', 'Linux Base', 1995, 'coordination', 3.2, 2.0, 2.0, 3.5, 0.1, 0.1, 0.95],
        ['LINUX', 'Linux Base', 2005, 'coordination', 4.0, 3.5, 4.0, 4.2, 0.1, 0.1, 0.95],
        ['LINUX', 'Linux Base', 2015, 'coordination', 4.6, 5.0, 5.4, 4.8, 0.1, 0.1, 0.95],
        ['LINUX', 'Linux Base', 2026, 'coordination', 4.8, 5.6, 6.0, 5.0, 0.1, 0.1, 0.95],
        ['LINUX', 'Linux Base', 2030, 'coordination', 4.9, 5.8, 6.2, 5.2, 0.1, 0.1, 0.85]
    ]
    columns = [
        'Ticker', 'Name', 'Year', 'Selector',
        'Proxy_Breadth', 'Proxy_Depth', 'Proxy_ReplacementCost',
        'Proxy_Novelty', 'Proxy_RevenueCapture', 'Proxy_CashCapture', 'Proxy_Confidence'
    ]
    df_init = pd.DataFrame(raw_data, columns=columns)
    df_init.to_csv(CSV_FILENAME, index=False)
    print(f"[*] Relational database established: {CSV_FILENAME}")

# Process and normalize data vectors
df_raw = pd.read_csv(CSV_FILENAME)
df_raw['SGI'] = (df_raw['Proxy_Breadth'] * df_raw['Proxy_Depth'] * df_raw['Proxy_ReplacementCost']) ** (1/3)
df_raw['Γ2'] = df_raw['Proxy_Novelty']
df_raw['Translation'] = (df_raw['Proxy_RevenueCapture'] + df_raw['Proxy_CashCapture']) / 2
df_clean = df_raw[['Ticker', 'Name', 'Year', 'Selector', 'Γ2', 'SGI', 'Translation', 'Proxy_Confidence']].copy()

entity_colors = {
    'NVDA': '#11c662', 'STRIP': '#635bff', 'ASML': '#00a1e0', 'V': '#1a1f71',
    'LIN': '#005a9c', 'WM': '#006644', 'OPENA': '#ff4a00', 'META': '#0668e1',
    'AAPL': '#a3aaae', 'LINUX': '#333333'
}
entity_markers = {
    'NVDA': 'o', 'STRIP': 'o', 'ASML': 's', 'V': '^', 'LIN': 'v',
    'WM': 'D', 'OPENA': '*', 'META': '*', 'AAPL': 'X', 'LINUX': 'p'
}

# -------------------------------------------------------------------------
# CHART 1: THE PURE OBSERVATION ENGINE (STRICT DATA ONLY)
# -------------------------------------------------------------------------
fig1, ax1 = plt.subplots(figsize=(12, 9), dpi=300)
fig1.patch.set_facecolor('#ffffff')
ax1.set_facecolor('#fafafa')

for ticker, group in df_clean.groupby('Ticker'):
    group_sorted = group.sort_values('Year')
    past = group_sorted[group_sorted['Year'] < 2026]
    current = group_sorted[group_sorted['Year'] == 2026]
    
    color = entity_colors.get(ticker, '#7f7f7f')
    marker = entity_markers.get(ticker, 'o')
    
    # Plot empirical historical lines
    ax1.plot(group_sorted[group_sorted['Year'] <= 2026]['Γ2'], 
             group_sorted[group_sorted['Year'] <= 2026]['SGI'], 
             color=color, linestyle='-', linewidth=1.5, alpha=0.4, zorder=1)
    
    # Draw historical footprints
    for _, p in past.iterrows():
        ax1.scatter(p['Γ2'], p['SGI'], s=p['Translation']*70, color=color, marker=marker, alpha=0.15, zorder=2)
        
    # Draw frozen current baseline (Mid-2026 Node)
    if not current.empty:
        c = current.iloc[0]
        # Opacity directly represents measurement confidence score
        confidence_alpha = c['Proxy_Confidence']
        ax1.scatter(c['Γ2'], c['SGI'], s=c['Translation']*120, color=color, marker=marker, 
                   edgecolor='#000000', linewidth=1.2, alpha=confidence_alpha, zorder=4)
        
        offset = 0.14 if ticker != 'STRIP' else -0.14
        v_align = 'bottom' if ticker != 'STRIP' else 'top'
        ax1.text(c['Γ2'], c['SGI'] + offset, c['Name'], fontsize=9, fontweight='bold', color='#1a252f', ha='center', va=v_align, zorder=5)

ax1.set_xlim(0.8, 5.5)
ax1.set_ylim(-0.4, 6.4)
ax1.set_xlabel('Measured Reachability Expansion (Γ₂)', fontsize=11, fontweight='bold', color='#111111')
ax1.set_ylabel('Measured Structural Gravity Index (SGI)', fontsize=11, fontweight='bold', color='#111111')
ax1.set_title('CHART 1: THE PURE OBSERVER ENGINE (STRICT ECOSYSTEM MEASUREMENTS)', fontsize=12, fontweight='bold', pad=20)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(True, linestyle=':', color='#e8e8e8', alpha=0.5)

plt.tight_layout()
ax1.figure.savefig('gamma_1_observation_engine.png')
plt.close(fig1)

# -------------------------------------------------------------------------
# CHART 2: THE EXPLANATORY FIELD ARCHITECTURE (THEORY SELECTION)
# -------------------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(12, 9), dpi=300)
fig2.patch.set_facecolor('#ffffff')
ax2.set_facecolor('#fdfdfd')

# Map analytical field quadrants for strategic categorization
ax2.axhline(3.0, color='#e2e8f0', linestyle='--', linewidth=1.2, zorder=1)
ax2.axvline(3.0, color='#e2e8f0', linestyle='--', linewidth=1.2, zorder=1)

ax2.text(1.5, 5.5, 'SYSTEMIC TOLLBOOTHS\n& BOTTLENECK LAYER\n(High Friction / Centralized Coercion)', fontsize=9, fontweight='semibold', color='#7f8c8d', ha='center')
ax2.text(4.5, 5.5, 'SUBSTRATE ENTERPRISES\n(Thermodynamic / Coordination Attractors)', fontsize=9, fontweight='semibold', color='#27ae60', ha='center')
ax2.text(1.5, 0.5, 'EXTRACTION ENDPOINTS\n(Terminal Capital Sinks)', fontsize=9, fontweight='semibold', color='#c0392b', ha='center')
ax2.text(4.5, 0.5, 'EMERGING ARCHITECTS\n(Unhardened Latent Option Space)', fontsize=9, fontweight='semibold', color='#d35400', ha='center')

# Map the active 2026 nodes overlaying hypothetical future vector forecasts
for ticker, group in df_clean.groupby('Ticker'):
    group_sorted = group.sort_values('Year')
    current = group_sorted[group_sorted['Year'] == 2026]
    future = group_sorted[group_sorted['Year'] == 2030]
    
    color = entity_colors.get(ticker, '#7f7f7f')
    marker = entity_markers.get(ticker, 'o')
    
    if not current.empty and not future.empty:
        c = current.iloc[0]
        f = future.iloc[0]
        
        # Display the strategic vector forecast link path
        ax2.plot([c['Γ2'], f['Γ2']], [c['SGI'], f['SGI']], color=color, linestyle='-.', linewidth=2.0, alpha=0.7, zorder=2)
        ax2.scatter(c['Γ2'], c['SGI'], s=140, color=color, marker=marker, edgecolor='#000000', linewidth=1.2, zorder=3)
        ax2.scatter(f['Γ2'], f['SGI'], s=100, facecolor='none', edgecolor=color, marker='*', linewidth=1.2, zorder=3)
        
        offset = 0.14 if ticker != 'STRIP' else -0.14
        v_align = 'bottom' if ticker != 'STRIP' else 'top'
        ax2.text(c['Γ2'], c['SGI'] + offset, ticker, fontsize=8, fontweight='bold', color='#34495e', ha='center', va=v_align)
        ax2.text(f['Γ2'] + 0.05, f['SGI'], '2030-P', fontsize=7, color=color, fontweight='bold', alpha=0.8, ha='left', va='center')

ax2.set_xlim(0.8, 5.5)
ax2.set_ylim(-0.4, 6.4)
ax2.set_xlabel('Hypothesized Attractor Space Expansion (Γ₂)', fontsize=11, fontweight='bold', color='#111111')
ax2.set_ylabel('Hypothesized Structural Field Gravity (SGI)', fontsize=11, fontweight='bold', color='#111111')
ax2.set_title('CHART 2: THE EXPLANATORY FIELD ARCHITECTURE (SELECTION HYPOTHESES)', fontsize=12, fontweight='bold', pad=20)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
ax2.figure.savefig('gamma_2_explanatory_field.png')
plt.close(fig2)

print("[*] Exclusion protocol executed successfully. Map assets exported: \n    1. gamma_1_observation_engine.png\n    2. gamma_2_explanatory_field.png")
