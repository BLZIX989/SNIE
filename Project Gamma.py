import matplotlib.pyplot as plt
import numpy as np

# Set aesthetic styling parameters
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# Define coordinate matrices for the frozen 2026 Core Archetypes
archetypes = {
    'NVIDIA (CUDA)': {'x': 4.8, 'y': 4.67, 'color': '#11c662', 'marker': 'o', 'path': 'hybrid'},
    'Stripe': {'x': 4.4, 'y': 3.45, 'color': '#635bff', 'marker': 'o', 'path': 'software'},
    'ASML (EUV)': {'x': 3.8, 'y': 5.00, 'color': '#00a1e0', 'marker': 's', 'path': 'physical'},
    'VisaNet': {'x': 2.2, 'y': 4.83, 'color': '#1a1f71', 'marker': '^', 'path': 'tollbooth'},
    'Linde plc': {'x': 1.6, 'y': 4.40, 'color': '#005a9c', 'marker': 'v', 'path': 'bottleneck'},
    'Waste Mgmt': {'x': 1.4, 'y': 2.67, 'color': '#006644', 'marker': 'D', 'path': 'extractor'},
    'OpenAI (AIP)': {'x': 4.8, 'y': 2.50, 'color': '#ff4a00', 'marker': '*', 'path': 'architect'},
    'Meta (Llama)': {'x': 4.7, 'y': 2.80, 'color': '#0668e1', 'marker': '*', 'path': 'meta_fork'},
    'Apple (iOS Gate)': {'x': 2.8, 'y': 3.00, 'color': '#a3aaae', 'marker': 'X', 'path': 'apple_decay'},
    'QWERTY Standard': {'x': 1.1, 'y': 4.10, 'color': '#7f7f7f', 'marker': 'p', 'path': 'legacy'}
}

fig, ax = plt.subplots(figsize=(13, 9), dpi=300)
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#fcfcfc')

# Draw evolutionary boundary zones and quadrants
ax.axhline(3.0, color='#e5e5e5', linestyle='--', linewidth=1.2, zorder=1)
ax.axvline(3.0, color='#e5e5e5', linestyle='--', linewidth=1.2, zorder=1)

# Annotate landscape quadrants using systemic definitions
ax.text(1.2, 5.7, 'LEGACY ANCHORS\n(Ghost Constraints / Trailing Friction)', fontsize=10, fontweight='bold', color='#7f7f7f', alpha=0.8, ha='center', va='center')
ax.text(4.2, 5.7, 'FULL SUBSTRATE WINNERS\n(Thermodynamic / Coordination Attraction)', fontsize=10, fontweight='bold', color='#11c662', alpha=0.8, ha='center', va='center')
ax.text(1.2, 0.4, 'EXTRACTION ENDPOINTS\n(Terminal Value Sinks)', fontsize=10, fontweight='bold', color='#006644', alpha=0.8, ha='center', va='center')
ax.text(4.2, 0.4, 'EMERGING ARCHITECTS\n(Latent Reachability / Unhardened Option Space)', fontsize=10, fontweight='bold', color='#ff4a00', alpha=0.8, ha='center', va='center')

# Plot vector trajectories mapping evolutionary tracks and paradigm shifts
# 1. The Software Platform Path (Stripe)
x_str = np.linspace(3.0, 4.4, 50)
y_str = 1.0 + 1.2 * (x_str - 3.0) + 0.3 * (x_str - 3.0)**2
ax.plot(x_str, y_str, color='#635bff', linestyle=':', linewidth=2, alpha=0.6, zorder=2)

# 2. The Physical Substrate Path (ASML)
x_asml = np.linspace(1.5, 3.8, 50)
y_asml = 2.5 + 0.8 * (x_asml - 1.5) + 0.2 * (x_asml - 1.5)**2
ax.plot(x_asml, y_asml, color='#00a1e0', linestyle=':', linewidth=2, alpha=0.6, zorder=2)

# 3. The Meta Open-Weight Fork (Meta shifting from Extractor to Substrate)
x_meta = np.linspace(2.0, 4.7, 50)
y_meta = 0.5 + 0.5 * (x_meta - 2.0) + 0.1 * (x_meta - 2.0)**2
ax.plot(x_meta, y_meta, color='#0668e1', linestyle='-.', linewidth=2.5, alpha=0.7, zorder=2)
ax.annotate('', xy=(4.7, 2.8), xytext=(3.5, 1.5), arrowprops=dict(arrowstyle="->", color='#0668e1', lw=2.5, ls='-.', connectionstyle="arc3,rad=-0.1"))

# 4. The Apple Abstraction Decay (Apple slipping down and left as intelligence abstracts endpoints)
x_appl = np.linspace(3.5, 2.8, 50)
y_appl = 4.0 - 0.7 * (3.5 - x_appl) - 0.4 * (3.5 - x_appl)**2
color = archetypes['Apple (iOS Gate)']["color"]

ax.plot(
    x_appl,
    y_appl,
    color=color,
    linewidth=3,
    alpha=0.8,
    zorder=3
)
ax.annotate('', xy=(2.8, 3.0), xytext=(3.3, 3.6), arrowprops=dict(arrowstyle="->", color='#a3aaae', lw=2.5, ls='--'))

# Plot static point positions for locked mid-2026 data coordinates
for name, data in archetypes.items():
    ax.scatter(data['x'], data['y'], color=data['color'], marker=data['marker'], s=180, edgecolor='#000000', linewidth=1.2, label=name, zorder=5)
    ax.text(data['x'], data['y'] + 0.14, name, fontsize=9, fontweight='semibold', color='#2c3e50', ha='center', va='bottom', zorder=6)

# Configure axis scaling, labels, and geometric titles
ax.set_xlim(0.8, 5.2)
ax.set_ylim(-0.2, 6.2)
ax.set_xticks(np.arange(1, 6, 1))
ax.set_yticks(np.arange(0, 7, 1))

ax.set_xlabel('Reachability Expansion (Γ₂) → [ Set of Accessible Future States ]', fontsize=12, fontweight='bold', labelpad=12, color='#222222')
ax.set_ylabel('Structural Gravity Index (SGI) → [ Systemic Interdiction / Non-Routeability ]', fontsize=12, fontweight='bold', labelpad=12, color='#222222')
ax.set_title('THE REACHABILITY GEOMETRY & EVOLUTIONARY ATTRACTOR LANDSPACE', fontsize=14, fontweight='bold', pad=20, color='#111111')

# Clean up graph borders to emphasize data layout
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.grid(True, which='both', linestyle=':', color='#f0f0f0', alpha=0.5)

plt.tight_layout()
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(
    script_dir,
    "gamma_reachability_landscape.png"
)

plt.savefig(
    output_path,
    facecolor=fig.get_facecolor(),
    edgecolor='none'
)
plt.close()
