# 適応型認証におけるGuard付きCriterion Trajectory：現在の認証判断と将来の認証基準更新の分離

**著者:** 川上俊太郎  
**プロジェクト:** GyroAuth  
**原稿状態:** 投稿候補稿

## 要旨

適応型認証は、端末、ネットワーク、場所、役割、行動などの正当な変化へ対応しなければならない。認証基準が一切変化しなければ硬直的になる一方、観測された挙動を独立した制御なしに取り込む認証基準は、追加の攻撃面を生む。すなわち、不正な挙動が段階的に新しい通常状態として吸収される可能性がある。本稿は、認証基準の変化を自動的なプロファイル更新としてではなく、Guard付きCriterion Trajectoryとして扱うGyroAuth拡張を提案する。本モデルは、現在の認証判断と、将来の認証に用いる基準を変更する判断とを分離する。Criterion Update Candidateは、現在のCriterion、Observed Access Trajectory、Context、Evidence、Historyから生成されるが、Guardを経て、Criterion Update Responseとして`ACCEPT`、`DEFER`、`FREEZE`、`REVIEW`、`ROLLBACK`のいずれかが選択された後にのみ有効化される。本稿では、Subject EvaluationとCriterion Integrity Evaluationを分離し、有限なCriterion Update State Machineを定義し、Candidateの直接採用モデルとGuard付き採用モデルを比較する決定論的PoCを実装した。正当な新規端末シナリオでは、Guard付きモデルはChallenge確認まで更新を保留し、その後、限定的な更新を採用した。段階的な許容領域拡張Poisoningでは、直接更新モデルが攻撃参照値を許容するまで拡張した一方、Guard付きモデルは許容前に更新を凍結した。単一Evidence source侵害では、自動採用を阻止した。これらの結果はSyntheticな仮定下で提案構造が実行可能であることを示すが、本番環境の安全性、普遍的な攻撃検知、False Accept率やFalse Reject率を保証するものではない。

**キーワード:** 適応型認証、継続認証、Criterion poisoning、Guard付き適応、Criterion Integrity、Trajectory、GyroAuth

---

## 1. はじめに

認証は、端末、ネットワーク、場所、行動、運用Contextが時間とともに変化する環境で実行される。Digital authentication guidanceはAuthenticatorやAssuranceの要件を定めるが、時間を通じて取得される観測を将来の認証判断へどのように反映するかは、Application layerで別途設計しなければならない[1], [2]。固定されたCriterionは正当な変化を拒否し得る一方、無制約な適応は攻撃者による挙動の正常化を許し得る。

本研究の中心命題は次である。

```text
dynamic criterion
!=
unconstrained self-update
```

したがって、問題は二重である。GyroAuthは、現在のAccess SubjectがExpected Identityとの関係で許容可能かを評価すると同時に、その判断に用いるAuthentication Criterion自体が引き続き許容可能かを、別の判断として評価しなければならない。

```text
Subject Evaluation
!=
Criterion Integrity Evaluation
```

判断空間も分離する。

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

この分離により、次の組合せを実行可能にする。

```text
AUTH_STABLE + FREEZE
```

現在のAuthentication Relationは一時的に継続可能である一方、将来のCriterion適応は停止できる。

本稿の貢献は次の通りである。

1. Subject EvaluationとCriterion Integrity Evaluationを分離する二重評価モデル。
2. Criterion変化を追跡可能にするCriterion Trajectory表現。
3. `ACCEPT`、`DEFER`、`FREEZE`、`REVIEW`、`ROLLBACK`からなるGuard付きCriterion Update。
4. 有限なCriterion Update State Machine。
5. Candidate直接採用とGuard付き採用を比較する決定論的PoC。
6. Security assumption、支持される主張、限界、非保証の明示。

---

## 2. 背景とRelated Work

### 2.1 GyroAuthの基礎

GyroAuthは認証を次のように定義する。

```text
Authentication
=
Stability-based Selection over State Convergence
```

レイヤー関係は次の通りである。

```text
Gyro Logic   = Theory
GyroOS       = Execution System
GyroAuth     = Authentication Application
```

本研究は、Gyro Logic Coreである`Structure → Slice → Stability`やGyroOS runtime contractを再定義しない。拡張対象はGyroAuth application layerの評価範囲である。

基礎GyroAuth論文は認証モデルそのものを定義する[14], [15]。Trajectory-Based Vulnerability Response論文は、ログイン後の操作とSecurity responseへTrajectory評価を適用する[16], [17]。本稿は、Authentication Criterionおよびその更新過程のIntegrityを対象とする。

### 2.2 Digital authenticationとZero Trust

NIST SP 800-63-4およびSP 800-63B-4は、Digital identityとAuthenticator managementの要件を定める[1], [2]。本モデルは、Password、Passkey、MFA、Authenticator、Assurance levelを置き換えない。Authenticator結果やChallenge結果はEvidenceとして利用できる。

NIST Zero Trust Architectureは、Network locationに基づく暗黙の信頼を排し、Policyに基づく継続的な評価を重視する[3], [4]。GyroAuthはこのArchitectureと両立するが、本稿が扱うのは、適応型認証Componentが将来の判断Criterionを変更してよいかという、より限定された問題である。

### 2.3 Continuous authenticationとBehavioral biometrics

Continuous authentication研究は、Behavior、Biometric、Sensor、Contextual signalを用いてSession中の利用者を継続的に評価する[5], [6]。GyroAuthも認証を一回のLogin eventへ還元しない。

ただし、本稿は次を分離する。

```text
continuous subject evaluation
!=
permission to update the future criterion
```

Behavioral biometricsはEvidenceとなり得るが、Behavioral featureはIdentityそのものではなく、Observed profile changeは自動的に受理されたCriterion updateではない。

### 2.4 Concept driftとPoisoning

Concept drift研究は、時間とともに変化するData distributionへの適応を扱う[8]。これらの手法はCriterion Update Candidateの生成に利用できるが、Security-sensitiveな用途では、観測されたDriftをすべて正当な変化と仮定できない。

Poisoning研究は、攻撃者がTraining dataやAdaptation dataを操作し、将来のModel behaviorを変更できることを示している[10], [13]。本稿では、この問題をAuthentication固有の状態遷移問題として扱い、Current subject decision、Future criterion adoption、Criterion state、Update response、Rollback linkageを分離する。

したがって、新規性主張は次の範囲に限定する。

> 本研究は、Adaptive authenticationやContinuous authenticationそのものの新規性を主張しない。提案の貢献は、Authentication Criterionの変更候補をGuard付きで追跡可能なTrajectoryとして表し、現在の認証判断とは独立して将来のCriterion変更を許可するCriterion Integrity modelにある。

---

## 3. 用語と適用範囲

### 3.1 Access Subject

**Access Subject**は、現在評価されているアクセスおよび操作の発生源である。正当な利用者、Credential thief、Session hijacker、Relay-mediated operator、Bot、Remote controller、または混在した発生源であり得る。

```text
Access Subject
!=
Verified Identity
```

### 3.2 Expected Identity

**Expected Identity**は、変化するSessionやContextをまたいで、Access Subjectを同一の認証Identityとして評価する際の持続的な参照関係である。Credential、端末、場所、行動はEvidenceとなり得るが、Identityそのものではない。

### 3.3 Observed Access Trajectory

**Observed Access Trajectory**は、現在のOrientation、Context、SliceのもとでLocal Authentication Realization間の許容可能な関係を辿ることで得られる、可読な関係的構成である。

```text
History
!=
Trajectory
```

### 3.4 Authentication Criterion

**Authentication Criterion**は、Evidence、Deviation、Stability、Trajectory、History、およびResponse条件を解釈するために用いるContext-relativeな評価基準である。

```text
Authentication Criterion
!=
Fixed Identity Profile
```

### 3.5 Criterion TrajectoryとCriterion Integrity

**Criterion Trajectory**は、Criterion変化を追跡する関係的構成であり、更新理由、Evidence provenance、変化量、方向、速度、識別能力への影響、Response、Rollback linkageを含む。

**Criterion Integrity**は、Authentication Criterionとその更新過程が、Authentication Relationを評価する基準として、許容可能かつ追跡可能な状態を維持していることである。これは自己証明を意味せず、Protected Anchor、独立したEvidence、保持されたHistory、Verified rollback pointに依存する。

---

## 4. Threat Model

本モデルの保護対象は次である。

```text
Authentication Relation
Authentication Criterion
Criterion Update Process
Criterion Trajectory
Trusted History
Rollback Points
Decision separation
```

Threat classには、Credential theft、Session hijacking、Relay attack、Gradual behavioral mimicry、Criterion poisoning、Evidence-source compromise、Coordinated multi-source compromiseを含む。

**Criterion poisoning**とは、攻撃者がEvidenceまたはObserved Access Trajectoryへ影響し、不正な状態や操作を段階的にEffective Authentication Criterionへ取り込ませる攻撃である。

実行検証の中心はGradual region-expansion poisoningである。その他、Criterion translation、Evidence-priority poisoning、Challenge weakening、Context-rule poisoning、History-window poisoning、Rollback-link poisoning、Slow contraction、Response-policy poisoningをThreat Modelへ含める。

最小のTrust assumptionは、少なくとも一つのIndependent Evidence source、Protected policy anchor、Intact audit linkage、Verified rollback pointが攻撃者の同時支配外に残ることである。すべてのEvidence、Anchor、History、Rollback pointが侵害された状況での識別や回復は保証しない。

---

## 5. Formal Security Model

評価は有限なStageで進む。

```text
t = 0, 1, 2, ...
```

時点`t`のEffective Criterionを`A_t`とする。Candidateは次で生成される。

```text
A*_(t+1)
=
U(A_t, T_t^obs, C_(t+1), E_t, H_t)
```

Candidate generationはAdoptionではない。

```text
A*_(t+1)
!=
A_(t+1)
```

Candidateは次のGuardで評価される。

```text
G_t
=
Guard(A_t, A*_(t+1), T_t^obs, C_(t+1), E_t, H_t, P_t)
```

最小Guard vectorは次を評価する。

```text
provenance
cross-evidence consistency
challenge confirmation
update magnitude
update rate
update direction
discrimination preservation
rollback linkage
Evidence-source integrity
```

Critical failureは平均値で相殺しない。

```text
CriticalGuardFail
→
Criterion Update Response != ACCEPT
```

Responseは次で選択する。

```text
D_crit_t = Pi_crit(G_t, Q_t, H_t)
```

Effective Criterionの遷移は次である。

```text
A_(t+1) = A*_(t+1)   when ACCEPT
A_(t+1) = A_t        when DEFER / FREEZE / REVIEW
A_(t+1) = A_tau      when ROLLBACK, tau < t
```

Subject Evaluationは独立して次を選択する。

```text
AUTH_STABLE
RECONVERGING
REAUTH_REQUIRED
AUTH_FAIL
```

Criterion Update Responseは次を選択する。

```text
ACCEPT
DEFER
FREEZE
REVIEW
ROLLBACK
```

---

## 6. Criterion Update State Machine

Criterion Stateは次である。

```text
STABLE
ADAPTING
UNCERTAIN
FROZEN
UNDER_REVIEW
COMPROMISED
ROLLED_BACK
```

Response semanticsは次の通りである。

- `ACCEPT`: Candidateを次のEffective Criterionとして採用する。
- `DEFER`: 追加EvidenceやChallenge結果を待ち、現在のCriterionを維持する。
- `FREEZE`: Update path自体が危険であるためAdaptive adoptionを停止する。Subject Evaluationは独立して継続できる。
- `REVIEW`: 判断をExternal policy、Administrator、Stronger verification path、Independent validatorへ移す。
- `ROLLBACK`: Audit trailを削除せず、Verified prior criterionへ戻す。

```text
DEFER != FREEZE
REVIEW != DEFER
```

図のSourceは`figures/guarded_criterion_trajectories_mermaid.md`に格納する。

---

## 7. PoC設計

PoCは同一のCandidate generatorを用いる二つのModelを比較する。

### 7.1 Model U: Direct adoption

```text
Observation
→ Candidate
→ Direct Adoption
```

### 7.2 Model G: Guarded adoption

```text
Observation
→ Candidate
→ Guard
→ Criterion Update Response
→ Effective Criterion Transition
```

最小Criterion表現は次である。

```text
A_t = (
  mu_t,
  width_t,
  provenance_requirement_t,
  challenge_requirement_t,
  rollback_integrity_t
)
```

実装はPython standard libraryのみを使用し、SyntheticかつDeterministicなInputを用いる。

```text
scripts/simulate_guarded_criterion_update.py
examples/criterion_update/scenarios.json
results/criterion_update_summary.json
```

Scenarioは次である。

```text
N1: Legitimate New Device Transition
P1: Gradual Region Expansion Poisoning
C1: Single Evidence Source Compromise
```

---

## 8. 結果

### 8.1 N1: 正当な新規端末移行

Guarded modelは次を出力した。

```text
Auth Decision:
REAUTH_REQUIRED
→ AUTH_STABLE
→ AUTH_STABLE

Criterion Update Response:
DEFER
→ ACCEPT
→ ACCEPT
```

最終値は次である。

```text
mu    = 0.234
width = 0.120
```

Challenge confirmation前のCandidateは保留され、Re-authentication成功とCross-evidence supportの後に、Admissible regionを拡張しない限定的な更新が採用された。

### 8.2 P1: 段階的な許容領域拡張Poisoning

Direct-update baselineの最終値は次である。

```text
final mu    = 0.3969728
final width = 0.277212
attack reference admissible = true
```

Guarded modelの最終値は次である。

```text
final mu    = 0.200
final width = 0.120
freeze stage = 2
attack reference admissible = false
```

Response pathは次である。

```text
DEFER
→ FREEZE
→ FREEZE
→ FREEZE
→ FREEZE
```

Stage 2で次を出力した。

```text
AUTH_STABLE + FREEZE
```

これは、Current subject acceptanceとPermission to redefine future acceptanceを独立して表現できることを示す。

### 8.3 C1: 単一Evidence source侵害

Guarded modelは次を出力した。

```text
FREEZE
→ FREEZE
```

最終値は次を維持した。

```text
mu    = 0.200
width = 0.120
```

Source integrityとCross-evidence consistencyが低いため、見かけ上強いEvidenceが存在してもCandidateは採用されなかった。

実装した7件のAssertionはすべて成功した。

---

## 9. 考察

中心的な結果は、Current Authentication Relationを継続する判断と、将来のAuthentication Criterionを変更する判断を、実行可能な別判断として表現できることである。`AUTH_STABLE + FREEZE`がその最小例である。

本モデルは非適応ではない。N1は、Challenge confirmation、Provenance check、Cross-evidence consistencyを満たした正当なContext変化を採用できることを示した。一方、観測の反復だけでは正当性を意味しない。

```text
repeated observation
!=
new normal automatically
```

Criterion Integrityは自己証明ではない。ExternalまたはProtected referenceに依存する。また、Guardは単純なWeighted scoreではなく、Critical failureを平均値で相殺しない。

---

## 10. Security Claimsと限界

実装したDeterministic assumptionの範囲では、次を構造的に示した。

1. Candidate generationとAdoptionを分離できる。
2. Auth DecisionとCriterion Update Responseを分離できる。
3. SupportされたBounded adaptationを採用できる。
4. Direct adoptionはCumulative criterion expansionを生み得る。
5. Guarded adoptionは実装したP1でAttack-reference admission前にFreezeできる。
6. C1でSource-integrity failureがAdoptionを阻止できる。
7. `AUTH_STABLE + FREEZE`を実行できる。

本研究は、Criterion poisoningの完全防止、Credential theftやRelay attackの普遍的検知、False Acceptゼロ、False Rejectゼロ、完全なIdentity proof、Total compromise下のSecurity、Production performance、Privacy guarantee、Formal correctness、Statistical generalizationを示していない。

PoCはSyntheticかつDeterministicであり、一次元Criterion、縮約Trajectory proxy、手動設定Thresholdを用いる。Real-world error rateやOperational costは未測定である。

---

## 11. 再現性と公開物

実行例は次である。

```bash
python scripts/simulate_guarded_criterion_update.py \
  --scenarios examples/criterion_update/scenarios.json \
  --output results/criterion_update_results.json
```

Repositoryには、Simulation source、Scenario input、Summary result、Formalization document、Figure sourceを含む。

---

## 12. 結論

適応型認証は正当な変化に対応できるCriterionを必要とするが、ObservationからCriterionへの直接取り込みはPoisoning surfaceを生む。本稿は、Criterion changeをGuard付きTrajectoryとして扱うGyroAuth拡張を提案した。Current Auth DecisionとFuture Criterion Update Responseを独立して選択し、Deterministic PoCにより、Bounded adaptation、実装したP1条件下でのPoisoning containment、Compromised-source updateの阻止を示した。

中心命題は次である。

```text
dynamic criterion
!=
unconstrained self-update
```

---

## 参考文献

[1] D. Temoshok et al., *Digital Identity Guidelines: Authentication and Authenticator Management*, NIST SP 800-63B-4, 2025. DOI: 10.6028/NIST.SP.800-63b-4.

[2] D. Temoshok et al., *Digital Identity Guidelines*, NIST SP 800-63-4, 2025. DOI: 10.6028/NIST.SP.800-63-4.

[3] S. Rose, O. Borchert, S. Mitchell, and S. Connelly, *Zero Trust Architecture*, NIST SP 800-207, 2020. DOI: 10.6028/NIST.SP.800-207.

[4] R. Chandramouli and Z. Butcher, *A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Cloud Environments*, NIST SP 800-207A, 2023. DOI: 10.6028/NIST.SP.800-207A.

[5] M. Abuhamad, A. Abusnaina, D. Nyang, and D. Mohaisen, “Sensor-Based Continuous Authentication of Smartphones’ Users Using Behavioral Biometrics: A Contemporary Survey,” *IEEE Internet of Things Journal*, vol. 8, no. 1, pp. 65–84, 2021. DOI: 10.1109/JIOT.2020.3020076.

[6] A. Al Abdulwahid, N. Clarke, I. Stengel, S. Furnell, and C. Reich, “Security, Privacy, and Usability in Continuous Authentication: A Survey,” *Sensors*, vol. 21, no. 17, 5967, 2021. DOI: 10.3390/s21175967.

[8] J. Gama, I. Žliobaitė, A. Bifet, M. Pechenizkiy, and A. Bouchachia, “A Survey on Concept Drift Adaptation,” *ACM Computing Surveys*, vol. 46, no. 4, Article 44, 2014. DOI: 10.1145/2523813.

[10] B. Biggio, B. Nelson, and P. Laskov, “Poisoning Attacks against Support Vector Machines,” in *Proceedings of the 29th International Conference on Machine Learning*, 2012, pp. 1467–1474.

[13] A. Vassilev, A. Oprea, A. Fordyce, H. Anderson, X. Davies, and M. Hamin, *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations*, NIST AI 100-2e2025, 2025. DOI: 10.6028/NIST.AI.100-2e2025.

[14] S. Kawakami, “GyroAuth: Authentication as Stability-Based Selection over State Convergence,” Jxiv, DOI: 10.51094/jxiv.4600.

[15] S. Kawakami, “GyroAuth：状態収束に対する安定性に基づく認証,” Jxiv, DOI: 10.51094/jxiv.5341.

[16] S. Kawakami, “Trajectory-Based Vulnerability Response,” Jxiv, DOI: 10.51094/jxiv.5416.

[17] S. Kawakami, “Trajectoryに基づく脆弱性対応,” Jxiv, DOI: 10.51094/jxiv.5440.

---

## AI支援ツールの使用

本稿の構成整理、草稿作成補助、表現調整、整合性確認にAI支援ツールを使用した。著者は本文、主張、参考文献、最終原稿を確認・編集し、その内容に全責任を負う。
