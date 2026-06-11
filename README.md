# Project Gamma Infrastructure Intelligence Terminal

This workspace currently contains a rebuilt single-file Gamma terminal scaffold in [Project Gamma Topolgy v3.py](Project%20Gamma%20Topolgy%20v3.py).

## What it provides

- Live FastAPI app with HTML dashboard
- Gamma state-space map with dynamic zones
- Historical trajectory replay
- Structural invariant monitor
- Thesis intelligence and validation layers
- Reachability, attractor, and dependency endpoints
- Architecture contract endpoint for downstream platformization

## Run

```bash
python3 "Project Gamma Topolgy v3.py"
```

If `uvicorn` is installed, the app starts on `http://127.0.0.1:8000`. Otherwise the module prints a JSON summary.

## Dependencies

Install from `requirements.txt` if you want the live terminal server:

```bash
pip install -r requirements.txt
```

## Next phase

The next rebuild step is to split this scaffold into a proper multi-file service layout with:

- backend engine modules
- FastAPI routers and schemas
- frontend Next.js terminal UI
- PostgreSQL persistence and migrations
- live stream transport for snapshot updates
