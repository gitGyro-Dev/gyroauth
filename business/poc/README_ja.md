# GyroAuth PoC 日本語概要

このディレクトリでは、GyroAuthのPoC候補、対象範囲、必要データ、評価指標、制約、次段階への移行条件を管理します。

## 最初の具体的PoC

最初のGyroAuth PoCパッケージは、特権アクセスを対象とします。

- [`privileged_access_poc_package.md`](privileged_access_poc_package.md)

基本構成：

```text
特権アクセス
+ オフラインログ評価
+ 必要に応じてShadow Mode
+ 本番制御なし
```

既存ログから特権セッションのTrajectoryを再構築し、次の2つを独立して出力できるかを評価します。

```text
Auth Decision
!=
Criterion Update Response
```

代表的な評価状態：

```text
AUTH_STABLE + FREEZE
```

これは、現在の特権セッションを直ちに停止しない一方で、その不確実な挙動を将来の正常基準へ取り込まない状態です。

## 特権アクセスを最初に選ぶ理由

特権アクセスは、VPN / ZTNAよりも最初の対象範囲を限定しやすいためです。

初期PoCは、次のように狭く設定できます。

- 特権ユーザー 5〜10名
- 対象システムまたはサービス 1つ
- 観察期間 2〜4週間
- ログソース 2〜4種類
- オフライン分析のみ

VPN / ZTNAでは、Identity、端末状態、ネットワーク、位置、プロキシ、ルーティング、物理的な接続環境などを扱う必要が生じやすく、最初のPoCとしては対象が広がりやすいため、第2候補とします。

## PoCの進行順序

1. 特権アクセスのオフラインログ評価
2. 特権アクセスのShadow Mode
3. ReviewまたはStep-up Authenticationとの限定連携設計
4. VPN / ZTNA向け評価パッケージ
5. AI Agent Governance向け探索パッケージ

各段階から本番制御へ自動的に移行することはありません。

## 最初のPoCで行うこと

- 既存ログの受領と品質確認
- セッション単位のイベント再構築
- Trajectoryの構築
- Auth Decisionの算出
- Criterion Update Responseの算出
- 既存ルール、PAM、SIEM、UEBA等の結果との比較
- Review対象候補の抽出
- Audit Traceの作成
- 結果報告書の作成

## 最初のPoCで行わないこと

- セッションの自動遮断
- 権限の自動剥奪
- 本番認証基準の自動更新
- Fail-close制御
- PAM、IAM、MFAの置き換え
- GyroAuth単独による侵害断定
- 24時間監視サービス

## 必須ログの最小セット

```text
timestamp
subject_id
session_id
target_id
action
result
source_system
```

特に `session_id` または、それに相当するセッション再構築情報が重要です。

セッション単位の関係を十分に復元できない場合、Trajectory評価の成立が困難になるため、PoCの延期または対象変更を検討します。

## PoC成功の基本条件

- 対象セッションの大部分を再構築できる
- Auth DecisionとCriterion Update Responseを両方出力できる
- 各Findingに再現可能なAudit Traceがある
- 両判断を分離する価値を示す事例が確認できる
- 本番認証・アクセス判断を変更しない
- 不足データ、制約、評価できない範囲を明示する

成功とは、攻撃防止を一般的に証明することではありません。

```text
PoC結果
!=
一般的なセキュリティ保証
```

## 顧客への説明例

GyroAuthの特権アクセスPoCでは、既存の認証やPAMを置き換えず、現在の管理者セッションが継続可能かと、その操作を将来の正常基準へ取り込んでよいかを別々に評価します。最初は既存ログを使ったオフライン分析であり、本番セッションの停止や権限変更は行いません。

## 関連文書

- [`privileged_access_poc_package.md`](privileged_access_poc_package.md) — 特権アクセスPoC本体
- [`offline_log_evaluation.md`](offline_log_evaluation.md) — 汎用オフライン評価モデル
- [`evaluation_framework.md`](evaluation_framework.md) — 共通評価方針
- [`../README_ja.md`](../README_ja.md) — 事業化全体の日本語概要

## 正本と運用

詳細なPoC仕様の正本は英語版パッケージとし、この日本語概要は顧客説明および日本語での検討の入口として更新します。

顧客向け資料を作成する際は、この文書を起点とし、顧客固有情報や未合意の費用・期間・性能保証は公開リポジトリへ記載しません。
