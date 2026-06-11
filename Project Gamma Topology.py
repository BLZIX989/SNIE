import matplotlib.pyplot as plt
import numpy as np

# Set pristine font parameter strings
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# Define historical trajectory states for each archetype: [(x, y, translation, label_year)]
# Mapping Position + Velocity + Direction across multi-year structural regime shifts
historical_vectors = {
    'NVIDIA (CUDA)': {
        'path': [(2.0, 1.2, 2.5, '2012'), (3.2, 2.0, 3.2, '2016'), (4.2, 3.5, 4.0, '2021'), (4.8, 4.67, 4.8, '2026')],
        'color': '#11c662', 'marker': 'o'
    },
    'Stripe': {
        'path': [(3.2, 1.0, 2.0, '2011'), (3.8, 2.1, 2.8, '2016'), (4.2, 2.9, 3.5, '2021'), (4.4, 3.45, 3.8, '2026')],
        'color': '#635bff', 'marker': 'o'
    },
    'ASML (EUV)': {
        'path': [(1.8, 2.5, 3.0, '2010'), (2.6, 3.2, 3.8, '2016'), (3.4, 4.2, 4.4, '2021'), (3.8, 5.00, 4.5, '2026')],
        'color': '#00a1e0', 'marker': 's'
    },
    'VisaNet': {
        'path': [(2.0, 4.2, 4.8, '1995'), (2.1, 4.5, 4.8, '2010'), (2.2, 4.7, 4.8, '2018'), (2.2, 4.83, 4.8, '2026')],
        'color': '#1a1f71', 'marker': '^'
    },
    'Linde plc': {
        'path': [(1.5, 3.8, 4.0, '2005'), (1.6, 4.1, 4.0, '2015'), (1.6, 4.3, 4.0, '2022'), (1.6, 4.40, 4.0, '2026')],
        'color': '#005a9c', 'marker': 'v'
    },
    'Waste Mgmt': {
        'path': [(1.2, 2.2, 4.2, '2000'), (1.3, 2.4, 4.2, '2012'), (1.4, 2.6, 4.3, '2020'), (1.4, 2.67, 4.3, '2026')],
        'color': '#006644', 'marker': 'D'
    },
    'OpenAI (AIP)': {
        'path': [(4.5, 0.5, 1.0, '2016'), (4.6, 1.2, 1.5, '2020'), (4.7, 1.8, 2.0, '2023'), (4.8, 2.50, 2.5, '2026')],
        'color': '#ff4a00', 'marker': '*'
    },
    'Meta (Llama)': {
        'path': [(2.2, 1.8, 4.5, '2016'), (2.5, 1.5, 4.5, '2020'), (3.5, 2.0, 4.2, '2023'), (4.7, 2.80, 4.5, '2026')],
        'color': '#0668e1', 'marker': '*'
    },
    'Apple (iOS)': {
        'path': [(3.8, 4.2, 4.8, '2012'), (3.5, 3.8, 4.8, '2018'), (3.2, 3.5, 4.8, '2022'), (2.8, 3.00, 4.8, '2026')],
        'color': '#a3aaae', 'marker': 'X'
    },
    'Linux Base': {
        'path': [(3.5, 2.0, 0.1, '1995'), (4.2, 3.8, 0.1, '2005'), (4.8, 5.2, 0.1, '2015'), (5.0, 5.80, 0.1, '2026')],
        'color': '#333333', 'marker': 'p'
    }
}

fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#fafafa')

# 1. Generate Continuous Topographic Gravitational Contours (Attractor Potential Wells)
# Rather than rigid quadrant grids, we treat space as a continuous vector field
x_grid = np.linspace(0.5, 5.5, 200)
y_grid = np.linspace(-0.5, 6.5, 200)
X_mesh, Y_mesh = np.meshgrid(x_grid, y_grid)

# Define continuous mathematical fields tracking "Gravity Wells" and "Frontiers"
Z_gravity = np.exp(-((X_mesh - 4.5)**2 / 2.0 + (Y_mesh - 5.0)**2 / 1.5)) * 0.7
Z_frontier = np.exp(-((X_mesh - 4.8)**2 / 1.5 + (Y_mesh - 2.0)**2 / 2.0)) * 0.4
Z_total = Z_gravity + Z_frontier

# Map background contours using subtle structural shifts
contour = ax.contourf(X_mesh, Y_mesh, Z_total, levels=12, cmap='Blues', alpha=0.08, zorder=0)

# 2. Render Trajectory Vectors and Timeline Micro-Nodes
for entity, data in historical_vectors.items():
    pts = data['path']
    x_coords = [p[0] for p in pts]
    y_coords = [p[1] for p in pts]
    sizes = [p[2] * 70 for p in pts]  # Circle volume corresponds directly to Value Capture
    
    # Draw line curves showing historical momentum trajectory
    if entity == 'Meta (Llama)':
        ax.plot(x_coords, y_coords, color=data['color'], linestyle='-.', linewidth=2.5, alpha=0.7, zorder=2)
    elif entity == 'Apple (iOS)':
        ax.plot(x_coords, y_coords, color=data['color'], linestyle='--', linewidth=2.5, alpha=0.7, zorder=2)
    else:
        ax.plot(x_coords, y_coords, color=data['color'], linestyle=':', linewidth=2.0, alpha=0.5, zorder=2)
        
    # Draw historical temporal data points along the vector timeline path
    for i, p in enumerate(pts[:-1]):
        ax.scatter(p[0], p[1], s=sizes[i], color=data['color'], marker=data['marker'], alpha=0.25, edgecolor=data['color'], linewidth=1.0, zorder=3)
        if i % 2 == 0 or i == len(pts)-2: # Suppress label clutter
            ax.text(p[0] + 0.06, p[1] - 0.06, p[3], fontsize=7, color='#777777', alpha=0.7, zorder=4, ha='left', va='top')
            
    # Draw Final Point Representation (Mid-2026 Frozen Coordinates)
    final_p = pts[-1]
    final_size = final_p[2] * 85 # Highlight active current state scale volume
    ax.scatter(final_p[0], final_p[1], s=final_size, color=data['color'], marker=data['marker'], edgecolor='#000000', linewidth=1.3, zorder=5)
    
    # Specific layout configurations to optimize micro-label visibility
    v_adjust = 0.16 if entity != 'Stripe' else -0.16
    v_align = 'bottom' if entity != 'Stripe' else 'top'
    ax.text(final_p[0], final_p[1] + v_adjust, entity, fontsize=9.5, fontweight='bold', color='#1a252f', ha='center', va=v_align, zorder=6)

# 3. Annotate Field Contour Hotspots
ax.text(4.5, 5.2, 'THE GEOMETRIC WELL\n(High Substrate Permanence)', fontsize=10, fontweight='bold', color='#2b5c8f', alpha=0.6, ha='center', va='center')
ax.text(4.8, 1.4, 'THE EXPANSION FRONTIER\n(Pure Reachability Option Canvas)', fontsize=10, fontweight='bold', color='#2b5c8f', alpha=0.6, ha='center', va='center')

# Configure axis scaling, layout, and descriptions
ax.set_xlim(0.8, 5.4)
ax.set_ylim(-0.4, 6.4)
ax.set_xticks(np.arange(1, 6, 1))
ax.set_yticks(np.arange(0, 7, 1))

ax.set_xlabel('Reachability Expansion (Γ₂) → [ Set of Accessible Future States Generated ]', fontsize=12, fontweight='bold', labelpad=12, color='#111111')
ax.set_ylabel('Structural Gravity Index (SGI) → [ Systemic Non-Routeability / Interdiction Damage ]', fontsize=12, fontweight='bold', labelpad=12, color='#111111')
ax.set_title('THE REACHABILITY GEOMETRY & TIME-REGIME FIELD VECTORS', fontsize=14, fontweight='bold', pad=25, color='#000000')

# Polish aesthetic borders to enhance content scannability
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#dddddd')
ax.spines['bottom'].set_color('#dddddd')
ax.grid(True, which='both', linestyle=':', color='#e8e8e8', alpha=0.4)

# Render explicit visual legend anchor detailing point size translation logic
legend_sizes = [0.5 * 85, 2.5 * 85, 4.8 * 85]
legend_labels = ['Minimal Capture (Linux Base)', 'Partial Platform Capture (OpenAI)', 'Elite Substrate Capture (NVIDIA)']
for s, l in zip(legend_sizes, legend_labels):
    ax.scatter([], [], s=s, color='#7f7f7f', alpha=0.6, marker='o', edgecolor='#000000', label=l)
ax.legend(scatterpoints=1, loc='lower left', frameon=True, facecolor='#ffffff', edgecolor='#eeeeee', title='Point Mass Scale ≡ Translation Efficiency (Value Capture)', title_fontsize='9', fontsize='8')

plt.tight_layout()
plt.savefig('gamma_vector_field_landscape.png', facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
