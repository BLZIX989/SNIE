import os
import sys
import time
from datetime import datetime
import pandas as pd
import yfinance as yf
from tabulate import tabulate

# Workspace path configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "snie_universe.csv")
HISTORY_PATH = os.path.join(SCRIPT_DIR, "snie_history.csv")
UNIVERSE_PATH = os.environ.get("SNIE_UNIVERSE_PATH", "").strip()
UNIVERSE_SIZE = os.environ.get("SNIE_UNIVERSE_SIZE", "").strip()

# Terminal ANSI Theme Config
CLR_RESET = "\033[0m"
CLR_GREEN = "\033[32m"
CLR_CYAN  = "\033[36m"
CLR_YELLOW = "\033[33m"
CLR_WHITE = "\033[37m"
CLR_RED_BOLD = "\033[1;31m"

def load_data():
    candidate_path = UNIVERSE_PATH
    if not candidate_path and UNIVERSE_SIZE:
        sized_path = os.path.join(SCRIPT_DIR, "universe", UNIVERSE_SIZE, "universe.csv")
        if os.path.exists(sized_path):
            candidate_path = sized_path

    data_path = candidate_path or CSV_PATH
    if not os.path.exists(data_path) or not os.path.exists(HISTORY_PATH):
        print("[!] Error: Core CSV database components missing inside workspace folder.")
        sys.exit(1)
    univ = pd.read_csv(data_path)
    hist = pd.read_csv(HISTORY_PATH)
    univ.columns = univ.columns.str.strip()
    hist.columns = hist.columns.str.strip()
    return univ, hist

def min_max_scale(series):
    if series.max() == series.min(): return series * 0 + 50
    return ((series - series.min()) / (series.max() - series.min())) * 100

def run_state_machine():
    """Maps 4D coordinates to evaluate technological phase-transitions and lifecycle states."""
    univ, hist = load_data()
    
    # Generate live un-correlated factor derivations
    mc_scaled = min_max_scale(univ["MarketCap_B"])
    om_scaled = min_max_scale(univ["OpMargin"])
    rd_scaled = min_max_scale(univ["RD_Intensity"])
    cx_scaled = min_max_scale(univ["CapEx_to_Assets"])
    gr_scaled = min_max_scale(univ["Rev_Growth"])
    ec_scaled = min_max_scale(univ["Ecosystem_Proxy"])
    
    # 1. Coordinate 1: Gamma_2 (Possibility Expansion Runway)
    univ["Gamma_2"] = (rd_scaled * 0.6) + (gr_scaled * 0.4)
    
    # 2. Coordinate 2: Invariance (Static Resilience Array)
    univ["Invariance"] = (om_scaled * 0.4) + (ec_scaled * 0.6)
    
    # 3. Coordinate 4: Density (Current Systemic Embeddedness)
    univ["Density"] = (mc_scaled * 0.5) + (cx_scaled * 0.5)
    
    processed_records = []
    for _, row in univ.iterrows():
        t = row["Ticker"]
        g2 = float(row["Gamma_2"])
        inv = float(row["Invariance"])
        den = float(row["Density"])
        
        # 4. Coordinate 3: dI/dt (Extract the Velocity slope from historical time-series lines)
        t_hist = hist[hist["Ticker"] == t].sort_values(by="Quarter")
        if len(t_hist) >= 2:
            # Measure slope path of recent intervals
            didt = float(t_hist["Gamma_2"].iloc[-1] - t_hist["Gamma_2"].iloc[-2])
        else:
            didt = 0.0
            
        # =========================================================================
        # THE 4D LIFECYCLE REGIME CLASSIFICATION RULES MATRIX
        # =========================================================================
        if g2 >= 55.0 and den < 40.0:
            state = "FRONTIER STATE"
            color = CLR_YELLOW
        elif g2 >= 50.0 and didt > 0 and den >= 40.0:
            state = "EXPANSION STATE"
            color = CLR_GREEN
        elif inv >= 50.0 and den >= 60.0 and abs(didt) <= 2.5:
            state = "SUBSTRATE STATE"
            color = CLR_WHITE
        elif den >= 50.0 and didt < 0 and g2 < 45.0:
            state = "EXTRACTION SPIRAL"
            color = CLR_RED_BOLD
        else:
            state = "STABLE REGIME"
            color = CLR_CYAN
            
        processed_records.append({
            "Ticker": t, "Sector": row["Sector"], "Γ2 (Runway)": round(g2, 1),
            "I (Invariance)": round(inv, 1), "dI/dt (Slope)": round(didt, 2),
            "D (Density)": round(den, 1), "State": state, "_color": color
        })
        
    return pd.DataFrame(processed_records).sort_values(by="D (Density)", ascending=False)

def run_display():
    df = run_state_machine()
    tickers = df["Ticker"].tolist()
    
    # Establish single batch parallel quote collection download
    prices = {}
    try:
        m_data = yf.download(tickers, period="1d", interval="1m", group_by="ticker", progress=False)
        if m_data.dropna(how='all').empty:
            m_data = yf.download(tickers, period="5d", interval="1d", group_by="ticker", progress=False)
        for t in tickers:
            t_df = m_data[t] if len(tickers) > 1 else m_data
            prices[t] = {"P": t_df.dropna().iloc[-1]['Close'], "C": t_df.dropna().iloc[-1]['Change%'] if 'Change%' in t_df.columns else 0.0}
    except Exception:
        for t in tickers: prices[t] = {"P": 0.0, "C": 0.0}
        
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE 4D LIFECYCLE PHASE-TRANSITION STATE ENGINE | TRACKING COMPUTE INTERFACE{CLR_RESET}")
    print(f"  Unit of Analysis: Constraint-Removal Mechanisms -> Substrate Selection Maps")
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    
    ui_rows = []
    for _, r in df.iterrows():
        t = r["Ticker"]
        p = prices.get(t, {"P": 0.0, "C": 0.0})
        c = r["_color"]
        
        ui_rows.append([
            f"{c}{t}{CLR_RESET}", f"{c}{r['Sector']}{CLR_RESET}", 
            f"{c}${p['P']:.2f}{CLR_RESET}" if p['P'] > 0 else "N/A", f"{c}{p['C']:+.2f}%{CLR_RESET}",
            f"{c}{r['Γ2 (Runway)']}{CLR_RESET}", f"{c}{r['I (Invariance)']}{CLR_RESET}", 
            f"{c}{r['dI/dt (Slope)']}{CLR_RESET}", f"{c}{r['D (Density)']}{CLR_RESET}", 
            f"{c}{r['State']}{CLR_RESET}"
        ])
        
    headers = ["Ticker Mechanism", "Target Sector", "Price", "Change %", "Γ2 (Runway)", "I (Invariance)", "dI/dt (Velocity)", "D (Density)", "Phase Transition Lifecycle State"]
    print(tabulate(ui_rows, headers=headers, showindex=False, tablefmt='presto'))
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(" [*] System Mode: COGNITIVE GEOPOLITICAL STATE SELECTION ACTIVE. Press Ctrl+C to close.")

if __name__ == "__main__":
    try:
        while True:
            run_display()
            time.sleep(15)
    except KeyboardInterrupt:
        print("\n[!] State machine paused safely.")
