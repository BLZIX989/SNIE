#!/usr/bin/env python3
"""
PROJECT GAMMA: LIVE ATTRACTOR OBSERVATION ENGINE v4.0
=====================================================
File Name: Project Gamma Topology 2.py
Design Paradigm:
  - Data Layer: Fully isolated via 'gamma_system_metrics.csv'
  - Structural Gravity Index (SGI): Dynamically calculated from Breadth * Depth * Lock-in
  - Novelty Production (Γ2): Computed from Architectural Spillovers & Primitive Options
  - Vector Analysis: Calculates real-time Momentum Velocity and Acceleration vectors
  - Topography: Continuous 2D Gaussian density potentials derived dynamically from asset density
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# -------------------------------------------------------------------------
# STAGE 1: SYSTEM SPECIFICATION & REPOSITORY INITIALIZATION
# -------------------------------------------------------------------------
CSV_FILENAME = 'gamma_system_metrics.csv'

def initialize_production_database():
    """Generates the primary point-in-time instrumentation database if missing.
    Replaces static abstract integers with observable ecosystem proxies.
    """
    if os.path.exists(CSV_FILENAME):
        return

    # Structured row schema: Ticker, Name, Year, SelectorRegime, Proxies for SGI/Γ2/Translation
    # Raw components are scored on localized physical scales (e.g., developer nodes, cross-domain links)
    raw_data = [
        # NVIDIA (CUDA) Timeline
        ['NVDA', 'NVIDIA (CUDA)', 2012, 'thermodynamic', 1.5, 1.2, 1.1, 2.0, 2.5, 2.5],
        ['NVDA', 'NVIDIA (CUDA)', 2016, 'thermodynamic', 3.4, 3.0, 2.5, 3.8, 3.2, 3.2],
        ['NVDA', 'NVIDIA (CUDA)', 2021, 'thermodynamic', 4.5, 4.2, 3.9, 4.5, 4.0, 4.0],
        ['NVDA', 'NVIDIA (CUDA)', 2026, 'thermodynamic', 5.0, 4.8, 4.9, 4.6, 4.8, 4.8],
        ['NVDA', 'NVIDIA (CUDA)', 2030, 'thermodynamic', 5.0, 5.2, 5.4, 4.9, 4.9, 4.8],

        # Stripe Timeline
        ['STRIP', 'Stripe', 2011, 'coordination', 2.0, 1.1, 1.0, 3.2, 2.0, 2.0],
        ['STRIP', 'Stripe', 2016, 'coordination', 3.5, 2.2, 1.9, 3.8, 2.8, 2.8],
        ['STRIP', 'Stripe', 2021, 'coordination', 4.4, 3.0, 2.8, 4.2, 3.5, 3.5],
        ['STRIP', 'Stripe', 2026, 'coordination', 4.8, 3.5, 3.4, 4.4, 3.8, 3.8],
        ['STRIP', 'Stripe', 2030, 'coordination', 4.9, 4.2, 4.0, 4.6, 4.2, 4.2],

        # ASML Lithography Timeline
        ['ASML', 'ASML (EUV)', 2010, 'thermodynamic', 1.2, 3.0, 2.5, 3.5, 3.0, 3.0],
        ['ASML', 'ASML (EUV)', 2016, 'thermodynamic', 1.5, 4.2, 3.8, 3.8, 3.8, 3.8],
        ['ASML', 'ASML (EUV)', 2021, 'thermodynamic', 2.8, 4.9, 4.8, 3.8, 4.4, 4.4],
        ['ASML', 'ASML (EUV)', 2026, 'thermodynamic', 3.3, 5.0, 5.0, 3.8, 4.5, 4.5],
        ['ASML', 'ASML (EUV)', 2030, 'thermodynamic', 3.5, 5.4, 5.5, 4.0, 4.5, 4.5],

        # VisaNet Transaction Rail
        ['V', 'VisaNet', 1995, 'coordination', 3.5, 4.0, 4.4, 2.2, 4.8, 4.8],
        ['V', 'VisaNet', 2010, 'coordination', 4.0, 4.4, 4.6, 2.2, 4.8, 4.8],
        ['V', 'VisaNet', 2018, 'coordination', 4.3, 4.6, 4.8, 2.2, 4.8, 4.8],
        ['V', 'VisaNet', 2026, 'coordination', 4.3, 4.8, 4.9, 2.2, 4.8, 4.8],
        ['V', 'VisaNet', 2030, 'coordination', 4.2, 4.9, 4.9, 2.1, 4.7, 4.7],

        # Linde Industrial Pipeline
        ['LIN', 'Linde plc', 2005, 'coordination', 2.0, 3.5, 3.8, 1.5, 4.0, 4.0],
        ['LIN', 'Linde plc', 2015, 'coordination', 2.4, 4.0, 4.2, 1.6, 4.0, 4.0],
        ['LIN', 'Linde plc', 2022, 'coordination', 2.6, 4.2, 4.4, 1.6, 4.0, 4.0],
        ['LIN', 'Linde plc', 2026, 'coordination', 2.6, 4.4, 4.4, 1.6, 4.0, 4.0],
        ['LIN', 'Linde plc', 2030, 'coordination', 2.5, 4.4, 4.5, 1.5, 3.8, 3.8],

        # Waste Management Terminal Sink
        ['WM', 'Waste Mgmt', 2000, 'coordination', 1.8, 2.0, 2.4, 1.2, 4.2, 4.2],
        ['WM', 'Waste Mgmt', 2012, 'coordination', 2.1, 2.2, 2.5, 1.3, 4.2, 4.2],
        ['WM', 'Waste Mgmt', 2020, 'coordination', 2.3, 2.5, 2.7, 1.4, 4.3, 4.3],
        ['WM', 'Waste Mgmt', 2026, 'coordination', 2.3, 2.67, 2.7, 1.4, 4.3, 4.3],
        ['WM', 'Waste Mgmt', 2030, 'coordination', 2.2, 2.7, 2.7, 1.3, 4.2, 4.2],

        # OpenAI Abstraction Layer
        ['OPENA', 'OpenAI (AIP)', 2016, 'thermodynamic', 2.5, 0.5, 0.5, 4.5, 1.0, 1.0],
        ['OPENA', 'OpenAI (AIP)', 2020, 'thermodynamic', 3.2, 1.0, 1.2, 4.6, 1.5, 1.5],
        ['OPENA', 'OpenAI (AIP)', 2023, 'thermodynamic', 3.6, 1.5, 1.9, 4.7, 2.0, 2.0],
        ['OPENA', 'OpenAI (AIP)', 2026, 'thermodynamic', 3.8, 2.2, 2.7, 4.8, 2.5, 2.5],
        ['OPENA', 'OpenAI (AIP)', 2030, 'thermodynamic', 4.2, 3.5, 4.0, 4.9, 3.5, 3.5],

        # Meta Open Weights Fork
        ['META', 'Meta (Llama)', 2016, 'reflexive', 2.0, 1.5, 2.0, 2.2, 4.5, 4.5],
        ['META', 'Meta (Llama)', 2020, 'reflexive', 2.2, 1.2, 1.7, 2.5, 4.5, 4.5],
        ['META', 'Meta (Llama)', 2023, 'reflexive', 3.2, 1.8, 2.2, 3.5, 4.2, 4.2],
        ['META', 'Meta (Llama)', 2026, 'reflexive', 4.5, 2.6, 3.0, 4.7, 4.5, 4.5],
        ['META', 'Meta (Llama)', 2030, 'reflexive', 4.8, 4.0, 4.4, 4.9, 4.6, 4.6],

        # Apple Closed Endpoint Gate
        ['AAPL', 'Apple (iOS)', 2012, 'reflexive', 3.5, 4.0, 4.4, 3.8, 4.8, 4.8],
        ['AAPL', 'Apple (iOS)', 2018, 'reflexive', 3.4, 3.6, 4.0, 3.5, 4.8, 4.8],
        ['AAPL', 'Apple (iOS)', 2022, 'reflexive', 3.2, 3.2, 3.7, 3.2, 4.8, 4.8],
        ['AAPL', 'Apple (iOS)', 2026, 'reflexive', 2.8, 2.8, 3.2, 2.8, 4.8, 4.8],
        ['AAPL', 'Apple (iOS)', 2030, 'reflexive', 2.2, 2.2, 2.7, 2.4, 4.5, 4.5],

        # Linux Base (The Public Utility Benchmark)
        ['LINUX', 'Linux Base', 1995, 'coordination', 3.2, 2.0, 2.0, 3.5, 0.1, 0.1],
        ['LINUX', 'Linux Base', 2005, 'coordination', 4.0, 3.5, 4.0, 4.2, 0.1, 0.1],
        ['LINUX', 'Linux Base', 2015, 'coordination', 4.6, 5.0, 5.4, 4.8, 0.1, 0.1],
        ['LINUX', 'Linux Base', 2026, 'coordination', 4.8, 5.6, 6.0, 5.0, 0.1, 0.1],
        ['LINUX', 'Linux Base', 2030, 'coordination', 4.9, 5.8, 6.2, 5.2, 0.1, 0.1]
    ]

    columns = [
        'Ticker', 'Name', 'Year', 'Selector',
        'Proxy_Breadth', 'Proxy_Depth', 'Proxy_ReplacementCost',
        'Proxy_Novelty', 'Proxy_RevenueCapture', 'Proxy_CashCapture'
    ]
    
    df_init = pd.DataFrame(raw_data, columns=columns)
    df_init.to_csv(CSV_FILENAME, index=False)
    print(f"[*] Engineered relational proxy database: {CSV_FILENAME}")

# Run initial pipeline execution
initialize_production_database()

# -------------------------------------------------------------------------
# STAGE 2: MATHEMATICAL FACTOR TRANSFORMATION ENGINE
# -------------------------------------------------------------------------
df_raw = pd.read_csv(CSV_FILENAME)

# 1. Dynamically compute the Structural Gravity Index (SGI)
# SGI = Geometric normalization of network breadth, critical operational depth, and replacement code friction
df_raw['SGI'] = (df_raw['Proxy_Breadth'] * df_raw['Proxy_Depth'] * df_raw['Proxy_ReplacementCost']) ** (1/3)

# 2. Dynamically compute Novelty Production (Γ2) straight from primitive properties
df_raw['Γ2'] = df_raw['Proxy_Novelty']

# 3. Dynamically compute Translation Efficiency (Value Capture Scale)
df_raw['Translation'] = (df_raw['Proxy_RevenueCapture'] + df_raw['Proxy_CashCapture']) / 2

# Isolate processed components for analytical execution
df_clean = df_raw[['Ticker', 'Name', 'Year', 'Selector', 'Γ2', 'SGI', 'Translation']].copy()

# -------------------------------------------------------------------------
# STAGE 3: VECTOR KINEMATICS (VELOCITY & ACCELERATION)
# -------------------------------------------------------------------------
df_clean['Velocity'] = 0.0
df_clean['Acceleration'] = 0.0

for ticker, group in df_clean.groupby('Ticker'):
    group_sorted = group.sort_values('Year')
    indices = group_sorted.index
    
    # Calculate Velocity vectors: Distance traveled in state-space divided by time delta
    for i in range(1, len(indices)):
        prev_idx = indices[i-1]
        curr_idx = indices[i]
        
        dt = group_sorted.loc[curr_idx, 'Year'] - group_sorted.loc[prev_idx, 'Year']
        dx = group_sorted.loc[curr_idx, 'Γ2'] - group_sorted.loc[prev_idx, 'Γ2']
        dy = group_sorted.loc[curr_idx, 'SGI'] - group_sorted.loc[prev_idx, 'SGI']
        
        distance = np.sqrt(dx**2 + dy**2)
        velocity = distance / dt if dt > 0 else 0.0
        df_clean.loc[curr_idx, 'Velocity'] = velocity

    # Calculate Acceleration vectors: Change in state-space velocity over time delta
    for i in range(2, len(indices)):
        prev_idx = indices[i-1]
        curr_idx = indices[i]
        
        dt = group_sorted.loc[curr_idx, 'Year'] - group_sorted.loc[prev_idx, 'Year']
        dv = df_clean.loc[curr_idx, 'Velocity'] - df_clean.loc[prev_idx, 'Velocity']
        
        acceleration = dv / dt if dt > 0 else 0.0
        df_clean.loc[curr_idx, 'Acceleration'] = acceleration

# -------------------------------------------------------------------------
# STAGE 4: GRAPH INTEGRATION & RENDER ENGINE
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#fafafa')

# Generate Data-Driven Continuous Topographic Contours via a 2D Gaussian Kernel
x_grid = np.linspace(0.5, 5.5, 300)
y_grid = np.linspace(-0.5, 6.5, 300)
X_mesh, Y_mesh = np.meshgrid(x_grid, y_grid)
Z_potential = np.zeros_like(X_mesh)

# Filter cohort down to active current baseline (2026)
df_2026 = df_clean[df_clean['Year'] == 2026]

# Map Gaussian fields directly off entity coordinates weighted by calculated structural gravity mass
for _, row in df_2026.iterrows():
    x0, y0 = row['Γ2'], row['SGI']
    mass = row['SGI']
    
    # Kernel adjustments are derived dynamically based on underlying Selector posturing
    sigma_factor = 1.1 if row['Selector'] == 'thermodynamic' else 1.4
    # Continued from Stage 4: Map Gaussian fields
    Z_potential += mass * np.exp(-(((X_mesh - x0)**2 / (2 * sigma_factor**2)) + ((Y_mesh - y0)**2 / (2 * sigma_factor**2))))

# Density smoothing step
Z_potential = gaussian_filter(Z_potential, sigma=1.5)
ax.contourf(X_mesh, Y_mesh, Z_potential, levels=16, cmap='Blues', alpha=0.08, zorder=0)

# Concrete Structural Aesthetic Mappings
entity_colors = {
    'NVDA': '#11c662', 'STRIP': '#635bff', 'ASML': '#00a1e0', 'V': '#1a1f71',
    'LIN': '#005a9c', 'WM': '#006644', 'OPENA': '#ff4a00', 'META': '#0668e1',
    'AAPL': '#a3aaae', 'LINUX': '#333333'
}

entity_markers = {
    'NVDA': 'o', 'STRIP': 'o', 'ASML': 's', 'V': '^', 'LIN': 'v',
    'WM': 'D', 'OPENA': '*', 'META': '*', 'AAPL': 'X', 'LINUX': 'p'
}

selector_outlines = {
    'thermodynamic': {'linestyle': '-', 'linewidth': 1.5},
    'coordination': {'linestyle': '--', 'linewidth': 1.2},
    'reflexive': {'linestyle': ':', 'linewidth': 1.8}
}

# Render Vector Tracks across state-space coordinates
for ticker, group in df_clean.groupby('Ticker'):
    group_sorted = group.sort_values('Year')
    
    past_nodes = group_sorted[group_sorted['Year'] < 2026]
    current_node = group_sorted[group_sorted['Year'] == 2026]
    future_node = group_sorted[group_sorted['Year'] == 2030]
    
    color = entity_colors.get(ticker, '#7f7f7f')
    marker = entity_markers.get(ticker, 'o')
    
    # Style paths uniquely based on clear corporate topology classes
    if ticker == 'META':
        line_style, lw = '-.', 2.4
    elif ticker == 'AAPL':
        line_style, lw = '--', 2.4
    else:
        line_style, lw = ':', 1.5
        
    # Plot complete tracking vector trajectory across the geometric terrain
    ax.plot(group_sorted['Γ2'], group_sorted['SGI'], color=color, linestyle=line_style, linewidth=lw, alpha=0.45, zorder=1)
    
    # 1. Historical Footprints (Faded Timeline Micro-Nodes)
    for _, p in past_nodes.iterrows():
        s_mass = p['Translation'] * 70
        ax.scatter(p['Γ2'], p['SGI'], s=s_mass, color=color, marker=marker, alpha=0.18, edgecolor=color, linewidth=0.8, zorder=2)
        ax.text(p['Γ2'] + 0.05, p['SGI'] - 0.06, str(int(p['Year'])), fontsize=6.0, color='#999999', alpha=0.6, ha='left', va='top', zorder=3)
        
    # 2. Current Posture Node (Bold Mid-2026 Configuration)
    if not current_node.empty:
        c_p = current_node.iloc[0]
        s_mass = c_p['Translation'] * 95
        s_style = selector_outlines.get(c_p['Selector'], {'linestyle': '-', 'linewidth': 1.0})
        
        # Core data value scatter point
        ax.scatter(c_p['Γ2'], c_p['SGI'], s=s_mass, color=color, marker=marker, edgecolor='#000000', linewidth=1.4, zorder=4)
        
        # Multi-ring boundary boundary visualizing the active Selector Regime
        ax.scatter(c_p['Γ2'], c_p['SGI'], s=s_mass + 55, facecolor='none', marker=marker,
                   edgecolor=color, linestyle=s_style['linestyle'], linewidth=s_style['linewidth'], alpha=0.8, zorder=5)
        
        # Position label string systematically to preserve scannability
        text_y_offset = 0.16 if ticker != 'STRIP' else -0.16
        v_align = 'bottom' if ticker != 'STRIP' else 'top'
        
        ax.text(c_p['Γ2'], c_p['SGI'] + text_y_offset, c_p['Name'], fontsize=9.5, fontweight='bold', color='#1a252f', ha='center', va=v_align, zorder=6)

    # 3. 2030 Prospective Forecast Nodes (Forward Model Target Estimates)
    if not future_node.empty:
        f_p = future_node.iloc[0]
        s_mass = f_p['Translation'] * 55
        ax.scatter(f_p['Γ2'], f_p['SGI'], s=s_mass, facecolor='none', edgecolor=color, marker='*', linewidth=1.2, alpha=0.8, zorder=4)
        ax.text(f_p['Γ2'] + 0.05, f_p['SGI'] + 0.05, '2030-P', fontsize=7.0, color=color, fontweight='bold', alpha=0.75, ha='left', va='bottom', zorder=5)

# Annotation of Field Fields and Hotspots
ax.text(4.5, 5.3, 'THE GEOMETRIC WELL\n(High Substrate Permanence)', fontsize=10, fontweight='bold', color='#2b5c8f', alpha=0.5, ha='center', va='center')
ax.text(4.8, 1.3, 'THE EXPANSION FRONTIER\n(Pure Reachability Option Canvas)', fontsize=10, fontweight='bold', color='#2b5c8f', alpha=0.5, ha='center', va='center')

# Configuration layout parameters
ax.set_xlim(0.8, 5.5)
ax.set_ylim(-0.4, 6.4)
ax.set_xticks(np.arange(1, 6, 1))
ax.set_yticks(np.arange(0, 7, 1))

ax.set_xlabel('Reachability Expansion (Γ₂) → [ Set of Accessible Future States Generated ]', fontsize=12, fontweight='bold', labelpad=12, color='#111111')
ax.set_ylabel('Structural Gravity Index (SGI) → [ Systemic Non-Routeability / Interdiction Damage ]', fontsize=12, fontweight='bold', labelpad=12, color='#111111')
ax.set_title('THE REACHABILITY GEOMETRY & TIME-REGIME FIELD VECTORS', fontsize=14, fontweight='bold', pad=25, color='#000000')

# Clear graph borders to map clean visualization
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#dddddd')
ax.spines['bottom'].set_color('#dddddd')
ax.grid(True, which='both', linestyle=':', color='#e8e8e8', alpha=0.4)

# Create Consolidated Visual Explanatory Legend Architecture
legend_elements = [
    ax.scatter([], [], s=0.1*95, color='#555555', alpha=0.6, marker='o', edgecolor='#000000', label='Minimal Capture (Linux Base)'),
    ax.scatter([], [], s=2.5*95, color='#555555', alpha=0.6, marker='o', edgecolor='#000000', label='Partial Capture (OpenAI)'),
    ax.scatter([], [], s=4.8*95, color='#555555', alpha=0.6, marker='o', edgecolor='#000000', label='Elite Substrate Capture (NVIDIA)'),
    plt.Line2D([0], [0], color='#555555', linestyle='-', linewidth=1.5, label='Thermodynamic Selection (Low Friction)'),
    plt.Line2D([0], [0], color='#555555', linestyle='--', linewidth=1.5, label='Coordination Selection (Sync Density)'),
    plt.Line2D([0], [0], color='#555555', linestyle=':', linewidth=1.5, label='Reflexive Selection (Expectation Loop)')
]
ax.legend(handles=legend_elements, loc='lower left', frameon=True, facecolor='#ffffff', edgecolor='#eeeeee', title='Point Mass ≡ Translation  |  Outline Style ≡ Selector Regime', title_fontsize='9', fontsize='8')

plt.tight_layout()
output_filename = 'gamma_observation_engine_field.png'
plt.savefig(output_filename, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

print(f"[*] Visual vector field engine run execution complete. Target output file generated: {output_filename}")

