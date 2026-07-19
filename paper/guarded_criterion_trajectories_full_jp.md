# 適応型認証におけるGuard付きCriterion Trajectory：現在のアクセス判断と将来の認証基準更新の分離

## 要旨

適応型認証は、端末、ネットワーク、場所、役割、行動などの正当な変化へ対応しなければならない。認証基準が一切変化しなければ硬直的になる一方、観測された挙動を独立した制御なしに取り込む基準は、第二の攻撃面を生む。すなわち、不正な挙動が段階的に新しい通常状態として吸収される可能性がある。本稿は、認証基準の変化を自動的なプロファイル更新としてではなく、Guard付きのTrajectoryとして扱うGyroAuth拡張を提案する。本モデルは、現在の認証判断と、将来の認証に使用する基準を変更する判断とを分離する。Criterion Update Candidateは、現在の観測、Context、History、および有効な基準から生成されるが、GuardとCriterion Update Responseを経て、`ACCEPT`、`DEFER`、`FREEZE`、`REVIEW`、`ROLLBACK`のいずれかが選択された後にのみ有効化される。本稿では、Subject EvaluationとCriterion Integrity Evaluationの分離、有限なCriterion Update State Machine、および直接採用モデルとGuard付き採用モデルを比較する決定論的PoCを示す。正当な新規端末シナリオでは、Guard付きモデルはChallenge確認まで更新を保留し、その後、限定的な更新を採用した。段階的な許容領域拡張攻撃では、直接更新モデルが攻撃参照値を許容するまで拡張した一方、Guard付きモデルは許容前に更新を凍結した。単一Evidence source侵害では、見かけ上妥当なEvidenceが存在しても自動採用を阻止した。これらはSyntheticな仮定下で提案構造が実行可能であることを示すが、本番環境の安全性、普遍的な攻撃検知、False Accept率やFalse Reject率を保証するものではない。

**キーワード:** 適応型認証、継続認証、Criterion poisoning、Guard付き適応、Trajectory、Criterion Integrity、GyroAuth

---

## 1. はじめに

認証システムは、利用者の状態、端末状態、ネットワーク条件、場所、行動、運用Contextが時間とともに変化する環境で動作する。固定プロファイルや固定閾値だけでは、正当な変化を十分に扱えない可能性がある。利用者は端末を交換し、旅行し、役割を変更し、既存の作業手順を変え、緊急操作を行うことがある。したがって、適応型認証には、評価基準自体が変化できる仕組みが必要である。

しかし、適応は別のセキュリティ問題を生む。観測された挙動が基準へ直接取り込まれる場合、不正な挙動が繰り返されることで、将来の判断に用いる基準が徐々に移動、拡張、弱化、または汚染される可能性がある。システムは現在のアクセス関係を適切に評価しながら、同時に、将来のアクセスを評価する規則を破壊してしまうことがある。

本稿は、この区別を対象とする。中心命題は次である。

```text
dynamic criterion
!=
unconstrained self-update
```

問題は、現在のAccess SubjectがExpected Identityとの関係で許容可能かどうかだけではない。その判断の基礎となるAuthentication Criterion自体が、引き続き適切であるかも評価しなければならない。

そこで、次の二つの問いを分離する。

```text
Subject Question:
現在のAccess Subjectは、Expected Identityとの関係で、
なお許容可能か。
```

```text
Criterion Question:
現在のAuthentication Criterionは、
その関係を評価する基準として、なお許容可能か。
```

この結果、二つの判断空間を明確に分離する。

```text
Auth Decision
!=
Criterion Update Response
```

さらに、更新候補と正式な基準も分離する。

```text
Criterion Update Candidate
!=
Accepted Criterion
```

この分離により、次のような組合せを許容できる。

```text
AUTH_STABLE + FREEZE
```

すなわち、現在のアクセス関係は一時的に継続可能である一方、将来のCriterion適応は停止できる。

本稿の主な貢献は次の通りである。

1. Subject EvaluationとCriterion Integrity Evaluationを分離する二重継続評価モデルを定義する。
2. Criterion変化を、無検証な更新列ではなく、追跡可能なCriterion Trajectoryとして表現する。
3. `ACCEPT`、`DEFER`、`FREEZE`、`REVIEW`、`ROLLBACK`からなるGuard付きCriterion Updateを定義する。
4. 現在の認証判断と将来のCriterion変更を分離する有限状態機械を定義する。
5. 正当な適応、段階的Poisoning、単一Evidence source侵害について、直接採用モデルとGuard付き採用モデルを比較する決定論的PoCを実装する。
6. 仮定、支持される主張、条件付き主張、非保証を明示する。

---

## 2. 背景と位置づけ

### 2.1 GyroAuthの基礎

GyroAuthは認証を次のように定義する。

```text
Authentication
=
Stability-based Selection over State Convergence
```

GyroAuthは次のレイヤー関係に位置づけられる。

```text
Gyro Logic   = Theory
GyroOS       = Execution System
GyroAuth     = Authentication Application
```

本研究は、次のGyro Logic Coreを再定義しない。

```text
Structure
↓
Slice
↓
Stability
```

また、GyroOS runtimeやcanonical Operator Responseも再定義しない。本稿の貢献はGyroAuth application layerに限定される。

### 2.2 既存GyroAuth研究との関係

基礎GyroAuth論文は認証モデルそのものを定義する。Trajectory-Based Vulnerability Response研究は、ログイン後の操作系列とセキュリティResponseへTrajectory評価を適用する。本稿が対象とするのは別の対象である。

```text
Authentication Criterion
and
Criterion Update Process
```

本稿は、Stability-based Selectionに用いる測定・選択基準が、引き続き使用可能な状態にあるかを検討する。

### 2.3 Related Workの対象

最終投稿前には、以下の最新研究との比較が必要である。

```text
Adaptive Authentication
Continuous Authentication
Risk-Based Authentication
Behavioral Biometrics
Concept Drift
Online Learning Security
Data Poisoning
Model Poisoning
Zero Trust
UEBA
Anomaly Detection
```

本作業稿では、これらに対する新規性を最終確定していない。投稿前に一次文献を中心としたRelated Work調査と参考文献一覧の整備が必要である。

---

## 3. 用語と適用範囲

### 3.1 Access Subject

**Access Subject**は、認証Context内で現在評価されているアクセスおよび操作の発生源である。正当な利用者、Credential thief、Session hijacker、relay-mediated operator、bot、remote controller、または混在した発生源であり得る。

```text
Access Subject
!=
Verified Identity
```

### 3.2 Expected Identity

**Expected Identity**は、変化するSessionやContextをまたいで、現在のAccess Subjectが同一の認証Identityとして評価される際の持続的な参照関係である。Credential、端末、場所、行動はEvidenceになり得るが、それ自体がExpected Identityではない。

```text
Evidence
!=
Identity
```

### 3.3 Observed Evidence

**Observed Evidence**は、観測源およびSliceを通じてGyroAuthへ提供される情報である。Credential結果、端末状態、行動状態、時間、空間、ネットワーク、Motion、操作順序、権限遷移、Challenge結果、Response Evidence、History、Criterion update provenanceなどを含み得る。

### 3.4 Observed Access Trajectory

**Observed Access Trajectory**は、現在のOrientation、Context、SliceのもとでLocal Authentication Realization間の許容可能な関係を辿ることで得られる可読な関係的構成である。単なる時系列ログやFeature vector列ではない。

```text
History
!=
Trajectory
```

### 3.5 Authentication Relation

**Authentication Relation**は、SessionおよびContext内で現在評価されているAccess SubjectとExpected Identityとの関係である。GyroAuthは、この関係を継続可能とみなすかを選択する。

### 3.6 Authentication Criterion

**Authentication Criterion**は、Evidence、Deviation、Stability、Trajectory、History、およびResponse条件を解釈するためにGyroAuthが用いるContext-relativeな評価基準である。

```text
Authentication Criterion
!=
Fixed Identity Profile
```

### 3.7 Criterion Update Candidate

**Criterion Update Candidate**は、現在のCriterion、新しいEvidence、Context、Historyから生成される次期Criterion候補である。生成時点ではまだ有効ではない。

```text
Criterion Update Candidate
!=
Accepted Criterion
```

### 3.8 Criterion Trajectory

**Criterion Trajectory**は、Criterion変化を許容可能または不許容な遷移として追跡できる関係的構成である。更新理由、Evidence、provenance、変化量、方向、速度、識別能力への影響、Response、Rollback linkageを含む。

### 3.9 Criterion Integrity

**Criterion Integrity**は、Authentication Criterionとその更新過程が、Expected Identityとの認証関係を評価する基準として、許容可能かつ追跡可能な状態を維持していることである。

Criterion Integrityは自己証明を意味しない。Protected Anchor、Evidence provenance、History、Rollback Point、Response ruleに依存する。

---

## 4. Threat Model

### 4.1 Security Objective

本モデルは次の二つを保護対象とする。

1. 現在のAuthentication Relationが継続可能かを評価する能力。
2. 攻撃者がAuthentication Criterionを移動、拡張、弱化、または汚染し、不正な挙動を通常として取り込ませることを抑制する能力。

### 4.2 保護対象

```text
Authentication Relation
Authentication Criterion
Criterion Update Process
Criterion Trajectory
Trusted History
Rollback Points
Decision separation
```

### 4.3 Threat Class

Threat Modelは以下を含む。

```text
Credential theft
Session hijacking
Relay attack
Gradual behavioral mimicry
Criterion poisoning
Evidence-source compromise
Multi-source coordinated compromise
```

PoCで中心的に扱うのはCriterion poisoningである。

### 4.4 Criterion poisoning

Criterion poisoningとは、攻撃者がEvidenceまたはObserved Trajectoryに影響し、不正な状態や操作を有効なCriterionへ段階的に取り込ませる攻撃である。

主な細分類は次の通りである。

```text
Region expansion
Criterion translation
Evidence-priority poisoning
Recovery-expectation poisoning
Challenge-requirement weakening
Context-rule poisoning
History-window poisoning
Rollback-link poisoning
Slow contraction
Response-policy poisoning
```

### 4.5 Trusted Assumption

最小モデルでは、次の少なくとも一つが攻撃者の同時支配外にあると仮定する。

```text
独立したEvidence source
Protected Policy Anchor
改ざんされていないAudit linkage
検証済みRollback Point
```

すべてのEvidence source、Anchor、History、Rollback Pointが侵害された場合、本モデルは確実な識別や回復を主張しない。

---

## 5. Formal Security Model

### 5.1 離散評価段階

評価は有限な段階で進行する。

```text
t = 0, 1, 2, ...
```

各段階は、`/auth/step`呼出し、観測区間、Security event、Challenge結果、またはCriterion update evaluationに対応し得る。

### 5.2 判断空間

Auth Decision集合は次である。

```text
D_auth = {
  AUTH_STABLE,
  RECONVERGING,
  REAUTH_REQUIRED,
  AUTH_FAIL
}
```

Criterion Update Response集合は次である。

```text
D_crit = {
  ACCEPT,
  DEFER,
  FREEZE,
  REVIEW,
  ROLLBACK
}
```

両者は交換可能ではない。

### 5.3 Candidate生成

時点`t`の有効なCriterionを次とする。

```text
A_t
```

Candidateは次で生成される。

```text
A*_(t+1)
=
U(A_t, T_t^obs, C_(t+1), E_t, H_t)
```

Candidate生成はCandidate採用ではない。

```text
A*_(t+1)
!=
A_(t+1)
```

### 5.4 Guard

Candidateは次のGuardで評価される。

```text
G_t
=
Guard(
  A_t,
  A*_(t+1),
  T_t^obs,
  C_(t+1),
  E_t,
  H_t,
  P_t
)
```

最小Guard vectorは次を含む。

```text
provenance
cross-evidence consistency
challenge confirmation
update magnitude
update rate
update direction
discrimination preservation
rollback linkage
evidence-source integrity
```

### 5.5 Non-compensation rule

Critical Guardの失敗は平均化によって相殺されない。

```text
CriticalGuardFail
→
Criterion Update Response != ACCEPT
```

これにより、高い平均スコアによってsource integrityやdiscrimination preservationの失敗が隠されることを防ぐ。

### 5.6 Criterion Update Response

Responseは次で選択される。

```text
D_crit_t
=
Pi_crit(G_t, Q_t, H_t)
```

有効なCriterionの遷移は次である。

```text
A_(t+1) = A*_(t+1)
when D_crit_t = ACCEPT
```

```text
A_(t+1) = A_t
when D_crit_t ∈ {DEFER, FREEZE, REVIEW}
```

```text
A_(t+1) = A_tau
when D_crit_t = ROLLBACK and tau < t
```

### 5.7 Subject Evaluation

Subject EvaluationはCriterion adaptationから独立している。Observed Access Trajectory、Deviation、Stability、Context、History、Response Evidenceを用いてAuth Decisionを選択する。

Criterion Update ResponseをAuth Decisionから直接推定してはならない。

---

## 6. Criterion Update State Machine

### 6.1 Criterion State

本モデルは次のCriterion Stateを定義する。

```text
STABLE
ADAPTING
UNCERTAIN
FROZEN
UNDER_REVIEW
COMPROMISED
ROLLED_BACK
```

### 6.2 Response semantics

#### ACCEPT

Candidateを次の有効なCriterionとして採用する。

#### DEFER

追加Evidence、Challenge結果、または観測を待つ間、現在のCriterionを維持する。

#### FREEZE

更新経路自体が危険と判断されるため、適応的採用を停止する。Subject Evaluationは独立して継続可能である。

#### REVIEW

自動採用を停止し、外部Policy、管理者、より強いVerification path、独立Validatorへ判断を移す。

#### ROLLBACK

Audit trailを削除せず、検証済みの過去Criterionへ復帰する。

### 6.3 区別

```text
DEFER
!=
FREEZE
```

`DEFER`はCandidateへの支持不足を意味する。`FREEZE`はAdaptive path自体の危険を意味する。

```text
REVIEW
!=
DEFER
```

`REVIEW`は判断経路または判断主体を変更する。

---

## 7. PoC設計

### 7.1 比較モデル

PoCは同一のCandidate generatorを用いる二つのモデルを比較する。

#### Model U: Unconstrained Update

```text
Observation
→ Candidate
→ Direct Adoption
```

#### Model G: Guarded Update

```text
Observation
→ Candidate
→ Guard
→ Criterion Update Response
→ Effective Criterion Transition
```

Model Uは意図的に安全性を欠いた比較Baselineであり、既存の全Adaptive Authentication systemを代表するものではない。

### 7.2 Criterion表現

有効なCriterionは次で表す。

```text
A_t = (
  mu_t,
  width_t,
  provenance_requirement_t,
  challenge_requirement_t,
  rollback_integrity_t
)
```

`mu_t`はCriterion center、`width_t`は許容領域幅である。この一次元表現は最小実行抽象であり、本番Identity modelを主張するものではない。

### 7.3 Candidate generator

両モデルは次を用いる。

```text
mu*_(t+1)
=
mu_t + eta_mu (y_t - mu_t)
```

```text
width*_(t+1)
=
width_t
+ eta_width max(0, |y_t - mu_t| - width_t)
```

両モデルの違いはCandidate adoptionにある。

### 7.4 Scenario

最小Scenarioは次である。

```text
N1: Legitimate New Device Transition
P1: Gradual Region Expansion Poisoning
C1: Single Evidence Source Compromise
```

### 7.5 実装

実装はPython標準ライブラリのみを使用し、決定論的なSynthetic inputを用いる。

Artifactは次である。

```text
scripts/simulate_guarded_criterion_update.py
examples/criterion_update/scenarios.json
results/criterion_update_summary.json
```

実装はCandidate、Guard result、Auth Decision、Criterion Update Response、Criterion State、有効Criterion、Assertionを記録する。

---

## 8. 結果

### 8.1 Scenario N1：正当な新規端末移行

Guard付きモデルは次を出力した。

```text
Auth Decision:
REAUTH_REQUIRED
→ AUTH_STABLE
→ AUTH_STABLE
```

```text
Criterion Update Response:
DEFER
→ ACCEPT
→ ACCEPT
```

最終値は次であった。

```text
mu    = 0.234
width = 0.120
```

最初のCandidateはChallenge確認前であったため採用されなかった。再認証成功とcross-evidence consistency確認後、限定的な更新が採用された。許容領域幅は拡張しなかった。

この結果は、Guard付き適応が非適応と同義ではないことを示す。

```text
Guarded
!=
Non-adaptive
```

### 8.2 Scenario P1：段階的Region Expansion Poisoning

攻撃参照値は次である。

```text
y_attack = 0.62
```

#### Model U

最終値は次であった。

```text
mu    = 0.3969728
width = 0.277212
```

結果は次である。

```text
attack reference admissible = true
```

直接更新BaselineはすべてのCandidateを採用し、Criterionが移動・拡張して攻撃参照値を許容した。

#### Model G

最終値は次であった。

```text
mu    = 0.200
width = 0.120
freeze stage = 2
```

結果は次である。

```text
attack reference admissible = false
```

Response pathは次であった。

```text
DEFER
→ FREEZE
→ FREEZE
→ FREEZE
→ FREEZE
```

有効なCriterionは信頼済みの初期状態に維持された。

Stage 2では次の組合せが得られた。

```text
AUTH_STABLE + FREEZE
```

これは次の違いを実行結果として示す。

```text
current subject acceptance
```

と、

```text
permission to redefine future acceptance
```

は同一ではない。

### 8.3 Scenario C1：単一Evidence source侵害

Guard付きモデルは次を出力した。

```text
FREEZE
→ FREEZE
```

最終値は次であった。

```text
mu    = 0.200
width = 0.120
```

Candidateは一度も採用されなかった。見かけ上強いEvidence値があっても、低いsource integrityと弱いcross-evidence consistencyを相殺できなかった。

```text
single Evidence match
!=
criterion update acceptance
```

### 8.4 Assertion

実装した7個のAssertionはすべて成功した。

```text
PASS N1 guarded model eventually accepts supported adaptation
PASS P1 unconstrained model makes attack reference admissible
PASS P1 guarded model freezes criterion adaptation
PASS P1 guarded model keeps attack reference non-admissible
PASS C1 guarded model does not accept compromised source update
PASS C1 guarded model freezes or reviews
PASS Auth Decision and Criterion Update Response remain separate
```

---

## 9. 考察

### 9.1 主結果

PoCは、現在の認証判断と、将来の認証基準を変更する許可を、独立した実行可能な判断として表現できることを示した。

現在のAccess Subjectが現行Criterionのもとで一時的に許容可能であっても、観測された更新経路が危険である場合がある。`AUTH_STABLE + FREEZE`は、この状態を直接表現する。

### 9.2 Guard付き適応は適応を否定しない

N1では、Challenge confirmation、provenance、cross-evidence consistencyが満たされた後に、正当な変更が採用された。提案モデルはCriterion固定を要求しない。

### 9.3 繰り返し観測だけでは不十分

P1は、反復だけでは正当性が成立しないことを示す。

```text
repeated observation
!=
new normal automatically
```

小さな局所Deviationが累積し、大きなCriterion driftになる可能性がある。そのためGuardは、一段階の変化量だけでなく、累積方向、拡張、識別能力低下、Evidence qualityを評価する。

### 9.4 Criterion Integrityは自己証明ではない

本モデルは、前提なしに自らの信頼性を証明しない。Criterion IntegrityはProtected Anchor、独立Evidence、保持されたHistory、有効なRollback linkageに依存する。

### 9.5 GyroAuthとの関係

提案は、Criterionとその更新過程をGyroAuth application layerの評価対象に含める拡張である。Gyro Logic CoreやGyroOS execution contractは変更しない。

---

## 10. Security Claim

### 10.1 構造的に実証された主張

実装した決定論的仮定下では、次を支持できる。

1. Criterion Update CandidateとAccepted Criterionを分離できる。
2. Auth DecisionとCriterion Update Responseを独立したDecision streamとして維持できる。
3. 十分な支持のある正当な限定更新を採用できる。
4. Candidate直接採用は累積的Criterion expansionを生じ得る。
5. 実装したP1では、攻撃参照値許容前にGuard付きResponseが更新を凍結できる。
6. 実装したC1では、Evidence source侵害時にCriterion adoptionを阻止できる。
7. `AUTH_STABLE + FREEZE`を実行できる。

### 10.2 条件付き主張

次の主張には追加の仮定と検証が必要である。

```text
P1以外のCriterion poisoning containment
Rollback-supported recovery
Credential theft resistance
Session hijacking detection
Relay attack detection
Multi-source compromise resistance
```

### 10.3 支持されない主張

本研究は次を立証しない。

```text
Criterion poisoningの完全防止
すべての攻撃者の検知
False Acceptゼロ
False Rejectゼロ
完全なIdentity proof
全EvidenceおよびAnchor侵害下の安全性
本番性能
Privacy guarantee
Formal proof of correctness
Statistical generalization
```

---

## 11. 限界

### 11.1 Syntheticかつ決定論的な入力

Scenarioは手作業で指定された決定論的入力であり、実利用者母集団の分布を表さない。

### 11.2 一次元Criterion

Criterion centerとwidthはScalarである。本番システムでは、多次元状態および関係表現が必要である。

### 11.3 縮約されたTrajectory proxy

PoCはTrajectory ContinuityとStabilityの縮約数値Proxyを用いる。これは広い関係的定義を置き換えるものではない。

### 11.4 手動設定されたThreshold

Guard thresholdとCoefficientは明示されているが、実データによって最適化されていない。

### 11.5 False Accept / False Reject率未測定

本研究は状態遷移構造を示すものであり、実運用上の認証精度を示さない。

### 11.6 攻撃種類が限定的

実行Scenarioは、正当な適応一件、Gradual Expansion一件、Single-source compromise一件である。Translation poisoning、Evidence-priority poisoning、Challenge weakening、History-window poisoning、Rollback-link poisoningは今後の課題である。

### 11.7 本番統合なし

Cryptographic protocol、Hardware attestation、本番GyroOS execution、Privacy-preserving storage、Distributed Evidence collection、Resource benchmarkは含まれない。

### 11.8 Related Work未完了

一次文献や標準との比較が完了するまで、新規性主張は暫定的である。

---

## 12. 今後の課題

今後の研究課題は次である。

1. 検証済みRollback executionを実装する。
2. Criterion translation poisoningを追加する。
3. Evidence-priority poisoningとChallenge weakeningを追加する。
4. ThresholdおよびCoefficientのSensitivity analysisを行う。
5. 正当な変化に対するFalse-positive比較を追加する。
6. Criterionを多次元状態・関係へ拡張する。
7. 計算量、Storage、Energy costを測定する。
8. 実データまたは現実的なAuthentication telemetryで評価する。
9. Related WorkおよびStandard比較を完了する。
10. Criterion History保持に関するPrivacyとGovernanceを評価する。

---

## 13. 結論

適応型認証には、正当な変化へ対応できるCriterionが必要である。しかし、観測からCriterionへの直接取り込みは、不正な挙動が段階的に通常状態を再定義するPoisoning surfaceを生む。

本稿は、Criterion changeをGuard付きTrajectoryとして扱うGyroAuth拡張を提案した。本モデルは、現在の認証判断と、将来のCriterionを変更する判断を分離する。Candidateは生成されるが、GuardとCriterion Update Responseが`ACCEPT`、`DEFER`、`FREEZE`、`REVIEW`、`ROLLBACK`のいずれかを選択するまで有効化されない。

決定論的PoCでは、正当な新規端末適応が支持確認後に採用され、段階的Criterion expansionが攻撃参照値許容前に凍結され、Evidence source侵害時にはCandidate採用が阻止された。`AUTH_STABLE + FREEZE`は、現在のアクセス継続と将来のCriterion変更を独立して評価できることを示した。

本研究は構造的・実行可能な実証であり、本番Security guaranteeではない。中心命題は次である。

```text
dynamic criterion
!=
unconstrained self-update
```

---

## 参考文献

最終参考文献一覧は、Adaptive Authentication、Continuous Authentication、Behavioral Biometrics、Concept Drift、Online Learning Security、Poisoning attack、Zero Trust、UEBA、Anomaly Detectionに関する最新の一次文献調査後に追加する。

---

## AI支援ツールの使用

本稿の作成にあたり、構成整理、草稿作成補助、表現調整、整合性確認のためにAI支援ツールを使用した。本文の内容、主張、参考文献、最終原稿については著者が確認・編集し、全責任を負う。