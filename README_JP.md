## 🚀 Latest Release

GyroAuth v2.0 (PoC)  
https://github.com/gitGyro-Dev/gyroauth/releases/tag/v2.0.0

# GyroAuth vNext

**状態収束に対する安定性に基づく認証**

---

## スタック上の位置づけ

```text
Gyro Logic   = 理論層
GyroOS       = 実行系 / 実装層
GyroAuth     = 応用層（このリポジトリ）
```

* Gyro Logic は **Structure / Slice / Deviation / Stability** を定義する
* GyroOS は **Gyro Process + Operator Response** を実行する
* GyroAuth はその結果を **認証判断** として解釈する

GyroAuth は Gyro Logic を再定義しない。  
GyroAuth は GyroOS を再実装しない。  
GyroAuth は GyroOS の上で動作する応用層である。

---

## コア定義

```text
認証 = State Convergence に対する Stability-based Selection
```

State Convergence は、GyroAuth が観測する現象である。  
Stability-based Selection は、その現象を認証判断へ変換する方法である。

短く言えば：

```text
GyroAuth は、多次元状態が期待される Identity Trajectory へ
収束しているかを観測し、
Stability、Deviation、Operator Response、History に基づいて
Auth Decision を選択する。
```

---

## 更新された Core Flow（GyroOS v4 整合）

```text
GyroOS:
Gyro Processₙ
→ Operator Responseₙ
→ Gyro Processₙ₊₁

GyroAuth:
Stability-based Selection
→ Auth Decision
```

---

## 重要な補正

GyroAuth は認証を次のような単純処理へ戻さない。

```text
observe → evaluate → update
```

GyroAuth は以下に依存する。

```text
POST /loop/step
```

これは以下を返す。

```text
slice-done = X + Δ
Stability
Operator Response
History
```

GyroAuth は、これらの GyroOS 実行結果を、応用層の認証判断へ写像する。

---

## vNext Loop-aligned PoC

GyroAuth vNext では、GyroOS v4 `/loop/step` 前提に沿った Loop-aligned PoC を追加する。

この vNext PoC は GyroOS 全体を実装するものではない。  
GyroAuth の解釈層を検証するものである。

```text
GyroOS /loop/step output
→ slice-done / Stability / Operator Response / History
→ State Convergence に対する Stability-based Selection
→ Auth Decision
```

確認済みの状態遷移：

```text
AUTH_STABLE
→ RECONVERGING
→ REAUTH_REQUIRED
→ AUTH_STABLE
→ AUTH_FAIL
```

重要：

```text
Re-auth ≠ AUTH_FAIL
Re-auth → REAUTH_REQUIRED
```

参照：

```text
docs/14_vnext_loop_poc.md
app/vnext/main.py
examples/vnext/
```

---

## Auth Decision States

```text
AUTH_STABLE
RECONVERGING
REAUTH_REQUIRED
AUTH_FAIL
```

* `AUTH_STABLE` — セッション状態が期待される Identity Trajectory へ収束している
* `RECONVERGING` — ズレは増加しているが、再収束可能性が残っている
* `REAUTH_REQUIRED` — 明示的な追加認証が必要。ただし、本人性が崩壊したとは限らない
* `AUTH_FAIL` — Trajectory continuity が崩壊し、認証を継続できない

---

## Final Statement

GyroAuth は raw input によって駆動されるのではない。

GyroAuth は以下によって駆動される。

```text
State Convergence
+ Stability
+ Operator Response
+ History
→ Stability-based Selection
→ Authentication
```

認証とは完全一致ではない。

変化の中で、本人性がなお成立しているかどうかである。
