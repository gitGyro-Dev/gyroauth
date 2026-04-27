# GyroAuth v2 — Demo Scenarios & Visualization

---

## 🧭 Purpose

This document defines how GyroAuth v2 should be demonstrated.

The goal is to make the following immediately clear:

- Authentication is not matching
- Identity is dynamic
- Deviation is normal
- Stability determines identity
- Recovery is possible
- Attacks break stability

---

## ■ Core Message

Authentication is not exact matching.
It is whether identity still holds under change.

---

## ■ Demo Story (Full Flow)

AUTH_STABLE
↓
Small Drift
↓
RECONVERGING
↓
Recovery
↓
AUTH_STABLE
↓
Attack
↓
AUTH_FAIL

👉 この流れを「見せる」ことがすべて

---

## ■ Scenario 1 — Normal Login

### 状態
- known device
- normal behavior
- expected context

### 結果
AUTH_STABLE

### 可視化
- Stability: 高い（0.9以上）
- グラフ: 横ばい（安定）

### 投資家メッセージ
GyroAuth allows access when identity is stable.

---

## ■ Scenario 2 — Small Drift

### 状態
- slight behavior change
- small context variation

### 結果
AUTH_STABLE または RECONVERGING

### 可視化
- Stability: 少し低下（0.8〜0.9）
- グラフ: 小さな揺れ

### 投資家メッセージ
Real users are not identical every moment.
GyroAuth tolerates natural variation.

---

## ■ Scenario 3 — Re-convergence

### 状態
- 一時的なズレ
- 軽微な異常

### 結果
RECONVERGING → AUTH_STABLE

### 可視化
- Stability: 一度低下 → 回復
- グラフ: V字回復

### 投資家メッセージ
GyroAuth recovers identity instead of failing immediately.

---

## ■ Scenario 4 — Attack / Hijack

### 状態
- device mismatch
- behavior anomaly
- network anomaly

### 結果
AUTH_FAIL

### 可視化
- Stability: 急落
- グラフ: 急激なドロップ

### 投資家メッセージ
Copied identity does not hold as a stable state.

---

## ■ Scenario 5 — Step-up / Controlled Recovery

### 状態
- 中程度のリスク
- 不安定だが完全崩壊ではない

### 結果
RECONVERGING → AUTH_STABLE or AUTH_FAIL

### 可視化
- Stability: 中程度
- 状態: 黄色（RECONVERGING）

### 投資家メッセージ
GyroAuth enables controlled escalation instead of binary rejection.

---

# 📊 Stability Visualization

---

## ■ 1. Stability Timeline

- 折れ線グラフ（時間 × Stability）

意味:
- 平坦 → 安定
- 小さな揺れ → 許容範囲
- 低下 → ドリフト
- 急落 → 攻撃
- 回復 → 再収束

---

## ■ 2. Slice Breakdown

- Device
- Behavior
- Time
- Space
- Network
- Motion

👉 どこが壊れているか可視化

---

## ■ 3. Auth State Indicator

- AUTH_STABLE → 緑
- RECONVERGING → 黄
- AUTH_FAIL → 赤

---

## ■ 4. Event Overlay

- device change
- network anomaly
- behavior jump

👉 Stability変化の原因を表示

---

## ■ 5. Reconvergence Window

- 黄色の帯で表示

👉 GyroAuthの特徴（即失敗しない）

---

# 🖥️ Recommended Demo Dashboard

## Panel 1 — Current State
- 状態
- Stability
- Risk

## Panel 2 — Stability Graph
- 時系列
- イベント

## Panel 3 — Slice Status
- 各Sliceの状態

## Panel 4 — Event Log
- 状態変化ログ

---

# ■ 90秒デモ構成

1. ログイン
2. 小さなズレ
3. RECONVERGING
4. 回復
5. 攻撃
6. FAIL

---

# ■ 投資家が理解すべきこと

- 静的認証ではない
- 継続評価
- 回復可能
- コピー不可
- 状態ベース

---

# 🔴 Final Statement

If stability cannot be seen,
the value of GyroAuth cannot be understood.

Visualization is the product.
