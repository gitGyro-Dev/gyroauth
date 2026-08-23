# Claude Review — Guarded Criterion Trajectories for Adaptive Authentication

Date: 2026-08-23  
Target: Guarded Criterion Trajectories for Adaptive Authentication  
Jxiv DOI: https://doi.org/10.51094/jxiv.5671  
Reviewer role: Claude (critique only)

## Overall Assessment

The central idea—explicitly separating the current access decision from the authorization to update future authentication criteria—is coherent. The use of `AUTH_STABLE + FREEZE` as the minimum executable example supports the claim that permission for continued adaptation is not identical to acceptance of the current relation. The state-machine and PoC presentation are internally consistent and easy to follow.

The Discussion and Limitations sections are appropriately cautious. The paper clearly states that it does not establish production-grade security and that the PoC is a structural demonstration using synthetic inputs.

## Review Points

### R1. PoC scale is too small relative to the strength of the claims

The PoC uses a one-dimensional criterion (`mu`, `width`) and only three deterministic synthetic scenarios (N1/P1/C1). Under these conditions, a result such as “guarded adoption can contain poisoning” risks becoming close to a tautological demonstration: if a freeze threshold is defined to stop the implemented attack, then the implemented attack is stopped.

The current evaluation does not include an adaptive adversary who knows or estimates the Guard thresholds and attempts to remain below them while gradually shifting the criterion.

The phrase `poisoning containment` may therefore read as stronger than the implemented evidence supports.

### R2. Section 5 is called a “Formal Security Model” but is not formal in the theorem/proof sense

Expressions such as:

```text
A*_(t+1) = U(...)
G_t = Guard(...)
```

primarily define interfaces, state variables, and transition structure. The paper does not provide formal adversary capabilities, security games, reduction arguments, probability bounds, invariants proved under stated assumptions, or theorems with proofs.

As written, Section 5 is closer to a formalized model specification or typed state-transition model than a formal security proof.

A future version should either:

- strengthen the formalization toward theorem/security-property level, or
- weaken/rename the section title to match the current level of rigor.

### R3. Missing reference numbers

References `[7]`, `[9]`, `[11]`, and `[12]` are absent from both the manuscript text and the References list.

This appears to be a numbering artifact from prior editing and should be cleaned up in a revision.

### R4. Dependence on self-citation

References `[14]`–`[17]` are all Jxiv papers by the same author. Several GyroAuth / Gyro Logic foundation concepts are delegated to those papers.

Because of this series structure, a reader evaluating this paper in isolation may have difficulty independently assessing the foundation on which the extension is built.

A future revision could make the paper more self-contained by summarizing the minimum foundation needed for the present claim, while still preserving the layered project architecture.

### O1. Heavy use of `!=` notation

Expressions such as:

```text
dynamic criterion != unconstrained self-update
```

are readable rhetorical devices, but they are not formal logical formulas. Their use near a section titled “Formal Security Model” may blur the distinction between rhetorical separation statements and mathematically formal claims.

Future revisions should consider explicitly distinguishing these two roles.

### O2. Related-work coverage could include model-update governance / MLOps safety

The novelty claim is appropriately limited: the paper does not claim novelty in adaptive or continuous authentication alone.

However, the architecture may also be interpreted through existing practices such as:

- canary release,
- gradual rollout,
- human-in-the-loop review,
- controlled model update governance,
- safe deployment / rollback patterns.

Adding related work from the model-update governance and MLOps safety domain could make the positioning clearer and reduce the risk that the contribution appears to be only a repackaging of known deployment controls.

## Summary

The structural claim is clear and educationally useful:

```text
current authentication decision
!=
permission to change the future criterion
```

The current paper remains a minimum concept demonstration rather than an empirical or formally proved security result.

The strongest next-step candidates are:

1. evaluate adaptive attackers that attempt to evade the Guard;
2. either strengthen Section 5 toward theorem-level formalization or rename it to match its current scope;
3. clean reference numbering;
4. reduce reliance on external self-citations by making the minimum foundation more self-contained;
5. distinguish rhetorical `!=` statements from formal notation;
6. expand related work toward model-update governance / MLOps safety.
