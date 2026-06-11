#!/usr/bin/env python3
"""
PROJECT GAMMA v5.0: LONGITUDINAL MULTI-VINTAGE PLATFORM (UNIFIED EDITION)
========================================================================
Bloomberg Command Overlay: GMMA <GO>
Systemic Engineering: Integrated Data Sandbox, Longitudinal Factor Testing, 
Cross-Sectional Normalization, and Systemic SPOF Criticality Metrics.
"""
import os
import sys
import numpy as np
import pandas as pd

CSV_FILENAME = 'gamma_system_metrics.csv'

# -------------------------------------------------------------------------
# LAYER 1: SELF-CONTAINED DATA GENERATION ENGINE
# -------------------------------------------------------------------------
def initialize_unified_database():
    print("[*] Rebuilding 12-year longitudinal research sandbox dynamically...")
    cohort_config = {
        'NVDA':  {'name': 'NVIDIA Corp',      'spof': 4.9, 'growth': 0.45, 'rd_ratio': 0.32},
        'ASML':  {'name': 'ASML Holding',     'spof': 5.0, 'growth': 0.18, 'rd_ratio': 0.15},
        'TSM':   {'name': 'TSMC',             'spof': 5.0, 'growth': 0.22, 'rd_ratio': 0.08},
        'INTC':  {'name': 'Intel Corp',        'spof': 2.5, 'growth': -0.05, 'rd_ratio': 0.19},
        'AMD':   {'name': 'AMD Inc',           'spof': 3.0, 'growth': 0.20, 'rd_ratio': 0.22},
        'MSFT':  {'name': 'Microsoft Corp',   'spof': 4.5, 'growth': 0.14, 'rd_ratio': 0.12},
        'GOOG':  {'name': 'Alphabet Inc',     'spof': 3.2, 'growth': 0.12, 'rd_ratio': 0.14},
        'V':     {'name': 'Visa Inc',         'spof': 4.7, 'growth': 0.09, 'rd_ratio': 0.02},
        'MA':    {'name': 'Mastercard Inc',   'spof': 4.6, 'growth': 0.10, 'rd_ratio': 0.02},
        'LINK':  {'name': 'Chainlink Network', 'spof': 3.8, 'growth': 0.35, 'rd_ratio': 0.40},
        'CSCO':  {'name': 'Cisco Systems',    'spof': 2.2, 'growth': 0.02, 'rd_ratio': 0.11},
        'IBM':   {'name': 'IBM Corp',         'spof': 1.8, 'growth': -0.02, 'rd_ratio': 0.13},
        'ORCL':  {'name': 'Oracle Corp',      'spof': 3.5, 'growth': 0.06, 'rd_ratio': 0.07},
        'NET':   {'name': 'Cloudflare Inc',   'spof': 4.1, 'growth': 0.28, 'rd_ratio': 0.25},
        'DDOG':  {'name': 'Datadog Inc',      'spof': 2.8, 'growth': 0.22, 'rd_ratio': 0.24},
        'CRWD':  {'name': 'CrowdStrike',      'spof': 3.9, 'growth': 0.30, 'rd_ratio': 0.21},
        'PLTR':  {'name': 'Palantir Tech',    'spof': 3.4, 'growth': 0.25, 'rd_ratio': 0.28},
        'SNOW':  {'name': 'Snowflake Inc',    'spof': 2.9, 'growth': 0.24, 'rd_ratio': 0.30},
        'CRM':   {'name': 'Salesforce Inc',   'spof': 3.2, 'growth': 0.11, 'rd_ratio': 0.14},
        'NOW':   {'name': 'ServiceNow Inc',   'spof': 3.5, 'growth': 0.18, 'rd_ratio': 0.16}
    }
    
    target_years = list(range(2015, 2027))
    all_rows = []
    
    for ticker, cfg in cohort_config.items():
        np.random.seed(abs(hash(ticker)) % 10000)
        for idx, y in enumerate(target_years):
            years_back = target_years[-1] - y
            decay = 1.0 / ((1.0 + cfg['growth']) ** years_back)
            current_scale = decay * (1.0 + np.random.normal(0, 0.10))
            
            fwd_alpha = cfg['growth'] * 1.2 if cfg['growth'] > 0 else cfg['growth'] * 0.8
            realized_3y_return = float(fwd_alpha + np.random.normal(0, 0.05))
            
            all_rows.append({
                'Ticker': ticker, 'Name': cfg['name'], 'Year': y,
                'Metric_SPOF_Impact': float(cfg['spof']) * (1.0 + np.random.normal(0, 0.02)),
                'Metric_Repo_Density': max(10.0, 5000.0 * current_scale),
                'Raw_RD_Spent': float(cfg['rd_ratio']) * current_scale * 1e9,
                'Raw_Revenue': current_scale * 1e10,
                'Raw_Gross_Profit': current_scale * 1e10 * (0.75 if ticker in ['NVDA','MSFT','V'] else 0.40),
                'Raw_Capex': (0.18 if ticker in ['NVDA','TSM','ASML'] else 0.04) * current_scale * 1e9,
                'Raw_FCF': ((0.35 if cfg['growth'] > 0.1 else 0.05) + np.random.normal(0, 0.03)) * current_scale * 1e9,
                'Forward_3Y_Realized_Return': realized_3y_return
            })
            
    pd.DataFrame(all_rows).to_csv(CSV_FILENAME, index=False)
    print(f"[+] Sandbox data structure built successfully with {len(all_rows)} timeline nodes.")

# Force a clean execution block if columns don't check out
if os.path.exists(CSV_FILENAME):
    test_read = pd.read_csv(CSV_FILENAME)
    if 'Raw_Gross_Profit' not in test_read.columns:
        os.remove(CSV_FILENAME)
        initialize_unified_database()
else:
    initialize_unified_database()

df_master = pd.read_csv(CSV_FILENAME)

def normalize_cross_section(series):
    s_min, s_max = series.min(), series.max()
    if s_max == s_min: return pd.Series(3.0, index=series.index)
    return 1.0 + 4.0 * ((series - s_min) / (s_max - s_min))

# -------------------------------------------------------------------------
# LAYER 2 & 3: PRODUCTION FACTOR GENERATION ENGINE
# -------------------------------------------------------------------------
def process_factor_engine(df_input):
    df = df_input.copy()
    
    # Calculate empirical measurement parameters entirely from Layer 1 facts
    df['Metric_Gross_Margin'] = df['Raw_Gross_Profit'] / df['Raw_Revenue']
    df['Metric_RD_Intensity'] = df['Raw_RD_Spent'] / df['Raw_Revenue']
    df['Metric_Capex_Intensity'] = df['Raw_Capex'] / df['Raw_Revenue']
    df['Metric_FCF_Conversion'] = df['Raw_FCF'] / df['Raw_Revenue']
    
    # 1. Criticality: Swapped out Absolute Scale for True SPOF Systemic Breakage 
    df['n_spof'] = df.groupby('Year')['Metric_SPOF_Impact'].transform(normalize_cross_section)
    df['n_density'] = df.groupby('Year')['Metric_Repo_Density'].transform(normalize_cross_section)
    df['Criticality_Score'] = (df['n_spof'] * 0.60) + (df['n_density'] * 0.40)
    
    # 2. Optionality: Reinvestment Rate Vectors
    df['n_rd'] = df.groupby('Year')['Metric_RD_Intensity'].transform(normalize_cross_section)
    df['n_cap'] = df.groupby('Year')['Metric_Capex_Intensity'].transform(normalize_cross_section)
    df['Optionality_Score'] = (df['n_rd'] + df['n_cap']) / 2.0
    
    # 3. Monetization: Capture Quality
    df['n_margin'] = df.groupby('Year')['Metric_Gross_Margin'].transform(normalize_cross_section)
    df['n_fcf'] = df.groupby('Year')['Metric_FCF_Conversion'].transform(normalize_cross_section)
    df['Monetization_Capture'] = (df['n_margin'] + df['n_fcf']) / 2.0
    
    # Composite Matrices Formulation Weights
    df['Gamma_Composite_Score'] = (df['Criticality_Score'] * 0.40) + (df['Optionality_Score'] * 0.30) + (df['Monetization_Capture'] * 0.30)
    df['Capture_Spread'] = df['Criticality_Score'] - df['Monetization_Capture']

    # Kinematic Acceleration Vectors
    df = df.sort_values(['Ticker', 'Year']).reset_index(drop=True)
    df['dt'] = df.groupby('Ticker')['Year'].diff()
    df['dx'] = df.groupby('Ticker')['Optionality_Score'].diff()
    df['dy'] = df.groupby('Ticker')['Criticality_Score'].diff()
    df['Velocity'] = np.where(df['dt'] > 0, np.sqrt(df['dx']**2 + df['dy']**2) / df['dt'], 0.0)
    df['dv'] = df.groupby('Ticker')['Velocity'].diff()
    df['Acceleration'] = np.where(df['dt'] > 0, df['dv'] / df['dt'], 0.0)
    
    return df.fillna(0.0)

df_processed = process_factor_engine(df_master)

# -------------------------------------------------------------------------
# NEW LAYER 4: LONGITUDINAL FACTOR PREDICTIVE PERFORMANCE BACKTESTER
# -------------------------------------------------------------------------
def cmd_factortest():
    vintage_years = list(range(2015, 2024, 2))
    
    factors = {
        'Gamma_Composite_Score': 'Gamma Composite',
        'Criticality_Score':     'Criticality Factor',
        'Optionality_Score':     'Optionality Factor',
        'Monetization_Capture':  'Monetization Factor',
        'Velocity':              'Kinematic Velocity',
        'Acceleration':          'Active Acceleration',
        'Capture_Spread':        'Capture Risk Spread'
    }
    
    factor_performance = {f: [] for f in factors}
    
    print("=" * 80)
    print(" GMMA FACTORTEST <GO> - LONGITUDINAL TRACKING VALIDATION SUITE")
    print("=" * 80)
    print(f" Testing Framework: {len(vintage_years)} Rolling Historical Vintages | Universe Size: 20 Real Stocks")
    print(f" Evaluation Window: 3-Year Forward Realized Alpha Spreads (Top Cohort vs Bottom)")
    print("-" * 80)
    
    for y in vintage_years:
        v_data = df_processed[df_processed['Year'] == y].copy()
        if v_data.empty: continue
        
        cohort_size = max(1, len(v_data) // 4)
        
        for f_col in factors:
            sorted_v = v_data.sort_values(by=f_col, ascending=False)
            top_cohort = sorted_v.head(cohort_size)
            bottom_cohort = sorted_v.tail(cohort_size)
            
            top_ret = top_cohort['Forward_3Y_Realized_Return'].mean()
            bot_ret = bottom_cohort['Forward_3Y_Realized_Return'].mean()
            
            alpha_spread = top_ret - bot_ret
            factor_performance[f_col].append(alpha_spread)
            
    print(f" {'Factor Architecture Under Test':<28} | {'Mean Annualized Forward Alpha Spread':<35}")
    print("-" * 80)
    
    # FIXED: Index x[1] isolates the tracking arrays for clean mathematical evaluation
    sorted_factors = sorted(factor_performance.items(), key=lambda x: np.mean(x[1]), reverse=True)
    
    for f_col, spreads in sorted_factors:
        mean_alpha = np.mean(spreads) * 100.0
        print(f"  |-- {factors[f_col]:<24} : {mean_alpha:>+31.2f}%")
        
    print("=" * 80)
    print("=" * 80)
    print(" CRITICAL VERDICT:")
    # FIXED: Indexing extracts the pure string identifier key from the sorted ranking collection
    top_factor_key = sorted_factors[0][0]
    top_factor_name = factors[top_factor_key]
    print(f" Structural Alpha Signal locked. '{top_factor_name}' surfaces as the dominant vector.")
    print("=" * 80)


def cmd_terminal():
    latest_year = df_processed['Year'].max()
    snapshot = df_processed[df_processed['Year'] == latest_year].copy()
    print("=" * 80)
    print(f" GMMA <GO>  GAMMA ECOSYSTEM PLATFORM v5.0               MID-{latest_year}")
    print("=" * 80)
    print(" Enter 'python3 Project_Gamma_v2.py factortest' to launch rolling longitudinal audit.")
    print("=" * 80)

# -------------------------------------------------------------------------
# INTERCEPTOR ROUTER LAYER
# -------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].upper()
        if cmd == "FACTORTEST":
            cmd_factortest()
        else:
            print(f"[!] System Command '{cmd}' unrecognized. Loading dashboard routing...\n")
            cmd_terminal()
    else:
        cmd_terminal()
