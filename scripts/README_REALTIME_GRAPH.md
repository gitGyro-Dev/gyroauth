# GyroAuth v2 — FastAPI + Live Stability Graph

This package demonstrates a minimal realtime connection:

```text
FastAPI /authenticate
↓
outputs/auth_history.csv
↓
scripts/live_stability_graph.py
↓
outputs/live_stability_timeline.png
```

## Install

```bash
pip install -r requirements.txt
```

## Start API

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Demo Steps

1. POST `/observe` with `examples/stable_observation.json`
2. POST `/authenticate`
3. POST `/observe` with `examples/reconverging_observation.json`
4. POST `/authenticate`
5. POST `/observe` with `examples/recovered_observation.json`
6. POST `/authenticate`
7. POST `/observe` with `examples/attack_observation.json`
8. POST `/authenticate`

Then run:

```bash
python scripts/live_stability_graph.py
```

Output:

```text
outputs/live_stability_timeline.png
outputs/auth_history.csv
```

## Meaning

This turns the API result into a visible stability timeline.

```text
AUTH_STABLE
→ RECONVERGING
→ AUTH_STABLE
→ AUTH_FAIL
```

## Final Statement

The graph is not just a chart.

It is the visible state of authentication.
