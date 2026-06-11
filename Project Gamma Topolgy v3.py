#!/usr/bin/env python3
"""
PROJECT GAMMA: SYSTEMIC ATTRACTOR OBSERVATION ENGINE v3.0
=========================================================
File Name: Project Gamma Topology 2.py
Core Design:
  - X-Axis: Reachability Expansion (Γ₂)
  - Y-Axis: Structural Gravity Index (SGI)
  - Point Mass Size: Translation Efficiency (Value Capture Scale)
  - Node Outlines: Selector Regime (Thermodynamic, Coordination, Reflexive)
  - Field Contours: Emergent Density via Data-Driven Gaussian Kernel
  - Vector Tracks: Historical Realities (Faded) -> Current State (Bold) -> 2030 Projections (Star)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------
# STAGE 1: ISOLATED SYSTEM DATABASE INGESTION LAYER
# -------------------------------------------------------------------------
CSV_FILENAME = 'gamma_system_metrics.csv'

def initialize_database():
    """Generates the standardized data stack directly if missing."""
    csv_payload = """Ticker,Name,Year,Γ2,SGI,Translation,Selector
NVDA,NVIDIA (CUDA),2012,2.0,1.2,2.5,thermodynamic
NVDA,NVIDIA (CUDA),2016,3.2,2.0,3.2,thermodynamic
NVDA,NVIDIA (CUDA),2021,4.2,3.5,4.0,thermodynamic
NVDA,NVIDIA (CUDA),2026,4.8,4.67,4.8,thermodynamic
NVDA,NVIDIA (CUDA),2030,5.1,5.2,4.8,thermodynamic
STRIP,Stripe,2011,3.2,1.0,2.0,coordination
STRIP,Stripe,2016,3.8,2.1,2.8,coordination
STRIP,Stripe,2021,4.2,2.9,3.5,coordination
STRIP,Stripe,2026,4.4,3.45,3.8,coordination
STRIP,Stripe,2030,4.6,4.0,4.2,coordination
ASML,ASML (EUV),2010,1.8,2.5,3.0,thermodynamic
ASML,ASML (EUV),2016,2.6,3.2,3.8,thermodynamic
ASML,ASML (EUV),2021,3.4,4.2,4.4,thermodynamic
ASML,ASML (EUV),2026,3.8,5.0,4.5,thermodynamic
ASML,ASML (EUV),2030,4.0,5.5,4.5,thermodynamic
V,VisaNet,1995,2.0,4.2,4.8,coordination
V,VisaNet,2010,2.1,4.5,4.8,coordination
V,VisaNet,2018,2.2,4.7,4.8,coordination
V,VisaNet,2026,2.2,4.83,4.8,coordination
V,VisaNet,2030,2.1,4.9,4.7,coordination
LIN,Linde plc,2005,1.5,3.8,4.0,coordination
LIN,Linde plc,2015,1.6,4.1,4.0,coordination
LIN,Linde plc,2022,1.6,4.3,4.0,coordination
LIN,Linde plc,2026,1.6,4.4,4.0,coordination
LIN,Linde plc,2030,1.5,4.45,3.8,coordination
WM,Waste Mgmt,2000,1.2,2.2,4.2,coordination
WM,Waste Mgmt,2012,1.3,2.4,4.2,coordination
WM,Waste Mgmt,2020,1.4,2.6,4.3,coordination
WM,Waste Mgmt,2026,1.4,2.67,4.3,coordination
WM,Waste Mgmt,2030,1.3,2.7,4.2,coordination
OPENA,OpenAI (AIP),2016,4.5,0.5,1.0,thermodynamic
OPENA,OpenAI (AIP),2020,4.6,1.2,1.5,thermodynamic
OPENA,OpenAI (AIP),2023,4.7,1.8,2.0,thermodynamic
OPENA,OpenAI (AIP),2026,4.8,2.5,2.5,thermodynamic
OPENA,OpenAI (AIP),2030,4.9,3.8,3.5,thermodynamic
META,Meta (Llama),2016,2.2,1.8,4.5,reflexive
META,Meta (Llama),2020,2.5,1.5,4.5,reflexive
META,Meta (Llama),2023,3.5,2.0,4.2,reflexive
META,Meta (Llama),2026,4.7,2.8,4.5,reflexive
META,Meta (Llama),2030,4.9,4.2,4.6,reflexive
AAPL,Apple (iOS),2012,3.8,4.2,4.8,reflexive
AAPL,Apple (iOS),2018,3.5,3.8,4.8,reflexive
AAPL,Apple (iOS),2022,3.2,3.5,4.8,reflexive
AAPL,Apple (iOS),2026,2.8,3.0,4.8,reflexive
AAPL,Apple (iOS),2030,2.4,2.5,4.5,reflexive
LINUX,Linux Base,1995,3.5,2.0,0.1,coordination
LINUX,Linux Base,2005,4.2,3.8,0.1,coordination
LINUX,Linux Base,2015,4.8,5.2,0.1,coordination
LINUX,Linux Base,2026,5.0,5.8,0.1,coordination
LINUX,Linux Base,2030,5.2,6.0,0.1,coordination"""
    
    if not os.path.exists(CSV_FILENAME):
        with open(CSV_FILENAME, 'w', encoding='utf-8') as f:
            f.write(csv_payload.strip())
        print(f"[*] Initialized flat-file repository: {CSV_FILENAME}")

# Execute isolation check
initialize_database()
df = pd.read_csv(CSV_FILENAME)

# Normalize the current repository schema into the plotting columns this
# script expects. Older CSVs only store proxy fields, so derive the plotting
# metrics when needed instead of failing on a missing column.
if 'SGI' not in df.columns:
    df['SGI'] = (df['Proxy_Breadth'] * df['Proxy_Depth'] * df['Proxy_ReplacementCost']) ** (1 / 3)

if 'Γ2' not in df.columns:
    df['Γ2'] = df['Proxy_Novelty']

if 'Translation' not in df.columns:
    df['Translation'] = (df['Proxy_RevenueCapture'] + df['Proxy_CashCapture']) / 2

# -------------------------------------------------------------------------
# STAGE 2: RENDER SYSTEM CANVAS AND ENHANCED GEOMETRY
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#fafafa')

# Esthetic font mapping configurations
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# -- STROKE LAYER 1: DATA-DRIVEN EMERGING POTENTIAL WELL CONTOURS --
x_space = np.linspace(0.5, 5.5, 250)
y_space = np.linspace(-0.5, 6.5, 250)
X_mesh, Y_mesh = np.meshgrid(x_space, y_space)
Z_field = np.zeros_like(X_mesh)

# Extract only the frozen current baseline coordinates (2026) to generate vectors
df_2026 = df[df['Year'] == 2026]

# Calculate continuous Gaussian density weights dynamically derived from actual entity locations
for _, row in df_2026.iterrows():
    # Structural SGI height directly dictates the potential well density mass footprint
    mass = row['SGI']
    x0, y0 = row['Γ2'], row['SGI']
    
    # Calculate geometric kernel widths based on structural classification metrics
    x_sigma = 1.2 if row['Selector'] == 'thermodynamic' else 1.5
    y_sigma = 1.0 if row['Selector'] == 'thermodynamic' else 1.3
    
    Z_field += mass * np.exp(-(((X_mesh - x0)**2 / (2 * x_sigma**2)) + ((Y_mesh - y0)**2 / (2 * y_sigma**2))))

# Map topological structural contours smoothly onto the canvas background
ax.contourf(X_mesh, Y_mesh, Z_field, levels=14, cmap='Blues', alpha=0.07, zorder=0)

# Color and Stroke Mapping Rule Engine for Archetypes and Selector Regimes
archetype_colors = {
    'NVDA': '#11c662', 'STRIP': '#635bff', 'ASML': '#00a1e0', 'V': '#1a1f71',
    'LIN': '#005a9c', 'WM': '#006644', 'OPENA': '#ff4a00', 'META': '#0668e1',
    'AAPL': '#a3aaae', 'LINUX': '#333333'
}

archetype_markers = {
    'NVDA': 'o', 'STRIP': 'o', 'ASML': 's', 'V': '^', 'LIN': 'v',
    'WM': 'D', 'OPENA': '*', 'META': '*', 'AAPL': 'X', 'LINUX': 'p'
}

selector_styles = {
    'thermodynamic': {'linestyle': '-', 'linewidth': 1.4},   # Solid Outline
    'coordination': {'linestyle': '--', 'linewidth': 1.2},   # Dashed Outline
    'reflexive': {'linestyle': ':', 'linewidth': 1.6}        # Dotted Outline
}

# -- STROKE LAYER 2: CHRONO-VECTOR REGIME TRACKS & TIMELINE NODES --
grouped = df.groupby('Ticker')

for ticker, group in grouped:
    group_sorted = group.sort_values('Year')
    
    # Filter nodes into explicit temporal tranches
    past_nodes = group_sorted[group_sorted['Year'] < 2026]
    current_node = group_sorted[group_sorted['Year'] == 2026]
    future_node = group_sorted[group_sorted['Year'] == 2030]
    
    color = archetype_colors.get(ticker, '#7f7f7f')
    marker = archetype_markers.get(ticker, 'o')
    
    # Check trace style variations based on topological alignment
    if ticker == 'META':
        line_style = '-.'
        line_width = 2.2
    elif ticker == 'AAPL':
        line_style = '--'
        line_width = 2.2
    else:
        line_style = ':'
        line_width = 1.6
        
    # Plot Trailing and Prospective Line Vectors concurrently across the canvas
    ax.plot(group_sorted['Γ2'], group_sorted['SGI'], color=color, linestyle=line_style, linewidth=line_width, alpha=0.5, zorder=1)
    
    # A. Draw Faded Chrono-Nodes (Historical Footprints)
    for _, p in past_nodes.iterrows():
        size_mass = p['Translation'] * 75
        ax.scatter(p['Γ2'], p['SGI'], s=size_mass, color=color, marker=marker, alpha=0.20, edgecolor=color, linewidth=0.8, zorder=2)
        ax.text(p['Γ2'] + 0.05, p['SGI'] - 0.05, str(int(p['Year'])), fontsize=6.5, color='#888888', alpha=0.6, ha='left', va='top', zorder=3)
        
    # B. Draw Current State Node (Mid-2026 Frozen Structural Configuration)
    if not current_node.empty:
        c_p = current_node.iloc[0]
        size_mass = c_p['Translation'] * 95 # Volumetric sizing reflects Translation Efficiency
        selector = c_p['Selector']
        s_style = selector_styles.get(selector, {'linestyle': '-', 'linewidth': 1.0})
        
        # Build multi-ring outline to map the Selector Regime parameters explicitly
        ax.scatter(c_p['Γ2'], c_p['SGI'], s=size_mass, color=color, marker=marker, edgecolor='#000000', linewidth=1.4, zorder=4)
        
        # Overlay standard selector style layer ring boundary
        ax.scatter(c_p['Γ2'], c_p['SGI'], s=size_mass + 50, facecolor='none', marker=marker, 
                   edgecolor=color, linestyle=s_style['linestyle'], linewidth=s_style['linewidth'], alpha=0.8, zorder=5)
        
        # Handle custom text offsets to maintain clean grid scannability
        y_offset = 0.16 if ticker != 'STRIP' else -0.16
        v_align = 'bottom' if ticker != 'STRIP' else 'top'
        ax.text(c_p['Γ2'], c_p['SGI'] + y_offset, c_p['Name'], fontsize=9.5, fontweight='bold', color='#1c2833', ha='center', va=v_align, zorder=6)

    # C. Draw Star Target Nodes (2030 Predictive Modeling Vectors)
    if not future_node.empty:
        f_p = future_node.iloc[0]
        size_mass = f_p['Translation'] * 55
        # 2030 Prospective points are highlighted using a standardized forward execution indicator marker
        ax.scatter(f_p['Γ2'], f_p['SGI'], s=size_mass, facecolor='none', edgecolor=color, marker='*', linewidth=1.2, alpha=0.75, zorder=4)
        ax.text(f_p['Γ2'] + 0.05, f_p['SGI'] + 0.05, '2030-P', fontsize=7, color=color, fontweight='semibold', alpha=0.8, ha='left', va='bottom', zorder=5)

# -- STROKE LAYER 3: CONTEXTUAL INFRASTRUCTURE PROPERTY SIGNALS --
ax.text(1.2, 5.8, 'LEGACY ANCHORS\n(Ghost Constraints / High Friction)', fontsize=10, fontweight='bold', color='#7f7f7f', alpha=0.7, ha='center', va='center')
ax.text(4.6, 5.8, 'FULL SUBSTRATE WINNERS\n(Thermodynamic Attractor Core)', fontsize=10, fontweight='bold', color='#2b5c8f', alpha=0.7, ha='center', va='center')
ax.text(1.2, 0.2, 'EXTRACTION ENDPOINTS\n(Terminal Value Sinks)', fontsize=10, fontweight='bold', color='#006644', alpha=0.7, ha='center', va='center')
ax.text(4.6, 0.2, 'THE EXPANSION FRONTIER\n(Pure Reachability Options Canvas)', fontsize=10, fontweight='bold', color='#ff4a00', alpha=0.7, ha='center', va='center')

# Final canvas framing and export.
ax.set_xlim(0.8, 5.4)
ax.set_ylim(-0.4, 6.4)
ax.set_xticks(np.arange(1, 6, 1))
ax.set_yticks(np.arange(0, 7, 1))

ax.set_xlabel('Reachability Expansion (Γ₂) → [ Set of Accessible Future States Generated ]', fontsize=12, fontweight='bold', labelpad=12, color='#111111')
ax.set_ylabel('Structural Gravity Index (SGI) → [ Systemic Non-Routeability / Interdiction Damage ]', fontsize=12, fontweight='bold', labelpad=12, color='#111111')
ax.set_title('THE REACHABILITY GEOMETRY & EVOLUTIONARY ATTRACTOR LANDSCAPE', fontsize=14, fontweight='bold', pad=25, color='#000000')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#dddddd')
ax.spines['bottom'].set_color('#dddddd')
ax.grid(True, which='both', linestyle=':', color='#e8e8e8', alpha=0.4)

legend_elements = [
    plt.Line2D([0], [0], color='#555555', linestyle='-', linewidth=1.5, label='Thermodynamic Selection (Low Friction)'),
    plt.Line2D([0], [0], color='#555555', linestyle='--', linewidth=1.5, label='Coordination Selection (Sync Density)'),
    plt.Line2D([0], [0], color='#555555', linestyle=':', linewidth=1.5, label='Reflexive Selection (Expectation Loop)')
]
ax.legend(handles=legend_elements, loc='lower left', frameon=True, facecolor='#ffffff', edgecolor='#eeeeee', title='Point Mass ≡ Translation  |  Outline Style ≡ Selector Regime', title_fontsize='9', fontsize='8')

plt.tight_layout()
output_filename = 'gamma_reachability_landscape.png'
plt.savefig(output_filename, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

print(f"[*] Visual vector field engine run execution complete. Target output file generated: {output_filename}")

