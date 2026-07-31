# GyroAuth Business / PoC 日本語概要

このディレクトリは、GyroAuthの実用化、事業化、共同研究、PoC獲得を検討・管理するための作業領域です。

## 目的

GyroAuthを研究成果のまま留めず、次の形へ接続できるかを検討します。

- 企業とのPoCまたは共同研究
- 認証・アクセスログの評価機能
- 適応型認証やUEBAに対する認証基準更新ガード
- セキュリティベンダーへの組み込み、OEM、技術ライセンス
- 技術コンサルティング、導入支援、評価サービス

事業化では、次の順序を重視します。

```text
第三者が理解できるか
→ 試したいと思うか
→ 導入価値を説明できるか
→ PoCまたは共同研究として実施できるか
→ 継続利用、契約、事業へ接続できるか
```

## 現在の事業化ポジション

GyroAuthの中心的な特徴は、現在の認証判断と、将来の認証基準更新判断を分離することです。

```text
Auth Decision
!=
Criterion Update Response
```

つまり、現在のアクセスやセッションを継続できるかという判断と、その挙動を将来の正常基準へ取り込んでよいかという判断を別々に行います。

現在の代表的な説明状態は次です。

```text
AUTH_STABLE + FREEZE
```

これは、現在の認証関係は直ちに停止しない一方で、不確実な挙動を将来の正常基準へ自動的に取り込まない状態を示します。

## 現在できていること

- Stability-based Authenticationの基本モデル
- Auth Decisionの4状態
  - `AUTH_STABLE`
  - `RECONVERGING`
  - `REAUTH_REQUIRED`
  - `AUTH_FAIL`
- Criterion Update Response
  - `ACCEPT`
  - `DEFER`
  - `FREEZE`
  - `REVIEW`
  - `ROLLBACK`
- 正常な環境変化、段階的な基準汚染、証拠ソース侵害を扱う決定論的シナリオ
- GitHub Pagesの公開研究デモ
- 論文、再現可能なコード、Release成果物

## 現在できていないこと

- 実企業環境での性能実証
- FAR、FRR、EERなどの定量評価
- 本番環境でのレイテンシ・スループット評価
- PAM、IAM、IdP、VPN、ZTNA、SIEM等との本番接続
- 本番API、SLA、24時間サポート
- 法規制対応やセキュリティ認証
- 一般的な安全性保証

そのため、現時点で提供すべきものは本番認証サービスではありません。

最初の提供形態は、既存ログを利用したオフライン評価またはShadow Mode PoCとします。

## 最初の具体的PoC

最初のPoC対象は、特権アクセスです。

```text
特権アクセス
+ オフラインログ評価
+ 必要に応じてShadow Mode
+ 本番制御なし
```

特権アクセスを最初に選ぶ理由は、VPN / ZTNAよりも対象範囲を限定しやすく、顧客課題とGyroAuthの違いを説明しやすいためです。

初期範囲の例：

- 特権ユーザー 5〜10名
- 対象システムまたはサービス 1つ
- 観察期間 2〜4週間
- ログソース 2〜4種類
- オフライン分析のみ

最初のPoCでは、セッション遮断、権限剥奪、認証基準の自動更新は行いません。

## 顧客への基本説明

### 非技術者向け

GyroAuthは、現在のアクセスが問題ないかだけでなく、その行動を将来の「正常」として学習してよいかを分けて判断する認証評価技術です。

### CISO・セキュリティ責任者向け

GyroAuthは、現在の特権セッション継続判断と、適応型認証基準への取り込み判断を分離し、不確実な挙動による基準汚染をレビュー対象として止めることを目指します。

### 認証・PAM・セキュリティベンダー向け

GyroAuthは、既存のPAM、IAM、SIEM、UEBAを置き換えず、特権セッションのTrajectory評価と認証基準更新ガードを追加する補助レイヤーです。

## 顧客説明時の禁止事項

次の表現は行いません。

- GyroAuthが攻撃を必ず防止する
- 現在のデモが本番認証サービスである
- PoC結果が一般的な安全性を保証する
- GyroAuthだけで侵害を断定できる
- 既存PAM、IAM、MFAをすぐに置き換えられる

必ず次を区別します。

```text
決定論的研究シナリオで確認済み
!=
実企業環境で有効性を実証済み
```

## ファイル運用方針

README、概要、外部説明に使用する文書には、日本語版を用意します。

推奨命名：

```text
README.md
README_ja.md

example.md
example_ja.md
```

内部検討メモや一時的な作業ログは、必要性に応じて日本語版を省略できます。

顧客説明用の中心文書は、この `README_ja.md` とし、事業化方針、PoC対象、顧客向け説明が変わるたびに更新します。

## 関連文書

- [`README.md`](README.md) — 英語版概要
- [`strategy/positioning.md`](strategy/positioning.md) — 英語ポジショニング
- [`strategy/market_use_case_assessment.md`](strategy/market_use_case_assessment.md) — 市場・ユースケース評価
- [`poc/README_ja.md`](poc/README_ja.md) — PoC日本語概要
- [`poc/privileged_access_poc_package.md`](poc/privileged_access_poc_package.md) — 特権アクセスPoC本体

## 更新責任

技術定義と実装の正本は、既存のGyroAuth研究・実装ファイルです。

この日本語概要は、顧客価値、PoC範囲、制約、提供形態を説明するための文書であり、技術仕様そのものを置き換えません。
