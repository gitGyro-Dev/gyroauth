# GyroAuth v2

**ズレを前提とした Stability-based Selection 認証**

---

## 🧭 レイヤー構造

```text
Gyro Logic   = 理論
GyroOS       = 実行系
GyroAuth     = 応用（本リポジトリ）
```

* Gyro Logic は Structure / Slice / Deviation / Stability を定義
* GyroOS は Deviation → Stability → Selection を計算
* GyroAuth はそれを使って認証判断を行う

👉 上位は下位に依存しない
👉 下位は上位を実装する
👉 混同は禁止

---

## 🧠 GyroAuthとは

GyroAuthは次のような認証システムです。

> 認証は一致ではない
> 👉 ズレの中で成立しているかを選択するものである

従来：

```text
一致しているか？
```

GyroAuth：

```text
このセッションは同一人物として成立しているか？
```

---

## 🔥 なぜ重要か

従来の認証は：

* 完全一致前提
* 静的なID
* 成功 or 失敗

しかし現実は：

* ノイズがある
* 状態は変化する
* 文脈依存

GyroAuthは：

👉 ズレ前提
👉 継続的認証
👉 選択による判断

---

## 🧩 コア定義

```text
認証 = Stability-based Selection
```

より正確には：

```text
Auth ⇔ 安定性に基づく選択
```

---

## ⚙️ 処理フロー

```text
Structure
↓
Slice（観測）
↓
Observation
↓
Δ（ズレ）
↓
Stability
↓
Selection
↓
認証判断
```

---

## 🧠 Multi-Sliceモデル

複数の観測軸を使う：

* Space（位置）
* Time（時間）
* Motion（動き）
* Device（端末）
* Behavior（操作）
* Network（通信）

👉 IDは点ではない
👉 複数Sliceにまたがる軌跡である

---

## 🔐 認証状態

```text
AUTH_STABLE
RECONVERGING
AUTH_FAIL
```

### AUTH_STABLE

安定している

### RECONVERGING

ズレ増加 → 再収束中

### AUTH_FAIL

崩壊 → 再認証必要

---

## 🔁 継続認証

認証は一度きりではない。

* 状態の変化
* ズレの増加
* 再収束可能性

👉 常に評価され続ける

---

## 🛡️ セキュリティ

対応する攻撃：

* リプレイ攻撃
* なりすまし
* 端末偽装
* 行動模倣

理由：

* 静的情報に依存しない
* 時系列依存
* 再現不能

👉 コピーでは通らない
👉 状態として成立する必要がある

---

## 📡 API（概念）

```text
POST /observe
POST /authenticate
POST /reconverge
GET  /session/{id}
```

---

## 🔗 GyroOSとの関係

GyroAuthは以下を計算しない：

* Deviation
* Stability
* Selection

👉 GyroOSが提供する

GyroAuthは：

* ポリシー
* リスク制御
* 認証判断

のみを担当

---

## 🧪 PoC

以下を検証する：

* ズレ前提でも認証成立
* 継続認証
* 攻撃耐性
* 再収束

---

## 💼 ユースケース

* パスワードレス認証
* 継続セッション監視
* デバイス信頼
* 異常検知
* 次世代Zero Trust

---

## 📄 ドキュメント

以下から開始：

* docs/00_positioning.md
* docs/01_auth_model.md
* docs/03_decision_policy.md
* docs/08_poc_design.md

---

## 📦 構成

```text
docs/        → 仕様
app/         → 実装
scripts/     → デモ
examples/    → サンプル
archive_v1/  → 旧版
```

---

## 🧠 一行定義

GyroAuthとは：

> ズレの中で成立しているかを判断する認証システム

---

## 🔴 最後に

認証とは一致ではない。

👉 変化の中で成立しているかどうかである
