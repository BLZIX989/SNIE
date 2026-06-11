import os
import sys
import pandas as pd
from tabulate import tabulate

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "snie_tech.csv")

CLR_RESET = "\033[0m"
CLR_GREEN = "\033[32m"
CLR_CYAN  = "\033[36m"
CLR_YELLOW = "\033[33m"
CLR_WHITE = "\033[37m"
CLR_RED_BOLD = "\033[1;31m"

def load_tech_universe():
    if not os.path.exists(CSV_PATH):
        print(f"[!] Error: Technology data file missing at: {CSV_PATH}")
        sys.exit(1)
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()
    return df

def min_max_scale(series, invert=False):
    if series.max() == series.min(): return series * 0 + 50
    scaled = ((series - series.min()) / (series.max() - series.min())) * 100
    return 100.0 - scaled if invert else scaled

def evaluate_technology_states():
    df = load_tech_universe()
    
    # 1. Calculate Gamma_2 (Possibility Expansion)
    # Rewards low cost of entry, high patent network citations
    entry_inverted = min_max_scale(df["Cost_To_Entry"], invert=True)
    citations_scaled = min_max_scale(df["Patent_Citations"])
    df["Gamma_2"] = (entry_inverted * 0.5) + (citations_scaled * 0.5)
    
    # 2. Calculate Invariance (Static Environmental Robustness)
    # Rewards thermal envelope, abundance, punishes regulatory bans
    thermal_scaled = min_max_scale(df["Thermal_Envelope"])
    abundance_scaled = min_max_scale(df["Crustal_Abundance"])
    bans_inverted = min_max_scale(df["Regulatory_Bans"], invert=True)
    df["Invariance"] = (thermal_scaled * 0.3) + (abundance_scaled * 0.4) + (bans_inverted * 0.3)
    
    # 3. Calculate dI/dt (Discovery/Improvement Velocity Trajectory)
    # Blends learning curve slopes, error decay, and raw performance gains
    slope_scaled = min_max_scale(df["Learning_Slope"])
    decay_scaled = min_max_scale(df["Error_Decay"])
    gain_scaled = min_max_scale(df["Net_Gain"])
    df["dI_dt"] = (slope_scaled * 0.4) + (decay_scaled * 0.3) + (gain_scaled * 0.3)
    
    # 4. Calculate Density (Real-world Embeddedness Layer)
    # Measures physical capital spend, deployed systems, and labor depth
    capex_scaled = min_max_scale(df["CapEx_Millions"])
    systems_scaled = min_max_scale(df["Systems_Deployed"])
    engineers_scaled = min_max_scale(df["Engineers_Count"])
    df["Density"] = (capex_scaled * 0.4) + (systems_scaled * 0.3) + (engineers_scaled * 0.3)
    
    ui_rows = []
    for _, r in df.iterrows():
        tech = r["Technology"]
        g2, inv, didt, den = float(r["Gamma_2"]), float(r["Invariance"]), float(r["dI_dt"]), float(r["Density"])
        
        # Dynamic State Machine Phase-Transition Threshold Logic
        if g2 >= 60.0 and den < 25.0:
            state = "FRONTIER STATE"
            color = CLR_YELLOW
        elif g2 >= 50.0 and didt >= 45.0 and den >= 25.0:
            state = "EXPANSION STATE"
            color = CLR_GREEN
        elif inv >= 60.0 and den >= 60.0:
            state = "STABILIZED SUBSTRATE"
            color = CLR_WHITE
        elif den >= 40.0 and didt < 30.0 and g2 < 45.0:
            state = "EXTRACTION SPIRAL"
            color = CLR_RED_BOLD
        else:
            state = "STABLE REGIME"
            color = CLR_CYAN
            
        ui_rows.append([
            f"{color}{tech}{CLR_RESET}", f"{g2:.1f}", f"{inv:.1f}", f"{didt:.1f}", f"{den:.1f}", f"{color}{state}{CLR_RESET}"
        ])
        
    headers = ["Technology Paradigm", "Γ2 (Runway)", "I (Invariance)", "dI/dt (Velocity)", "D (Density)", "Phase Transition State"]
    print(f"\n{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE PHYSICAL TECHNOLOGY STATE MACHINE  |  CIVILIZATIONAL FORECASTING SUITE{CLR_RESET}")
    print(f"  Axiom: Substrate Formation = f(Γ2, I, dI/dt, D) derived from raw physical observables")
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(tabulate(ui_rows, headers=headers, showindex=False, tablefmt='presto'))
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}\n")

if __name__ == "__main__":
    evaluate_technology_states()
