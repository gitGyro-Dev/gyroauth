# GyroAuth v2 — UI Wireframe

---

## 🧭 Purpose

This document defines the UI structure for GyroAuth v2.

The goal is:

- Explain the system in one screen
- Make stability visible
- Show identity as a dynamic state
- Demonstrate deviation, recovery, and failure

---

## ■ Core Concept

Authentication is not a point.
It is a continuously evaluated state.

---

## ■ One-Screen Layout (Investor View)

+------------------------------------------------------+
|                  GyroAuth Dashboard                  |
+------------------------------------------------------+

| [A] CURRENT STATE       | [B] STABILITY SCORE        |
|------------------------|----------------------------|
| AUTH_STABLE            | 0.92                       |
| Risk: LOW              | Trend: Stable              |

+------------------------------------------------------+

| [C] STABILITY TIMELINE (MAIN GRAPH)                  |
|------------------------------------------------------|
|    1.0 ────────────────                             |
|        ────────╮                                   |
|    0.8         ╰───╮                                |
|    0.6              ╰─────╮                         |
|    0.4                    ╰─── Attack               |
|    0.2                         ▼                    |
|    0.0 ─────────────────────────────────────────    |
|        t0   t1   t2   t3   t4   t5   t6             |

+------------------------------------------------------+

| [D] SLICE STATUS                                     |
|------------------------------------------------------|
| Device   ████████ 0.95 (OK)                         |
| Behavior ███████░ 0.88 (OK)                         |
| Time     ████████ 0.91 (OK)                         |
| Space    ██████░░ 0.80 (Drift)                      |
| Network  █████░░░ 0.72 (Warning)                    |

+------------------------------------------------------+

| [E] EVENT LOG                                        |
|------------------------------------------------------|
| t1: login success                                   |
| t2: slight behavior drift                           |
| t3: RECONVERGING triggered                          |
| t4: stability recovered                             |
| t5: network anomaly detected                        |
| t6: AUTH_FAIL                                       |

+------------------------------------------------------+

---

## ■ Panel Definitions

[A] Current State:
- AUTH state
- Risk level

[B] Stability Score:
- Numeric score (0.0 – 1.0)
- Trend

[C] Stability Timeline:
- Time vs Stability graph
- Shows drift, recovery, collapse

[D] Slice Breakdown:
- Device / Behavior / Time / Space / Network / Motion

[E] Event Log:
- System events and transitions

---

## ■ UX Principles

- Understandable in 5 seconds
- Visual-first
- Show cause and effect
- Avoid raw data dumps

---

## 🔴 Final Statement

The UI is not a dashboard.

It is the explanation of the system itself.
