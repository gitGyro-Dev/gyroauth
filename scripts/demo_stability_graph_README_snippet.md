# scripts/demo_stability_graph.py

This script generates a visual GyroAuth v2 demo:

- Stability timeline
- Slice stability breakdown
- CSV demo data

## Run

```bash
python scripts/demo_stability_graph.py
```

## Output

```text
outputs/demo_stability_data.csv
outputs/stability_timeline.png
outputs/slice_breakdown.png
```

## Demo Story

```text
AUTH_STABLE
→ small drift
→ RECONVERGING
→ recovery
→ AUTH_STABLE
→ attack
→ AUTH_FAIL
```
