/*
 * Generated demo data derived from the public deterministic PoC artifacts:
 * - examples/criterion_update/scenarios.json
 * - results/criterion_update_summary.json
 * - scripts/simulate_guarded_criterion_update.py
 *
 * The data below is static and contains no credentials, personal telemetry,
 * secrets, or external API dependencies.
 */
window.GYROAUTH_DEMO_DATA = {
  version: 1,
  source: {
    scenarioFile: "examples/criterion_update/scenarios.json",
    summaryFile: "results/criterion_update_summary.json",
    simulationFile: "scripts/simulate_guarded_criterion_update.py",
    deterministic: true,
    attackReference: 0.62
  },
  scenarios: [
    {
      id: "N1",
      shortName: "Normal Transition",
      name: "Legitimate New Device Transition",
      description: "A legitimate new device is deferred until challenge confirmation, then accepted through a bounded update.",
      stages: [
        {
          stage: 1,
          label: "New device first seen",
          authDecision: "REAUTH_REQUIRED",
          criterionResponse: "DEFER",
          criterionState: "UNCERTAIN",
          criterionCenter: 0.2,
          criterionWidth: 0.12,
          attackReferenceAdmissible: false,
          note: "Challenge confirmation is still pending."
        },
        {
          stage: 2,
          label: "Successful re-authentication",
          authDecision: "AUTH_STABLE",
          criterionResponse: "ACCEPT",
          criterionState: "ADAPTING",
          criterionCenter: 0.22,
          criterionWidth: 0.12,
          attackReferenceAdmissible: false,
          note: "Independent challenge and cross-evidence support the bounded update."
        },
        {
          stage: 3,
          label: "Trusted post-challenge behavior",
          authDecision: "AUTH_STABLE",
          criterionResponse: "ACCEPT",
          criterionState: "STABLE",
          criterionCenter: 0.234,
          criterionWidth: 0.12,
          attackReferenceAdmissible: false,
          note: "The supported transition completes without widening the criterion."
        }
      ],
      comparison: {
        direct: {
          finalCenter: 0.24808,
          finalWidth: 0.12,
          attackReferenceAdmissible: false
        },
        guarded: {
          finalCenter: 0.234,
          finalWidth: 0.12,
          attackReferenceAdmissible: false
        }
      }
    },
    {
      id: "P1",
      shortName: "Gradual Poisoning",
      name: "Gradual Region Expansion Poisoning",
      description: "Repeated suspicious observations expand an unconstrained criterion, while the guarded path freezes adaptation at stage 2.",
      stages: [
        {
          stage: 1,
          label: "Small transfer expansion 1",
          authDecision: "RECONVERGING",
          criterionResponse: "DEFER",
          criterionState: "UNCERTAIN",
          criterionCenter: 0.2,
          criterionWidth: 0.12,
          attackReferenceAdmissible: false,
          note: "The observation is suspicious, but the first guarded response remains DEFER."
        },
        {
          stage: 2,
          label: "Small transfer expansion 2",
          authDecision: "AUTH_STABLE",
          criterionResponse: "FREEZE",
          criterionState: "FROZEN",
          criterionCenter: 0.2,
          criterionWidth: 0.12,
          attackReferenceAdmissible: false,
          note: "AUTH_STABLE + FREEZE: current access may continue, while future criterion adaptation is blocked."
        },
        {
          stage: 3,
          label: "Small transfer expansion 3",
          authDecision: "AUTH_FAIL",
          criterionResponse: "FREEZE",
          criterionState: "FROZEN",
          criterionCenter: 0.2,
          criterionWidth: 0.12,
          attackReferenceAdmissible: false,
          note: "The current relation fails, and the frozen criterion remains unchanged."
        },
        {
          stage: 4,
          label: "Attack reference approach",
          authDecision: "AUTH_FAIL",
          criterionResponse: "FREEZE",
          criterionState: "FROZEN",
          criterionCenter: 0.2,
          criterionWidth: 0.12,
          attackReferenceAdmissible: false,
          note: "The attack reference remains outside the guarded criterion."
        },
        {
          stage: 5,
          label: "Attack reference sustained",
          authDecision: "AUTH_FAIL",
          criterionResponse: "FREEZE",
          criterionState: "FROZEN",
          criterionCenter: 0.2,
          criterionWidth: 0.12,
          attackReferenceAdmissible: false,
          note: "Continued malicious behavior does not redefine the frozen criterion."
        }
      ],
      comparison: {
        direct: {
          finalCenter: 0.3969728,
          finalWidth: 0.277212,
          attackReferenceAdmissible: true
        },
        guarded: {
          finalCenter: 0.2,
          finalWidth: 0.12,
          attackReferenceAdmissible: false
        }
      }
    },
    {
      id: "C1",
      shortName: "Compromised Evidence",
      name: "Single Evidence Source Compromise",
      description: "Apparently strong evidence is not adopted when source integrity and cross-evidence consistency are insufficient.",
      stages: [
        {
          stage: 1,
          label: "Apparently valid location from compromised source",
          authDecision: "REAUTH_REQUIRED",
          criterionResponse: "FREEZE",
          criterionState: "FROZEN",
          criterionCenter: 0.2,
          criterionWidth: 0.12,
          attackReferenceAdmissible: false,
          note: "Low source integrity is non-compensable and blocks automatic adoption."
        },
        {
          stage: 2,
          label: "Continued cross-evidence inconsistency",
          authDecision: "REAUTH_REQUIRED",
          criterionResponse: "FREEZE",
          criterionState: "FROZEN",
          criterionCenter: 0.2,
          criterionWidth: 0.12,
          attackReferenceAdmissible: false,
          note: "Repeated apparently strong evidence does not override the compromised source."
        }
      ],
      comparison: {
        direct: {
          finalCenter: 0.2328,
          finalWidth: 0.12,
          attackReferenceAdmissible: false
        },
        guarded: {
          finalCenter: 0.2,
          finalWidth: 0.12,
          attackReferenceAdmissible: false
        }
      }
    }
  ]
};
