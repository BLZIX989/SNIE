SNIE: Structural Necessity & Infrastructure Evaluation
What This Project Is

SNIE is a structural analysis framework designed to identify systems, technologies, companies, and infrastructure layers that occupy critical positions within larger economic and technological networks.

Rather than focusing exclusively on valuation, earnings, momentum, or sentiment, SNIE attempts to measure how deeply a system is embedded within the dependencies of other systems.

The core research question is:

Which technologies become indispensable substrates for future activity, and which remain replaceable participants?

What Problem I Am Trying To Solve

Most investment and forecasting systems evaluate outcomes after they occur.

I wanted to explore whether structural characteristics could identify important systems before market consensus fully recognized them.

Examples include:

Railroads during industrial expansion
Integrated circuits during computing adoption
TCP/IP during internet expansion
Linux within cloud infrastructure
ASML within semiconductor manufacturing
NVIDIA within AI compute networks

The objective is not to predict stock prices directly.

The objective is to identify infrastructure layers that appear increasingly difficult to bypass.

Core Concepts
Necessity

Measures how difficult a system is to replace within its ecosystem.

Reachability Expansion (Γ₂)

Measures how many future states become possible because a system exists.

Invariance (I)

Measures how resilient a system remains across changing environmental conditions.

Density (D)

Measures the concentration of dependencies flowing through a system.

Structural Gravity Index (SGI)

Composite estimate of systemic importance based on the interaction of these variables.

Conceptual Model

You can then include:

S=Γ
2
	​

×I×
dt
dI
	​

×D

Where:

Γ₂ = Reachability Expansion
I = Invariance
dI/dt = Invariance Momentum
D = Dependency Density

This equation represents the conceptual architecture used throughout the framework.

What The Software Does

The software:

Pulls live market and system data.
Stores historical snapshots.
Tracks changes between runs.
Calculates structural indicators.
Generates ranking tables.
Produces lifecycle and regime analyses.
Builds visualizations of system evolution through time.

Outputs include:

Structural rankings
Regime shift detection
Dependency mapping
Necessity scoring
Survivorship analysis
Historical persistence tracking
Fixed income monitoring
Transition probability analysis
Example Interpretation

A company may score highly even if current revenue growth is modest.

This occurs when the company occupies a critical infrastructure position within a larger dependency network.

Examples:

Semiconductor manufacturing
Cloud infrastructure
Payment rails
Energy transmission
Industrial logistics

The framework attempts to distinguish value extraction from value enablement.


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
