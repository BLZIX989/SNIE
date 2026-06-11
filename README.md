# Project Gamma Run Sheet

Run everything from the project root:

```bash
cd "/Users/keithblaze/Desktop/ChatGPT/Project Gamma"
source .venv/bin/activate
```

## Core Workflow

```bash
python universe_builder.py
python "Topology/Graphs/Project Gamma v2.py" BLIND
python snie_gamma_monitor.py
python 4D_LifeCycle.py
python snie_tech_forecast.py
```

## Monitor Commands

```bash
python snie_gamma_monitor.py EXPLAIN TICKER
python snie_gamma_monitor.py LOG "note"
python snie_gamma_monitor.py REVIEW
python snie_gamma_monitor.py MACRO
python snie_gamma_monitor.py ALERT
python snie_gamma_monitor.py DELTA
python snie_gamma_monitor.py COMPARE TICKER1 TICKER2
python snie_gamma_monitor.py THESIS
python snie_gamma_monitor.py FACTORCORR
python snie_gamma_monitor.py SURVIVORS
python snie_gamma_monitor.py CONFIDENCE
python snie_gamma_monitor.py SCENARIO TICKER scenario_key
python snie_gamma_monitor.py LIFECYCLE
python snie_gamma_monitor.py TIMELINE
```

## Universe Scaling

Use one of these before running the monitor or lifecycle scripts:

```bash
SNIE_UNIVERSE_SIZE=100 python snie_gamma_monitor.py
SNIE_UNIVERSE_SIZE=250 python snie_gamma_monitor.py
SNIE_UNIVERSE_SIZE=500 python snie_gamma_monitor.py
```

Or point directly at a file:

```bash
SNIE_UNIVERSE_PATH="/full/path/to/universe.csv" python snie_gamma_monitor.py
```

## Topology Maps

```bash
python "Topology/Graphs/Project Gamma Topology 3.py"
python "Topology/Graphs/Project Gamma Institutional Terminal.py"
python "Topology/Graphs/Topology Tool/Project Gamma Topology 2.py"
python "Topology/Graphs/Topology Tool/Project Gamma Topology.py"
python "Topology/Graphs/Topology Tool/Expansion Frontier/Project Gamma Topolgy v3.py"
python "Topology/Graphs/Topology Tool/Reachability Landscape/Project Gamma.py"
```

## Output Folders

```text
blind_test_runs/
validation/
universe/100/
universe/250/
universe/500/
```

## Research Protocol

1. Build universe.
2. Run BLIND test.
3. Archive blind output.
4. Do not modify rankings after generation.
5. Track outcomes quarterly.
6. Write postmortems before adjusting model weights.
7. Never overwrite historical runs.

## Current Model

Version: Gamma v2

Core Factors:
- Criticality
- Optionality
- Monetization

Classification System:
- Substrate
- Extractor
- Frontier
- Stable Regime

Research Status:
Prospective Validation Active

## Validation Objectives

Primary Question:

Does the blind-ranking engine identify future
infrastructure compounders better than random selection?

Secondary Questions:

- Does Criticality predict persistence?
- Does Optionality predict future expansion?
- Does Monetization predict value capture?
- Does Composite Score outperform individual factors?

Success is measured prospectively.
No retrospective modifications allowed.

## Known Risks

- Sector concentration bias
- Software overrepresentation
- Survivorship bias
- Proxy factor contamination
- Market-cap leakage
- Hindsight interpretation risk

## Notes

- `BLIND` saves each run to `blind_test_runs/blind_test_YYYY_MM_DD_HHMMSS.txt`.
- Validation rows are appended to `validation/YYYY_Q#.csv`.
- The ranking logic is unchanged; only the universe and logging layers scale.
