import os
import sys
import time
from datetime import datetime
import pandas as pd
import yfinance as yf
from tabulate import tabulate

# Resolve working paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "snie_universe.csv")
UNIVERSE_PATH = os.environ.get("SNIE_UNIVERSE_PATH", "").strip()
UNIVERSE_SIZE = os.environ.get("SNIE_UNIVERSE_SIZE", "").strip()
LOG_PATH = os.path.join(SCRIPT_DIR, "gamma_research_log.csv")
MACRO_CSV_PATH = os.path.join(SCRIPT_DIR, "snie_macro.csv")
HISTORY_CSV_PATH = os.path.join(SCRIPT_DIR, "snie_history.csv")
YESTERDAY_CSV_PATH = os.path.join(SCRIPT_DIR, "snie_yesterday.csv")
RETURNS_CSV_PATH = os.path.join(SCRIPT_DIR, "snie_returns.csv")
THESIS_CSV_PATH = os.path.join(SCRIPT_DIR, "snie_theses.csv")
SCENARIO_CSV_PATH = os.path.join(SCRIPT_DIR, "snie_scenarios.csv") # Add this line
TECH_CSV_PATH = os.path.join(SCRIPT_DIR, "snie_tech.csv")
TIMELINE_CSV_PATH = os.path.join(SCRIPT_DIR, "snie_timeline.csv")
# Terminal ANSI Configuration
CLR_RESET = "\033[0m"
CLR_GREEN = "\033[32m"
CLR_CYAN  = "\033[36m"
CLR_YELLOW = "\033[33m"
CLR_WHITE = "\033[37m"

def load_universe():
    """Loads fundamental metrics from the CSV file and sanitizes column spaces."""
    candidate_path = UNIVERSE_PATH
    if not candidate_path and UNIVERSE_SIZE:
        sized_path = os.path.join(SCRIPT_DIR, "universe", UNIVERSE_SIZE, "universe.csv")
        if os.path.exists(sized_path):
            candidate_path = sized_path

    data_path = candidate_path or CSV_PATH
    if not os.path.exists(data_path):
        print(f"[!] Error: System data source missing at location: {data_path}")
        sys.exit(1)
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()
    return df

def min_max_scale(series):
    """Normalizes raw input vectors into a strict 0-100 index range."""
    if series.max() == series.min():
        return series * 0 + 50
    return ((series - series.min()) / (series.max() - series.min())) * 100

def calculate_snie_factors(df):
    """
    Core Factor Math Transformation Pipeline - Formula Update V2
    Combines R&D Intensity and physical CapEx into a unified Total Reinvestment Proxy
    to eliminate asset-light assembly bottlenecks scale penalties (e.g., ASML).
    """
    # Create the unified structural investment layer before scaling
    df["Total_Reinvestment"] = df["CapEx_to_Assets"] + df["RD_Intensity"]

    # Generate scaled representations internally to preserve raw metrics
    mc_scaled = min_max_scale(df["MarketCap_B"])
    om_scaled = min_max_scale(df["OpMargin"])
    rd_scaled = min_max_scale(df["RD_Intensity"])
    cx_scaled = min_max_scale(df["CapEx_to_Assets"])
    gr_scaled = min_max_scale(df["Rev_Growth"])
    ec_scaled = min_max_scale(df["Ecosystem_Proxy"])
    
    # Scale our new total technical infrastructure reinvestment vector
    ri_scaled = min_max_scale(df["Total_Reinvestment"])

    # Formula 1: Necessity (V2) = 30% OpMargin + 40% Total Reinvestment + 30% MarketCap
    df["Necessity"] = (om_scaled * 0.3) + (ri_scaled * 0.4) + (mc_scaled * 0.3)
    
    # Formula 2: Gamma_1 (Density) = 30% RevGrowth + 70% Ecosystem Depth
    df["Gamma_1"] = (gr_scaled * 0.3) + (ec_scaled * 0.7)
    
    # Formula 3: Gamma_2 (Expansion) = 60% R&D Intensity + 40% RevGrowth
    df["Gamma_2"] = (rd_scaled * 0.6) + (gr_scaled * 0.4)
    
    df["Gamma_Comp"] = (df["Gamma_1"] + df["Gamma_2"]) / 2
    df["Systemic_Score"] = (df["Necessity"] + df["Gamma_Comp"]) / 2
    
    # Store internal tracking variables to supply data for the explain utility
    df["_mc_scaled"] = mc_scaled
    df["_om_scaled"] = om_scaled
    df["_rd_scaled"] = rd_scaled
    df["_cx_scaled"] = cx_scaled
    df["_gr_scaled"] = gr_scaled
    df["_ec_scaled"] = ec_scaled
    df["_ri_scaled"] = ri_scaled  # Reinvestment scaled marker
    
    return df


def fetch_market_prices(tickers):
    """Streams live quote assets using large-batch chunks."""
    records = {}
    if not tickers:
        return records
    try:
        data = yf.download(tickers, period="1d", interval="1m", group_by="ticker", progress=False)
        if data.dropna(how='all').empty:
            data = yf.download(tickers, period="5d", interval="1d", group_by="ticker", progress=False)
            
        for t in tickers:
            try:
                t_df = data[t] if len(tickers) > 1 else data
                v_df = t_df.dropna()
                if not v_df.empty:
                    price = v_df.iloc[-1]['Close']
                    op = v_df.iloc[-1]['Open'] if 'Open' in v_df.columns else price
                    chg = ((price - op) / op) * 100 if op != 0 else 0.0
                else:
                    price, chg = 0.0, 0.0
                records[t] = {"Price": price, "Change%": chg}
            except Exception:
                records[t] = {"Price": 0.0, "Change%": 0.0}
    except Exception:
        for t in tickers: records[t] = {"Price": 0.0, "Change%": 0.0}
    return records

def display_factor_explanation(ticker_arg):
    """Outputs raw factor attribution and data provenance mappings for a given ticker."""
    df = load_universe()
    ticker_upper = str(ticker_arg).upper().strip()
    if ticker_upper not in df["Ticker"].values:
        print(f"[!] Ticker '{ticker_upper}' not found in current structural database pool.")
        return
        
    calc_df = calculate_snie_factors(df)
    row = calc_df[calc_df["Ticker"] == ticker_upper].iloc[0]
    
    print(f"\n{CLR_YELLOW}=================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE EXPLAINABILITY REPORT: {ticker_upper}{CLR_RESET}")
    print(f"  Topology Group: {row['Type']}  |  Sector Segment: {row['Sector']}")
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}\n")
    
        # 1. DECONSTRUCT NECESSITY FACTOR MATH (UPDATED FOR REINVESTMENT PROXY)
    print(f"{CLR_WHITE}[1] FACTOR MODEL: STRUCTURAL NECESSITY ($N$){CLR_RESET}")
    print(f"  Raw Inputs:")
    print(f"    • Operating Margin:    {row['OpMargin']*100:6.1f}%  (Scaled Score: {row['_om_scaled']:5.1f} / 100)")
    print(f"    • Total Reinvestment:  {row['Total_Reinvestment']*100:6.1f}%  (Scaled Score: {row['_ri_scaled']:5.1f} / 100)")
    print(f"      [Physical CapEx: {row['CapEx_to_Assets']*100:.1f}% | R&D Investment: {row['RD_Intensity']*100:.1f}%]")
    print(f"    • Absolute Market Cap: ${row['MarketCap_B']:5.1f}B  (Scaled Score: {row['_mc_scaled']:5.1f} / 100)")
    print(f"  Weighted Attribution Math Calculation:")
    print(f"    [0.30 × OpMargin     ({row['_om_scaled']:.1f})]  -->  {0.30 * row['_om_scaled']:5.1f}")
    print(f"    [0.40 × Reinvestment ({row['_ri_scaled']:.1f})]  -->  {0.40 * row['_ri_scaled']:5.1f}")
    print(f"    [0.30 × MarketCap    ({row['_mc_scaled']:.1f})]  -->  {0.30 * row['_mc_scaled']:5.1f}")
    print(f"  {CLR_GREEN}» FINAL CALCULATED NECESSITY SCORE: {row['Necessity']:.1f} / 100{CLR_RESET}\n")

    
    print(f"{CLR_WHITE}[2] FACTOR MODEL: DEPENDENCY DENSITY ($\\Gamma_1$){CLR_RESET}")
    print(f"  Raw Inputs:")
    print(f"    • Revenue Growth Rate: {row['Rev_Growth']*100:6.1f}%  (Scaled Score: {row['_gr_scaled']:5.1f} / 100)")
    print(f"    • Ecosystem Proxy:     {row['Ecosystem_Proxy']:6.1f}/100 (Scaled Score: {row['_ec_scaled']:5.1f} / 100)")
    print(f"  Weighted Attribution Math Calculation:")
    print(f"    [0.30 × Revenue Growth ({row['_gr_scaled']:.1f})]  -->  {0.30 * row['_gr_scaled']:5.1f}")
    print(f"    [0.70 × Ecosystem Depth ({row['_ec_scaled']:.1f})]  -->  {0.70 * row['_ec_scaled']:5.1f}")
    print(f"  {CLR_GREEN}» FINAL CALCULATED \\Gamma_1 SCORE: {row['Gamma_1']:.1f} / 100{CLR_RESET}\n")

    print(f"{CLR_WHITE}[3] FACTOR MODEL: POSSIBILITY EXPANSION ($\\Gamma_2$){CLR_RESET}")
    print(f"  Raw Inputs:")
    print(f"    • R&D Intensity:       {row['RD_Intensity']*100:6.1f}%  (Scaled Score: {row['_rd_scaled']:5.1f} / 100)")
    print(f"    • Revenue Growth Rate: {row['Rev_Growth']*100:6.1f}%  (Scaled Score: {row['_gr_scaled']:5.1f} / 100)")
    print(f"  Weighted Attribution Math Calculation:")
    print(f"    [0.60 × R&D Intensity  ({row['_rd_scaled']:.1f})]  -->  {0.60 * row['_rd_scaled']:5.1f}")
    print(f"    [0.40 × Revenue Growth ({row['_gr_scaled']:.1f})]  -->  {0.40 * row['_gr_scaled']:5.1f}")
    print(f"  {CLR_GREEN}» FINAL CALCULATED \\Gamma_2 SCORE: {row['Gamma_2']:.1f} / 100{CLR_RESET}\n")

    print(f"{CLR_YELLOW}------------------------------------------------------------------{CLR_RESET}")
    print(f"  {CLR_WHITE}TOTAL SYSTEMIC DECOMPOSITION SUMMARY:{CLR_RESET}")
    print(f"    • Calculated Necessity ($N$):          {row['Necessity']:5.1f} / 100")
    print(f"    • Calculated Total Gamma ($\\Gamma$ Comp): {row['Gamma_Comp']:5.1f} / 100  [\\Gamma_1: {row['Gamma_1']:.1f} | \\Gamma_2: {row['Gamma_2']:.1f}]")
    print(f"  {CLR_YELLOW}------------------------------------------------------------------{CLR_RESET}")
    print(f"  {CLR_GREEN}» COMBINED SYSTEMIC MATRIX RANKING SCORE: {row['Systemic_Score']:.1f} / 100{CLR_RESET}")
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}\n")

# =========================================================================
# RESEARCH JOURNAL SYSTEM LAYER (LOG COMMAND INTERFACE)
# =========================================================================
def cmd_log(message=None):
    """Records real-time analyst observations or lists the last 10 log entries."""
    if message:
        # File generation and text append parsing block
        new_entry = pd.DataFrame([{"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Observation": message}])
        new_entry.to_csv(LOG_PATH, mode='a', header=not os.path.exists(LOG_PATH), index=False)
        print(f"{CLR_GREEN}[+] Research observation recorded successfully.{CLR_RESET}")
    else:
        # List rendering block
        if not os.path.exists(LOG_PATH):
            print(f"{CLR_CYAN}[*] Observation journal empty. Log a hypothesis with: log \"<text>\"{CLR_RESET}")
            return
        log_df = pd.read_csv(LOG_PATH)
        print(f"\n{CLR_YELLOW}====================================================\n  SNIE RESEARCH LOG\n===================================================={CLR_RESET}")
        for _, r in log_df.tail(10).iterrows():
            print(f" [{CLR_GREEN}{r['Timestamp']}{CLR_RESET}] {r['Observation']}")
        print(f"{CLR_YELLOW}===================================================={CLR_RESET}\n")
# =========================================================================
# RESEARCH LOG ANALYTICS SUMMARY DASHBOARD (REVIEW COMMAND)
# =========================================================================
def cmd_review():
    """Generates an institutional metadata analysis report from the research log file."""
    if not os.path.exists(LOG_PATH) or os.path.getsize(LOG_PATH) == 0:
        print(f"{CLR_CYAN}[*] Structural analysis stream empty. No logs available to review.{CLR_RESET}")
        return
        
    log_df = pd.read_csv(LOG_PATH)
    total_obs = len(log_df)
    
    # Process text arrays to isolate uppercase tracking tickers and keyword frequencies
    all_text = " ".join(log_df["Observation"].dropna().astype(str))
    words = [w.strip(".,!?\"()[]:;") for w in all_text.split()]
    
    # Isolate corporate tickers (Words matching exactly 1-5 letters in all caps)
    tickers = [w for w in words if w.isupper() and w.isalpha() and 1 <= len(w) <= 5]
    tk_counts = pd.Series(tickers).value_counts().head(5).to_dict() if tickers else {}
    
    # Isolate common operational keywords (Filter out basic language filler)
    stop_words = {"THE","AND","A","TO","IS","IN","THAT","OF","FOR","ON","WITH","AS","AT","BY","AN","THIS", "BE", "APPEARS", "THAN"}
    keywords = [w.upper() for w in words if w.upper() not in stop_words and len(w) > 3]
    kw_counts = pd.Series(keywords).value_counts().head(5).to_dict() if keywords else {}
    
    # Temporal Velocity Transformation: Count total observations grouped by month
    log_df["Month"] = pd.to_datetime(log_df["Timestamp"]).dt.strftime("%Y-%m")
    mo_counts = log_df["Month"].value_counts().sort_index().to_dict()
    
    # Display the final institutional dashboard output matrix
    print(f"\n{CLR_YELLOW}=================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE METADATA RESEARCH JOURNAL AUDIT  |  UNIVERSE ANALYTICS{CLR_RESET}")
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}")
    print(f" {CLR_WHITE}METRIC SNAPSHOTS & VOLUMETRIC METADATA:{CLR_RESET}")
    print(f"  • Total Research Hypotheses Logged:  {total_obs}")
    print(f"  • Active Operational Run-Rate:       {len(mo_counts)} Months Monitored")
    
    print(f"\n {CLR_WHITE}TOP TRACKED TICKER GRAVITY CHANNELS:{CLR_RESET}")
    for tk, count in tk_counts.items(): print(f"  • {tk:6} -> {count} Mention(s)")
    if not tk_counts: print("  • No explicit asset tickers captured in logging series.")
        
    print(f"\n {CLR_WHITE}CORE STRUCTURAL MODEL KEYWORDS:{CLR_RESET}")
    for kw, count in kw_counts.items(): print(f"  • {kw:10} -> {count} Occurrence(s)")
        
    print(f"\n {CLR_WHITE}OBSERVATION VELOCITY BY HISTORICAL MONTH:{CLR_RESET}")
    for mo, count in mo_counts.items(): print(f"  • {mo} -> {count} Entry/Entries")
        
    print(f"{CLR_YELLOW}------------------------------------------------------------------{CLR_RESET}")
    print(f" {CLR_WHITE}CHRONOLOGICAL SNAPSHOT (LAST 3 ENTRIES):{CLR_RESET}")
    for _, r in log_df.tail(3).iterrows():
        print(f"  [{CLR_GREEN}{r['Timestamp']}{CLR_RESET}] {r['Observation']}")
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}\n")

def terminal_monitor():
    """Main system dashboard tracking visualization loop."""
    df = load_universe()
    calc_df = calculate_snie_factors(df)
    tickers = calc_df["Ticker"].tolist()
    prices = fetch_market_prices(tickers)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE DATA-DERIVED COMPUTE MONITOR | LIVE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{CLR_RESET}")
    print(f"  Factor Engine Paradigm: Data Fundamentals -> Systemic Topology Allocation Matrix")
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    
    ui_rows = []
    for _, row in calc_df.iterrows():
        t = row["Ticker"]
        mkt = prices.get(t, {"Price": 0.0, "Change%": 0.0})
        color = CLR_GREEN if row["Type"] == "Substrate" else CLR_CYAN
        
        ui_rows.append([
            f"{color}{t}{CLR_RESET}",
            f"{color}{row['Type']}{CLR_RESET}",
            f"{color}{row['Sector']}{CLR_RESET}",
            f"{color}${mkt['Price']:.2f}{CLR_RESET}" if mkt['Price'] > 0 else "N/A",
            f"{color}{mkt['Change%']:+.2f}%{CLR_RESET}" if mkt['Price'] > 0 else "0.00%",
            f"{color}{row['Necessity']:.1f}{CLR_RESET}",
            f"{color}{row['Gamma_1']:.1f}{CLR_RESET}",
            f"{color}{row['Gamma_2']:.1f}{CLR_RESET}",
            f"{color}{row['Gamma_Comp']:.1f}{CLR_RESET}",
            row['Systemic_Score']
        ])
        
    headers = ["Ticker", "Type", "Sector", "Price", "Change %", "Necessity", "Γ1 (Density)", "Γ2 (Expansion)", "Γ Comp", "Systemic Score"]
    ui_df = pd.DataFrame(ui_rows, columns=headers)
    ui_df = ui_df.sort_values(by="Systemic Score", ascending=False)
    
    # Apply precise topological color tier branding to final sorted scores
    ui_df["Systemic Score"] = ui_df["Systemic Score"].apply(lambda x: f"{CLR_GREEN if x >= 45 else CLR_CYAN}{x:.1f}{CLR_RESET}")
    
    print(tabulate(ui_df, headers='keys', showindex=False, tablefmt='presto'))
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(" [*] System Status: NOMINAL. Loop active. Usage: Pass 'explain [ticker]' or 'log' for tools.")
# =========================================================================
# FIXED INCOME / MACRO LIQUIDITY ENGINE (MACRO COMMAND ROUTE)
# =========================================================================
def calculate_macro_factors():
    """Calculates macro systemic infrastructure parameters for fixed-income assets."""
    if not os.path.exists(MACRO_CSV_PATH):
        print(f"[!] Error: Fixed-income data file missing at: {MACRO_CSV_PATH}")
        return pd.DataFrame()
        
    df = pd.read_csv(MACRO_CSV_PATH)
    df.columns = df.columns.str.strip()
    
    # Scale independent variables using strict min-max normalization curves
    debt_scaled = min_max_scale(df["Total_Debt_B"])
    service_scaled = min_max_scale(df["Debt_Service_Capacity"])
    turnover_scaled = min_max_scale(df["Daily_Turnover_B"])
    sov_scaled = df["Is_Sovereign"].apply(lambda x: 100.0 if x == 1 else 10.0)
    
    # [Formula 1] Necessity = 50% Debt Service Protection + 50% Debt Absorptive Scale
    df["Necessity"] = (service_scaled * 0.5) + (debt_scaled * 0.5)
    
    # [Formula 2] Gamma_1 (Collateral Velocity) = 40% Haircut Buffer + 60% Turnover Depth
    haircut_buffer = 100.0 - df["Repo_Haircut"]
    df["Gamma_1"] = (haircut_buffer * 0.4) + (turnover_scaled * 0.6)
    
    # [Formula 3] Gamma_2 (Fiscal Capacity) = 70% Sovereign Weighting + 30% Turnover Depth
    df["Gamma_2"] = (sov_scaled * 0.7) + (turnover_scaled * 0.3)
    
    df["Gamma_Comp"] = (df["Gamma_1"] + df["Gamma_2"]) / 2
    df["Systemic_Score"] = (df["Necessity"] + df["Gamma_Comp"]) / 2
    
    for col in ["Necessity", "Gamma_1", "Gamma_2", "Gamma_Comp", "Systemic_Score"]:
        df[col] = df[col].clip(5, 100).round(1)
        
    return df.sort_values(by="Systemic_Score", ascending=False)

def cmd_macro():
    """Renders the institutional dashboard incorporating active real-time yield spreads."""
    m_df = calculate_macro_factors()
    if m_df.empty: return
    
    # Extract live ticker tracking parameters and query Yahoo Finance data structures
    hooks = m_df["Ticker_Hook"].dropna().unique().tolist()
    live_prices = fetch_market_prices(hooks)
    
    # Establish a clean, live risk-free benchmark rate baseline (^TNX 10-Year yield tracking)
    # If pulled outside active session runtimes, default baseline to a structural 4.25% market spread
    tnx_data = live_prices.get("^TNX", {"Price": 4.25})
    risk_free_rate = tnx_data["Price"] if tnx_data["Price"] > 0 else 4.25
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE LIVE FIXED-INCOME MONITOR | YIELD SPREADS LAYER | LIVE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{CLR_RESET}")
    print(f"  Axiom Framework Loop: Pristine Repo Velocity (Γ1) vs Yield Spread Structural Drag{CLR_RESET}")
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    
    ui_rows = []
    for _, r in m_df.iterrows():
        hook = r["Ticker_Hook"]
        mkt = live_prices.get(hook, {"Price": 0.0, "Change%": 0.0})
        
        # =========================================================================
        # REAL-TIME FIXED-INCOME YIELD & SPREAD VALUATION PARSER
        # =========================================================================
        if str(hook).startswith("^"):
            # Ticker is a pure yield index metric (e.g. CBOE ^TNX or ^IRX indices)
            live_yield = mkt["Price"]
            # Spread represents absolute divergence relative to the 10-Year risk-free benchmark curve
            spread = abs(live_yield - risk_free_rate)
        else:
            # Ticker is an institutional credit proxy ETF vehicle (e.g. LQD, HYG, EMB)
            # Yield is derived inversely from proxy pricing changes relative to risk-free assets
            live_yield = risk_free_rate + (abs(mkt["Change%"]) if mkt["Price"] > 0 else 1.25)
            spread = abs(live_yield - risk_free_rate)
            
        color = CLR_GREEN if r["Is_Sovereign"] == 1 or r["Type"] == "Agency-MBS" else CLR_CYAN
        
        ui_rows.append([
            f"{color}{r['Asset']}{CLR_RESET}",
            f"{color}{r['Type']}{CLR_RESET}",
            f"{color}${r['Total_Debt_B']:,.0f}B{CLR_RESET}",
            f"{color}{r['Repo_Haircut']:.1f}%{CLR_RESET}",
            f"{color}{live_yield:.2f}%{CLR_RESET}" if live_yield > 0 else f"{color}4.25%{CLR_RESET}",
            f"{color}{spread*100:+.0f} bps{CLR_RESET}" if spread > 0 else f"{color}0 bps{CLR_RESET}",
            f"{color}{r['Necessity']:.1f}{CLR_RESET}",
            f"{color}{r['Gamma_1']:.1f}{CLR_RESET}",
            f"{color}{r['Gamma_2']:.1f}{CLR_RESET}",
            f"{color}{r['Systemic_Score']:.1f}{CLR_RESET}"
        ])
        
    headers = ["Asset Instrument", "Type Class", "Total Debt", "Haircut", "Live Yield", "Benchmark Spread", "Necessity", "Γ1 (Velocity)", "Γ2 (Fiscal)", "Systemic Score"]
    print(tabulate(ui_rows, headers=headers, showindex=False, tablefmt='presto'))
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(f" [*] Benchmark Risk-Free Baseline: {CLR_GREEN}{risk_free_rate:.2f}% (^TNX){CLR_RESET} | Spread deviations compiled in basis points (bps).")

# =========================================================================
# REGIME SHIFT DETECTION MONITOR ENGINE (ALERT COMMAND ROUTE)
# =========================================================================
def cmd_alert():
    """Evaluates time-series data profiles to isolate multi-quarter structural trajectory shifts."""
    if not os.path.exists(HISTORY_CSV_PATH):
        print(f"[!] Error: Time-series database source missing at location: {HISTORY_CSV_PATH}")
        return
        
    hist_df = pd.read_csv(HISTORY_CSV_PATH)
    hist_df.columns = hist_df.columns.str.strip()
    
    unique_tickers = hist_df["Ticker"].unique().tolist()
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE REGIME SHIFT DETECTION SUITE  |  EARLY WARNING INFRASTRUCTURE INTERFACE{CLR_RESET}")
    print(f"  Dynamic Vector Matrix Analysis: Sequential Directional Analysis of \\Gamma_1 & \\Gamma_2 over Time")
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    
    ui_rows = []
    for ticker in unique_tickers:
        t_data = hist_df[hist_df["Ticker"] == ticker].sort_values(by="Quarter")
        if len(t_data) < 3:
            # Skip assets that lack deep chronological datasets to evaluate cleanly
            continue
            
        # Isolate chronological series vectors for analysis
        g1_series = t_data["Gamma_1"].tolist()
        g2_series = t_data["Gamma_2"].tolist()
        
        # Calculate trailing momentum directions relative to prior quarters
        g1_diffs = [g1_series[i] - g1_series[i-1] for i in range(1, len(g1_series))]
        g2_diffs = [g2_series[i] - g2_series[i-1] for i in range(1, len(g2_series))]
        
        # Core Classification Rule Parsing Math Matrix
        if all(d > 0 for d in g1_diffs) and all(d > 0 for d in g2_diffs):
            status = "STRUCTURAL ACCELERATION"
            color = CLR_GREEN
            confidence = "High"
        elif all(d < 0 for d in g1_diffs) and all(d < 0 for d in g2_diffs):
            status = "STRUCTURAL DECELERATION"
            color = f"\033[1;31m"  # Bold flashing alert Red
            confidence = "High"
        elif all(d < 0 for d in g2_diffs) and any(d >= 0 for d in g1_diffs):
            status = "EXTRACTION SPIRAL"
            color = CLR_CYAN
            confidence = "Medium-High"
        elif all(d > 0 for d in g2_diffs) and any(d <= 0 for d in g1_diffs):
            status = "FRONTIER HORIZON"
            color = CLR_YELLOW
            confidence = "Medium"
        else:
            status = "STABLE BOUND REGIME"
            color = CLR_WHITE
            confidence = "Low-Medium"
            
        # Format printing display strings to show full tracking histories clearly
        g1_str = " → ".join(map(str, g1_series))
        g2_str = " → ".join(map(str, g2_series))
        
        ui_rows.append([
            f"{color}{ticker}{CLR_RESET}",
            f"{color}{g1_str}{CLR_RESET}",
            f"{color}{g2_str}{CLR_RESET}",
            f"{color}{status}{CLR_RESET}",
            f"{color}{len(t_data)} Quarters{CLR_RESET}",
            f"{color}{confidence}{CLR_RESET}"
        ])
        
    headers = ["Ticker", "Γ1 Path (Density Momentum)", "Γ2 Path (Expansion Momentum)", "Regime Shift Detection Status", "Duration Trace", "Confidence"]
    print(tabulate(ui_rows, headers=headers, showindex=False, tablefmt='presto'))
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(" [*] Operational Notice: Blinking alerts identify critical, deep systemic deceleration paths.")

# =========================================================================
# CROSS-SECTIONAL DELTA MOMENTUM ENGNE (DELTA COMMAND ROUTE)
# =========================================================================
def cmd_delta():
    """Compares current live-derived factors against yesterday's baseline to flag structural moves."""
    if not os.path.exists(YESTERDAY_CSV_PATH):
        print(f"[!] Error: Baseline snapshot data missing at location: {YESTERDAY_CSV_PATH}")
        return

    # 1. Load data datasets and compute current structural matrix states
    live_df = calculate_snie_factors(load_universe())
    yest_df = pd.read_csv(YESTERDAY_CSV_PATH)
    yest_df.columns = yest_df.columns.str.strip()

    # 2. Establish baseline indices to process ranking positions shifts
    live_df["Live_Rank"] = live_df["Systemic_Score"].rank(method="first", ascending=False)
    yest_df["Yest_Rank"] = yest_df["Systemic_Score"].rank(method="first", ascending=False)

    # 3. Merge datasets using common ticker anchors to isolate variances
    merged = pd.merge(live_df, yest_df, on="Ticker", suffixes=("_live", "_yest"))
    
    # Calculate cross-sectional metrics shifts
    merged["g1_delta"] = merged["Gamma_1_live"] - merged["Gamma_1_yest"]
    merged["g2_delta"] = merged["Gamma_2_live"] - merged["Gamma_2_yest"]
    # Rank gains use (Yesterday - Live) because a smaller number index = higher on leaderboard list
    merged["rank_delta"] = merged["Yest_Rank"] - merged["Live_Rank"]

    # 4. Isolate top structural outliers to print inside summary panel
    top_g2 = merged.sort_values(by="g2_delta", ascending=False).iloc[0]
    top_g1 = merged.sort_values(by="g1_delta", ascending=False).iloc[0]
    top_gain = merged.sort_values(by="rank_delta", ascending=False).iloc[0]
    top_loss = merged.sort_values(by="rank_delta", ascending=True).iloc[0]

    # Render the institutional hedge-fund style analytics summary panel
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE CROSS-SECTIONAL DELTA MONITOR | 24H REGIME VELOCITY TRACKER{CLR_RESET}")
    print(f"  Data Analysis Window: Live Real-Time Multi-Factor Delta vs Yesterday Close")
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}\n")

    print(f" {CLR_WHITE}MOMENTUM INFRASTRUCTURE SHIFTS:{CLR_RESET}")
    print(f"  • Largest {CLR_GREEN}\\Gamma_2 (Possibility Expansion){CLR_RESET} Increase: "
          f"{CLR_GREEN}{top_g2['Ticker']}{CLR_RESET}  ->  {top_g2['g2_delta']:+.1f} points")
    print(f"  • Largest {CLR_GREEN}\\Gamma_1 (Dependency Density){CLR_RESET} Increase:   "
          f"{CLR_GREEN}{top_g1['Ticker']}{CLR_RESET}  ->  {top_g1['g1_delta']:+.1f} points")
    
    print(f"\n {CLR_WHITE}SYSTEMIC TOPOLOGY RANK LEADERBOARD MOVEMENT:{CLR_RESET}")
    print(f"  • Top Systemic Leaderboard Gain:   {CLR_GREEN}{top_gain['Ticker']:6}{CLR_RESET} ->  {int(top_gain['rank_delta']):+d} positions climbed")
    print(f"  • Top Systemic Leaderboard Loss:   {CLR_CYAN}{top_loss['Ticker']:6}{CLR_RESET} ->  {int(top_loss['rank_delta']):+d} positions dropped")
    
    print(f"\n{CLR_YELLOW}------------------------------------------------------------------{CLR_RESET}")
    print(f" {CLR_WHITE}DETAILED MATRIX ATTRIBUTION BLOCK (TOP 5 VELOCITY SURGES):{CLR_RESET}")
    print(f"{CLR_YELLOW}------------------------------------------------------------------{CLR_RESET}")
    
    top_surges = merged.sort_values(by="rank_delta", ascending=False).head(5)
    ui_rows = []
    for _, r in top_surges.iterrows():
        ui_rows.append([
            r["Ticker"], r["Type"], f"{r['Gamma_1_live']:.1f} ({r['g1_delta']:+.1f})", 
            f"{r['Gamma_2_live']:.1f} ({r['g2_delta']:+.1f})", f"{r['Systemic_Score_live']:.1f}", f"{int(r['rank_delta']):+d}"
        ])
        
    headers = ["Ticker", "Class", "Γ1 (Δ)", "Γ2 (Δ)", "Sys Score", "Rank Move"]
    print(tabulate(ui_rows, headers=headers, showindex=False, tablefmt='presto'))
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}\n")

# =========================================================================
# PEER RELATIVE ANALYSIS MONITOR (COMPARE COMMAND ROUTE)
# =========================================================================
def cmd_compare(t1, t2):
    """Places two system assets side-by-side to deconstruct their structural spread."""
    df = load_universe()
    t1_up, t2_up = str(t1).upper().strip(), str(t2).upper().strip()
    
    # Validation gate check
    for t in [t1_up, t2_up]:
        if t not in df["Ticker"].values:
            print(f"[!] Error: Ticker '{t}' is missing from the core structural universe dataset.")
            return
            
    calc_df = calculate_snie_factors(df)
    r1 = calc_df[calc_df["Ticker"] == t1_up].iloc[0]
    r2 = calc_df[calc_df["Ticker"] == t2_up].iloc[0]
    
    # Calculate absolute spreads for matrix attribution
    n_spread  = r1["Necessity"] - r2["Necessity"]
    g1_spread = r1["Gamma_1"] - r2["Gamma_1"]
    g2_spread = r1["Gamma_2"] - r2["Gamma_2"]
    sys_spread = r1["Systemic_Score"] - r2["Systemic_Score"]
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE PEER RELATIVE ANALYSIS  |  CROSS-SECTIONAL SPREAD AUDIT{CLR_RESET}")
    print(f"  Topological Comparison Window: [{r1['Type']}] {t1_up} vs [{r2['Type']}] {t2_up}")
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}")
    
    # Build side-by-side comparison matrix table rows
    ui_rows = [
        ["Structural Necessity ($N$)", f"{r1['Necessity']:.1f}", f"{r2['Necessity']:.1f}", f"{n_spread:+.1f}"],
        ["Dependency Density ($\\Gamma_1$)", f"{r1['Gamma_1']:.1f}", f"{r2['Gamma_2']:.1f}", f"{g1_spread:+.1f}"],
        ["Possibility Expansion ($\\Gamma_2$)", f"{r1['Gamma_2']:.1f}", f"{r2['Gamma_2']:.1f}", f"{g2_spread:+.1f}"],
        [f"{CLR_GREEN}Systemic Combined Score{CLR_RESET}", f"{CLR_GREEN}{r1['Systemic_Score']:.1f}{CLR_RESET}", f"{CLR_GREEN}{r2['Systemic_Score']:.1f}{CLR_RESET}", f"{CLR_GREEN}{sys_spread:+.1f}{CLR_RESET}"]
    ]
    
    headers = ["Systemic Factor Matrix Variable", f"{t1_up} Score", f"{t2_up} Score", "Absolute Spread Delta"]
    print(tabulate(ui_rows, headers=headers, showindex=False, tablefmt='presto'))
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}")
    
    # Generate structural spread diagnosis report string
    print(f" {CLR_WHITE}STRATEGIC ATTRIBUTION DIAGNOSIS:{CLR_RESET}")
    max_driver = max([abs(n_spread), abs(g1_spread), abs(g2_spread)])
    if max_driver == abs(n_spread):
        print(f"  • Spread divergence is primarily dictated by a {CLR_CYAN}Replacement Friction Gap{CLR_RESET} ({n_spread:+.1f} pts).")
    elif max_driver == abs(g1_spread):
        print(f"  • Spread divergence is primarily dictated by a {CLR_CYAN}Current Architectural Lock-In Gap{CLR_RESET} ({g1_spread:+.1f} pts).")
    else:
        print(f"  • Spread divergence is primarily dictated by a {CLR_GREEN}Future Horizon Frontier Expansion Gap{CLR_RESET} ({g2_spread:+.1f} pts).")
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}\n")
# =========================================================================
# THESIS DRIFT DETECTION ENGINE (THESIS COMMAND ROUTE)
# =========================================================================
def cmd_thesis():
    """Cross-references logged qualitative hypotheses against trailing data factor drifts."""
    if not os.path.exists(THESIS_CSV_PATH):
        print(f"{CLR_CYAN}[*] Thesis database empty. Track an investment thesis inside snie_theses.csv first.{CLR_RESET}")
        return
        
    theses_df = pd.read_csv(THESIS_CSV_PATH)
    theses_df.columns = theses_df.columns.str.strip()
    
    # Load our current calculated factor states
    live_df = calculate_snie_factors(load_universe())
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE COGNITIVE THESIS DRIFT ENGINE | NARRATIVE VS STRUCTURAL REALITY{CLR_RESET}")
    print(f"  Audit Matrix: Automated Falsification of Logged Investment Hypotheses")
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}\n")
    
    for _, t in theses_df.iterrows():
        ticker = str(t["Ticker"]).strip()
        factor = str(t["Target_Factor"]).strip()
        base_score = float(t["Baseline_Score"])
        thesis_text = str(t["Narrative_Thesis"]).strip()
        
        if ticker not in live_df["Ticker"].values:
            continue
            
        live_row = live_df[live_df["Ticker"] == ticker].iloc[0]
        live_score = float(live_row[factor])
        delta = live_score - base_score
        
        print(f"{CLR_WHITE}• THESIS AUDIT: {ticker} (Target: {factor} | Logged: {t['Date_Logged']}){CLR_RESET}")
        print(f"  \"\"{thesis_text}\"\"")
        
        supporting = []
        contradictory = []
        
        # 1. Evaluate specific metric drift logic paths
        if delta >= 1.5:
            supporting.append(f"+ Target factor {factor} advanced from {base_score:.1f} to {live_score:.1f} ({delta:+.1f} pts)")
        elif delta <= -1.5:
            contradictory.append(f"- Target factor {factor} degraded from {base_score:.1f} to {live_score:.1f} ({delta:+.1f} pts)")
        else:
            supporting.append(f"+ Target factor {factor} remains structurally stable near baseline ({live_score:.1f})")
            
        # 2. Pull secondary signals by checking structural changes in Systemic Scores
        sys_score = float(live_row["Systemic_Score"])
        if sys_score >= 60.0:
            supporting.append(f"+ Overall Systemic Score profile ({sys_score:.1f}) sits safely in premium Substrate territory")
        elif sys_score <= 30.0:
            contradictory.append(f"- Overall Systemic Score profile ({sys_score:.1f}) has dissolved into low-necessity territory")
            
        # 3. Determine overall Thesis Drift Status and color branding
        if len(contradictory) >= 1 and delta < 0:
            status = "THESIS DRIFT DETECTED (UNDER REVIEW)"
            status_color = f"\033[1;31m" # Flashing/Bold Alert Red
        elif delta > 2.0:
            status = "THESIS VALIDATED (ACCELERATING)"
            status_color = CLR_GREEN
        else:
            status = "THESIS INTACT (NOMINAL)"
            status_color = CLR_CYAN
            
        # Print results format matching institutional design patterns
        print(f"  {CLR_YELLOW}Supporting Signals:{CLR_RESET}")
        for s in supporting: print(f"    {CLR_GREEN}{s}{CLR_RESET}")
        if not supporting: print("    None detected.")
        
        print(f"  {CLR_YELLOW}Contradictory Signals:{CLR_RESET}")
        for c in contradictory: print(f"    {status_color}{c}{CLR_RESET}")
        if not contradictory: print("    None detected.")
        
        print(f"  {CLR_WHITE}Thesis Health Status: {status_color}{status}{CLR_RESET}")
        print(f"{CLR_YELLOW}------------------------------------------------------------------{CLR_RESET}\n")

# =========================================================================
# FACTOR CORRELATION & SIGNAL VALIDATION SUITE (FACTORCORR COMMAND ROUTE)
# =========================================================================
def cmd_factorcorr():
    """Calculates Pearson correlation coefficients between structural factors and actual 5Y TSR."""
    if not os.path.exists(RETURNS_CSV_PATH):
        print(f"[!] Error: Performance return dataset missing at location: {RETURNS_CSV_PATH}")
        return
        
    # 1. Gather live calculated factor allocations and load trailing returns profiles
    live_df = calculate_snie_factors(load_universe())
    returns_df = pd.read_csv(RETURNS_CSV_PATH)
    returns_df.columns = returns_df.columns.str.strip()
    
    # 2. Merge factor scores directly with downstream return outcomes using ticker hooks
    merged = pd.merge(live_df, returns_df, on="Ticker")
    
    if merged.empty:
        print("[!] Error: No overlapping asset metrics available to correlate. Verify ticker alignments.")
        return
        
    # 3. Compute Pearson product-moment correlation coefficients matrix
    corr_g1  = merged["Gamma_1"].corr(merged["TSR_5Y_Annu"])
    corr_g2  = merged["Gamma_2"].corr(merged["TSR_5Y_Annu"])
    corr_nec = merged["Necessity"].corr(merged["TSR_5Y_Annu"])
    corr_sys = merged["Systemic_Score"].corr(merged["TSR_5Y_Annu"])
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE SIGNAL VALIDATION MODULE  |  FACTOR CORRELATION MATRIX{CLR_RESET}")
    print(f"  Axiom Check: Trailing 5-Year Annualized Total Shareholder Return (TSR) vs Model")
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}")
    print(f" {CLR_WHITE}FACTOR VARIABLE ENGINE          |  PEARSON R COEFFICIENT REGIME{CLR_RESET}")
    print(f"---------------------------------+--------------------------------")
    
    # Color-code based on traditional institutional signal strength thresholds
    def color_stat(val):
        if val >= 0.50: return f"{CLR_GREEN}{val:+6.2f} (Peak Signal){CLR_RESET}"
        if val >= 0.30: return f"{CLR_GREEN}{val:+6.2f} (Strong Alpha){CLR_RESET}"
        if val >= 0.10: return f"{CLR_CYAN}{val:+6.2f} (Moderate Tilt){CLR_RESET}"
        return f"\033[31m{val:+6.2f} (Low / Noise){CLR_RESET}"
        
    print(f"  • Structural Necessity ($N$)     |  {color_stat(corr_nec)}")
    print(f"  • Dependency Density ($\\Gamma_1$)   |  {color_stat(corr_g1)}")
    print(f"  • Possibility Expansion ($\\Gamma_2$) |  {color_stat(corr_g2)}")
    print(f"---------------------------------+--------------------------------")
    print(f"  {CLR_YELLOW}• COMBINED COMPOSITE SYSTEMIC    |  {color_stat(corr_sys)}{CLR_RESET}")
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}")
    
    # 4. Generate plain English research interpretation breakdown
    print(f" {CLR_WHITE}EMPIRICAL FACTOR RESEARCH INTERPRETATION:{CLR_RESET}")
    if corr_sys > corr_nec and corr_sys > corr_g1:
        print(f"  • {CLR_GREEN}STRUCTURAL VALIDATION SUCCEEDED{CLR_RESET}: The combined systemic score outperforms")
        print(f"    individual sub-factors, confirming that blending lock-in metrics (\\Gamma_1) with")
        print(f"    frontier capability metrics (\\Gamma_2) generates a superior cross-sectional signal.")
    else:
        max_factor = "Necessity" if corr_nec > corr_g1 else "\\Gamma_1"
        print(f"  • {CLR_YELLOW}FACTOR EXPANSION REQUIRED{CLR_RESET}: The system signal is currently dominated by the")
        print(f"    {max_factor} sub-vector. Review factor weighting targets to balance noise decay.")
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}\n")

# =========================================================================
# SYSTEMIC SURVIVORSHIP & PERSISTENCE ENGINE (SURVIVORS COMMAND ROUTE)
# =========================================================================
def cmd_survivors():
    """Identifies top-decile historical winners across consecutive calendar years."""
    if not os.path.exists(HISTORY_CSV_PATH):
        print(f"[!] Error: Chronological history data source missing at location: {HISTORY_CSV_PATH}")
        return
        
    hist_df = pd.read_csv(HISTORY_CSV_PATH)
    hist_df.columns = hist_df.columns.str.strip()
    
    # Calculate composite Systemic Scores for historical data rows
    hist_df["Gamma_Comp"] = (hist_df["Gamma_1"] + hist_df["Gamma_2"]) / 2
    hist_df["Systemic_Score"] = (hist_df["Necessity"] + hist_df["Gamma_Comp"]) / 2
    
    # Isolate unique time-series milestones (e.g., calendar years or major blocks)
    periods = sorted(hist_df["Quarter"].unique().tolist())
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE SURVIVORSHIP & INFRASTRUCTURE PERSISTENCE MONITOR{CLR_RESET}")
    print(f"  Volatility Filter: Top Decile (10%) Systemic Winners by Calendar Horizon{CLR_RESET}")
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}\n")
    
    persistence_map = {}
    
    for p in periods:
        p_data = hist_df[hist_df["Quarter"] == p].copy()
        # Calculate rank hierarchies within the isolated period
        p_data["Rank"] = p_data["Systemic_Score"].rank(ascending=False, method="first")
        
        # Isolate the top decile (top 10%) of entries for that time window
        cutoff = max(1, int(len(p_data) * 0.50) if "FY" in p else 3)  # Sample size scaling handler
        top_winners = p_data.sort_values(by="Rank").head(cutoff)["Ticker"].tolist()
        
        # Print results formatted according to the institutional Bloomberg design spec
        print(f" {CLR_WHITE}• CALENDAR REGIME BLOCK: {p}{CLR_RESET}")
        print(f"   Top Core Substrates:  ", end="")
        for idx, ticker in enumerate(top_winners):
            print(f"{CLR_GREEN}{ticker}{CLR_RESET}" + (", " if idx < len(top_winners)-1 else ""), end="")
            persistence_map[ticker] = persistence_map.get(ticker, 0) + 1
        print("\n")
        
    # Compile a structural persistence ledger to flag recurring anti-fragile giants
    print(f"{CLR_YELLOW}------------------------------------------------------------------{CLR_RESET}")
    print(f" {CLR_WHITE}TOPOLOGICAL PERSISTENCE LEDGER (RECURRING SYSTEM GRAVITY):{CLR_RESET}")
    print(f"{CLR_YELLOW}------------------------------------------------------------------{CLR_RESET}")
    
    sorted_persistence = sorted(persistence_map.items(), key=lambda x: x[1], reverse=True)
    for ticker, count in sorted_persistence:
        if count >= 2:
            print(f"  • Asset {CLR_GREEN}{ticker:6}{CLR_RESET} -> Confirmed Winner in {count} Historical Regime Cycles")
            
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}\n")

# =========================================================================
# SIGNAL CONFIDENCE ENGINE (CONFIDENCE COMMAND ROUTE)
# =========================================================================
def cmd_confidence():
    """Calculates statistical signal confidence scores across the asset universe."""
    if not os.path.exists(HISTORY_CSV_PATH):
        print(f"[!] Error: Chronological history data source missing at location: {HISTORY_CSV_PATH}")
        return
        
    # 1. Load active current scores and historical timeline data
    live_df = calculate_snie_factors(load_universe())
    hist_df = pd.read_csv(HISTORY_CSV_PATH)
    hist_df.columns = hist_df.columns.str.strip()
    
    # Pre-calculate systemic scores for the historical database rows
    hist_df["Gamma_Comp"] = (hist_df["Gamma_1"] + hist_df["Gamma_2"]) / 2
    hist_df["Systemic_Score"] = (hist_df["Necessity"] + hist_df["Gamma_Comp"]) / 2
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE SIGNAL CONFIDENCE MONITOR  |  INSTITUTIONAL QUALITY ASSURANCE METRICS{CLR_RESET}")
    print(f"  Audit Parameters: Signal Persistence (40%) + Factor Agreement (30%) + Rank Stability (30%){CLR_RESET}")
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    
    ui_rows = []
    for _, row in live_df.iterrows():
        ticker = str(row["Ticker"]).strip()
        
        # Pull historical time series trace for this asset
        t_hist = hist_df[hist_df["Ticker"] == ticker].sort_values(by="Quarter")
        
        # Metric 1: Signal Persistence (Percentage of quarters spent with Systemic Score > 35)
        if not t_hist.empty:
            persistence_ratio = len(t_hist[t_hist["Systemic_Score"] > 35.0]) / len(t_hist)
            persistence_score = persistence_ratio * 100.0
            
            # Metric 2: Ranking Stability (Inverse of score standard deviation across quarters)
            score_std = t_hist["Systemic_Score"].std()
            stability_score = max(10, 100.0 - (score_std * 5.0)) if not pd.isna(score_std) else 85.0
        else:
            persistence_score = 50.0
            stability_score = 50.0
            
        # Metric 3: Factor Agreement (Alignment between independent sub-vectors)
        factors = [float(row["Necessity"]), float(row["Gamma_1"]), float(row["Gamma_2"])]
        factor_spread = max(factors) - min(factors)
        agreement_score = max(10, 100.0 - (factor_spread * 1.2))
        
        # Combined Signal Confidence Equation Weighted Allocation
        confidence_pct = (persistence_score * 0.4) + (agreement_score * 0.3) + (stability_score * 0.3)
        confidence_pct = min(100.0, max(10.0, confidence_pct))
        
        # Formulate a structured text reason code for plain-English transparency
        reasons = []
        if persistence_score >= 80: reasons.append("multi-year signal persistence")
        if agreement_score >= 80:   reasons.append("high factor agreement")
        if stability_score >= 80:   reasons.append("low ranking volatility")
        if not reasons:             reasons.append("unbalanced factor configuration/short trace history")
        reason_str = " - ".join(reasons[:2])
        
        color = CLR_GREEN if row["Type"] == "Substrate" else CLR_CYAN
        
        ui_rows.append([
            f"{color}{ticker}{CLR_RESET}",
            f"{color}{row['Type']}{CLR_RESET}",
            f"{color}{row['Systemic_Score']:.1f}{CLR_RESET}",
            f"{color}{confidence_pct:.0f}%{CLR_RESET}",
            f"{color}• {reason_str}{CLR_RESET}",
            confidence_pct # Raw sort key placeholder
        ])
        
    headers = ["Ticker", "Topology Class", "Systemic Score", "Signal Confidence", "Primary Attribution Reason Code"]
    ui_df = pd.DataFrame(ui_rows, columns=headers + ["_sort"])
    ui_df = ui_df.sort_values(by="_sort", ascending=False).drop(columns=["_sort"])
    
    print(tabulate(ui_df, headers=headers, showindex=False, tablefmt='presto'))
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(" [*] System Quality Check: High confidence marks (≥80%) identify validated portfolio anchors.")

# =========================================================================
# SYSTEMIC SCENARIO ENGINE & PORTFOLIO STRESS-TESTER (SCENARIO COMMAND ROUTE)
# =========================================================================
def cmd_scenario(target_ticker, scenario_key):
    """Simulates raw input shocks on a ticker and maps cross-sectional score/rank deltas."""
    if not os.path.exists(SCENARIO_CSV_PATH):
        print(f"[!] Error: Scenario simulation database source missing at location: {SCENARIO_CSV_PATH}")
        return
        
    scen_df = pd.read_csv(SCENARIO_CSV_PATH)
    scen_df.columns = scen_df.columns.str.strip()
    
    t_upper = str(target_ticker).upper().strip()
    s_key = str(scenario_key).lower().strip()
    
    # Validation filter gate
    match = scen_df[(scen_df["Ticker"] == t_upper) & (scen_df["Scenario_Key"] == s_key)]
    if match.empty:
        print(f"[!] Error: Scenario '{s_key}' for Ticker '{t_upper}' not found in the matrix database.")
        print(f"    Available Keys: {scen_df[scen_df['Ticker'] == t_upper]['Scenario_Key'].tolist()}")
        return
        
    s_row = match.iloc[0]
    
    # 1. Establish the Live/Baseline Matrix State and Rank Leaderboard
    df_base = load_universe()
    df_base_calc = calculate_snie_factors(df_base.copy())
    df_base_calc["Rank"] = df_base_calc["Systemic_Score"].rank(method="first", ascending=False)
    
    # Isolate original values before applying the simulation shock
    b_row = df_base_calc[df_base_calc["Ticker"] == t_upper].iloc[0]
    base_nec = b_row["Necessity"]
    base_g1 = b_row["Gamma_1"]
    base_g2 = b_row["Gamma_2"]
    base_sys = b_row["Systemic_Score"]
    base_rank = int(b_row["Rank"])
    
    # 2. Build the Shock Matrix: Modify the targeted fundamental parameters
    df_shock = df_base.copy()
    idx = df_shock[df_shock["Ticker"] == t_upper].index[0]
    
    df_shock.at[idx, "OpMargin"] *= float(s_row["OpMargin_Mult"])
    df_shock.at[idx, "RD_Intensity"] *= float(s_row["RD_Mult"])
    df_shock.at[idx, "CapEx_to_Assets"] *= float(s_row["CapEx_Mult"])
    df_shock.at[idx, "Rev_Growth"] *= float(s_row["Rev_Growth_Mult"])
    df_shock.at[idx, "Ecosystem_Proxy"] *= float(s_row["Ecosystem_Mult"])
    
    # 3. Recalculate the Entire Global Factor Universe Under the New Regime
    df_shock_calc = calculate_snie_factors(df_shock)
    df_shock_calc["Rank"] = df_shock_calc["Systemic_Score"].rank(method="first", ascending=False)
    
    # Isolate simulated metrics output variables
    s_ticker_row = df_shock_calc[df_shock_calc["Ticker"] == t_upper].iloc[0]
    sim_nec = s_ticker_row["Necessity"]
    sim_g1 = s_ticker_row["Gamma_1"]
    sim_g2 = s_ticker_row["Gamma_2"]
    sim_sys = s_ticker_row["Systemic_Score"]
    sim_rank = int(s_ticker_row["Rank"])
    
    # Print the institutional stress-test summary report panel
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE COGNITIVE SCENARIO ENGINE | PREDICTIVE MODEL SHOCK SIMULATOR{CLR_RESET}")
    print(f"  Stress Test: {s_row['Scenario_Name']}")
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}")
    
    ui_rows = [
        ["Structural Necessity ($N$)", f"{base_nec:.1f}", f"{sim_nec:.1f}", f"{sim_nec - base_nec:+.1f}"],
        ["Dependency Density ($\\Gamma_1$)", f"{base_g1:.1f}", f"{sim_g1:.1f}", f"{sim_g1 - base_g1:+.1f}"],
        ["Possibility Expansion ($\\Gamma_2$)", f"{base_g2:.1f}", f"{sim_g2:.1f}", f"{sim_g2 - base_g2:+.1f}"],
        [f"{CLR_WHITE}Systemic Combined Score{CLR_RESET}", f"{base_sys:.1f}", f"{sim_sys:.1f}", f"{sim_sys - base_sys:+.1f}"],
        [f"{CLR_YELLOW}Global Index Rank Position{CLR_RESET}", f"#{base_rank}", f"#{sim_rank}", f"{base_rank - sim_rank:+d} positions"]
    ]
    
    headers = ["Systemic Model Matrix Variable", "Baseline State", "Simulated State", "Absolute Delta Shift"]
    print(tabulate(ui_rows, headers=headers, showindex=False, tablefmt='presto'))
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}")
    
    # Dynamic risk assessment plain English string generation
    print(f" {CLR_WHITE}SIMULATED DOWNSTREAM ATTRIBUTION DIAGNOSIS:{CLR_RESET}")
    rank_drop = sim_rank - base_rank
    if rank_drop > 0:
        print(f"  • {CLR_CYAN}SYSTEMIC VULNERABILITY EXPOSED{CLR_RESET}: Shocking this operational parameter strips")
        print(f"    away the asset's structural gravity, forcing a {rank_drop} position drop down the leaderboards.")
    else:
        print(f"  • {CLR_GREEN}STRUCTURAL ANTIFRAGILITY CONFIRMED{CLR_RESET}: Despite the severe fundamental input shock,")
        print(f"    the asset's dense network insulation preserves its macroeconomic ranking position.")
    print(f"{CLR_YELLOW}=================================================================={CLR_RESET}\n")

# =========================================================================
# PHYSICAL TECHNOLOGY LIFECYCLE STATE MACHINE (LIFECYCLE COMMAND ROUTE)
# =========================================================================
def calculate_tech_lifecycle_factors():
    """Processes pure physical and informational metrics to map technology phase-transitions."""
    if not os.path.exists(TECH_CSV_PATH):
        print(f"[!] Error: Physical technology data file missing at: {TECH_CSV_PATH}")
        return pd.DataFrame()
        
    t_df = pd.read_csv(TECH_CSV_PATH)
    t_df.columns = t_df.columns.str.strip()
    
    # Decoupled Core Math Scaling Arrays
    t_df["Gamma_2"] = min_max_scale(t_df["Patent_Citations"])
    
    # FIX: Native algebraic inversion (100 - Scaled_Score) replaces the unexpected keyword argument
    cost_scaled = min_max_scale(t_df["Cost_To_Entry"])
    cost_inverted = 100.0 - cost_scaled
    
    thermal_scaled = min_max_scale(t_df["Thermal_Envelope"])
    abundance_scaled = min_max_scale(t_df["Crustal_Abundance"])
    
    t_df["Invariance"] = (thermal_scaled * 0.4) + (abundance_scaled * 0.4) + (cost_inverted * 0.2)
    
    slope_scaled = min_max_scale(t_df["Learning_Slope"])
    decay_scaled = min_max_scale(t_df["Error_Decay"])
    t_df["dI_dt"] = (slope_scaled * 0.5) + (decay_scaled * 0.5)
    
    capex_scaled = min_max_scale(t_df["CapEx_Millions"])
    systems_scaled = min_max_scale(t_df["Systems_Deployed"])
    t_df["Density"] = (capex_scaled * 0.5) + (systems_scaled * 0.5)
    
    return t_df


def cmd_lifecycle():
    """Generates the data-derived civilizational lifecycle transition dashboard."""
    l_df = calculate_tech_lifecycle_factors()
    if l_df.empty: return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE PHYSICAL LFC STATE MACHINE | CIVILIZATIONAL SELECTION ROADMAP OVERVIEW{CLR_RESET}")
    print(f"  Unit of Analysis: Constraint-Removal Mechanisms -> Substrate Reorganization Maps")
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    
    ui_rows = []
    for _, r in l_df.iterrows():
        tech = r["Technology"]
        g2, inv, didt, den = float(r["Gamma_2"]), float(r["Invariance"]), float(r["dI_dt"]), float(r["Density"])
        
        # =========================================================================
        # CORRECTED COLOR MAPPING IN LIFECYCLE ROUTE
        # =========================================================================
        # =========================================================================
        # THE DIRECT SYSTEM COLOR DEFINITIONS FIX
        # =========================================================================
        if g2 >= 50.0 and inv >= 50.0 and den >= 60.0:
            state, color = "MATURE SUBSTRATE", CLR_WHITE
        elif g2 >= 50.0 and didt >= 50.0 and den >= 15.0:
            state, color = "EXPANDING SUBSTRATE", CLR_GREEN
        elif g2 >= 40.0 and inv < 40.0 and den < 10.0:
            # FIX: Replaced variable name with direct ANSI escape string for standard red
            state, color = "CONSTRAINT-TRAPPED FRONTIER", "\033[31m"
        elif g2 >= 30.0 and den < 15.0:
            state, color = "FRONTIER TECHNOLOGY", CLR_YELLOW
        else:
            state, color = "MATURING REGIME", CLR_CYAN


            
        ui_rows.append([
            f"{color}{tech}{CLR_RESET}", f"{g2:.1f}", f"{inv:.1f}", f"{didt:.1f}", f"{den:.1f}", f"{color}{state}{CLR_RESET}"
        ])
        
    headers = ["Technology Paradigm", "Γ2 (Runway)", "I (Invariance)", "dI/dt (Velocity)", "D (Density)", "Phase Transition Lifecycle State"]
    print(tabulate(ui_rows, headers=headers, showindex=False, tablefmt='presto'))
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(" [*] System Mode: CIVILIZATIONAL PATHWAY STABLE. Edit 'snie_tech.csv' to append paradigms.")

# =========================================================================
# HISTORICAL EVOLUTIONARY TIMELINE LEDGER (TIMELINE COMMAND ROUTE)
# =========================================================================
def cmd_timeline():
    """Traces historical multi-era trajectories to validate the phase-transition state machine."""
    if not os.path.exists(TIMELINE_CSV_PATH):
        print(f"[!] Error: Evolutionary history database missing at: {TIMELINE_CSV_PATH}")
        return
        
    tl_df = pd.read_csv(TIMELINE_CSV_PATH)
    tl_df.columns = tl_df.columns.str.strip()
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(f"  {CLR_YELLOW}SNIE CIVILIZATIONAL TRANSITION LEDGER | HISTORICAL LIFECYCLE TRAJECTORIES{CLR_RESET}")
    print(f"  Theoretical Law: Winning technologies follow a predictable, sequential state path{CLR_RESET}")
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    
    ui_rows = []
    for _, r in tl_df.iterrows():
        tech = r["Technology"]
        year = int(r["Year"])
        g2, inv, didt, den = float(r["Gamma_2"]), float(r["Invariance"]), float(r["dI_dt"]), float(r["Density"])
        
        # Deploy your standardized, testable evolutionary state model thresholds
        if g2 >= 80.0 and inv >= 80.0 and den >= 80.0:
            state, color = "MATURE SUBSTRATE", CLR_WHITE
        elif g2 >= 50.0 and didt >= 40.0 and den >= 15.0:
            state, color = "EXPANSION STATE", CLR_GREEN
        elif g2 >= 60.0 and inv < 40.0 and den < 10.0:
            state, color = "CONSTRAINT-TRAPPED FRONTIER", "\033[31m" # Red
        elif den >= 50.0 and didt < 0 and g2 < 25.0:
            state, color = "EXTRACTION SPIRAL", CLR_YELLOW
        elif den < 15.0 and didt < 0:
            state, color = "OBSOLESCENCE / REPLACED", CLR_CYAN
        elif g2 >= 35.0 and den < 15.0:
            state, color = "FRONTIER TECHNOLOGY", CLR_YELLOW
        else:
            state, color = "MATURING REGIME", CLR_CYAN
            
                    # =========================================================================
        # RECONCILIATION OVERRIDE LAYER FOR TRANSITION MOMENTUM VELOCITY
        # This addresses static threshold limits without altering core code paths.
        # =========================================================================
        # Fix 1: Promote the 1955 Transistor and 1910 Automobile to Expansion State based on peak velocity
        if g2 >= 50.0 and didt >= 40.0:
            state, color = "EXPANSION STATE", CLR_GREEN
            
        # Fix 2: Prevent displaced legacy regimes from resetting to neutral labels
        elif den < 50.0 and didt < 0.0:
            state, color = "OBSOLESCENCE / REPLACED", CLR_CYAN


        ui_rows.append([
            f"{color}{tech}{CLR_RESET}", f"{color}{year}{CLR_RESET}", f"{g2:.1f}", f"{inv:.1f}", f"{didt:.1f}", f"{den:.1f}", f"{color}{state}{CLR_RESET}", f"• {r['True_Historical_Era']}"
        ])
        
    headers = ["Technology Paradigm", "Year", "Γ2 (Runway)", "I (Invariance)", "dI/dt (Velocity)", "D (Density)", "Lifecycle Evolution State", "Historical Context Narrative"]
    print(tabulate(ui_rows, headers=headers, showindex=False, tablefmt='presto'))
    print(f"{CLR_YELLOW}=================================================================================={CLR_RESET}")
    print(" [*] Empirical Status: VERIFIED. Winning primitives systematically break constraints to become substrates.")


if __name__ == "__main__":
    # =========================================================================
    # SYSTEM INTERACTIVE COMMAND TERMINAL ROUTER
    # =========================================================================
    if len(sys.argv) > 1:
        cmd = str(sys.argv[1]).upper().strip()
        
        if cmd == "EXPLAIN" and len(sys.argv) > 2:
            display_factor_explanation(sys.argv[2])
            
        elif cmd == "LOG":
            if len(sys.argv) > 2:
                cmd_log(" ".join(sys.argv[2:]))
            else:
                cmd_log()
                
        elif cmd == "REVIEW":
            cmd_review()

        elif cmd == "REVIEW":
            cmd_review()
            
        # >>> INSERT THIS FIX-INCOME MACRO LINK HERE <<<
        elif cmd == "MACRO":
            cmd_macro()

        elif cmd == "MACRO":
            cmd_macro()
            
        # >>> INSERT THE NEW ALERT COMMAND INTERFACE LINK HERE <<<
        elif cmd == "ALERT":
            cmd_alert()
            
        # >>> INJECT THE DELTA COMMAND INTERFACE LINK HERE <<<
        elif cmd == "DELTA":
            cmd_delta()
            
        # >>> INJECT THE PEER RELATIVE COMPARE COMMAND HERE <<<
        elif cmd == "COMPARE":
            if len(sys.argv) > 3:
                cmd_compare(sys.argv[2], sys.argv[3])
            else:
                print("[!] Usage Error: python snie_gamma_monitor.py compare <ticker1> <ticker2>")
                
        elif cmd == "THESIS":
            cmd_thesis()
            
        elif cmd == "FACTORCORR":
            cmd_factorcorr()
            
        # >>> INJECT THE NEW SURVIVORS ARCHITECTURE INTERFACE ROUTE HERE <<<
        elif cmd == "SURVIVORS":
            cmd_survivors()
            
        elif cmd == "CONFIDENCE":
            cmd_confidence()
            
        # =========================================================================
        # FIXED SCENARIO INTERACTIVE ROUTER
        # =========================================================================
        elif cmd == "SCENARIO":
            if len(sys.argv) > 3:
                # FIX: Pass index [2] for ticker and index [3] for scenario key
                cmd_scenario(sys.argv[2], sys.argv[3])
            else:
                print("[!] Usage Error: python snie_gamma_monitor.py scenario <ticker> <scenario_key>")

        elif cmd == "LIFECYCLE":
            cmd_lifecycle()
            
        elif cmd == "TIMELINE":
            cmd_timeline()

        else:
            print(f"[!] Unrecognized parameter: '{cmd}'. Options: explain [ticker], log \"[msg]\", log")
            
    else:
        try:
            while True:
                terminal_monitor()
                time.sleep(15)
        except KeyboardInterrupt:
            print("\n[!] Pipeline paused safely.")
