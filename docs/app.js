(() => {
  "use strict";

  const data = window.GYROAUTH_DEMO_DATA;
  if (!data || !Array.isArray(data.scenarios) || data.scenarios.length === 0) {
    document.body.innerHTML = "<p>Demo data could not be loaded.</p>";
    return;
  }

  const state = {
    scenarioIndex: 0,
    stageIndex: 0
  };

  const elements = {
    buttons: document.getElementById("scenario-buttons"),
    stageTitle: document.getElementById("stage-title"),
    stageCount: document.getElementById("stage-count"),
    authDecision: document.getElementById("auth-decision"),
    criterionResponse: document.getElementById("criterion-response"),
    criterionCenter: document.getElementById("criterion-center"),
    criterionWidth: document.getElementById("criterion-width"),
    attackAdmissible: document.getElementById("attack-admissible"),
    criterionState: document.getElementById("criterion-state"),
    previous: document.getElementById("previous-stage"),
    next: document.getElementById("next-stage"),
    combinationPanel: document.getElementById("combination-panel"),
    combinationTitle: document.getElementById("combination-title"),
    combinationCopy: document.getElementById("combination-copy"),
    guardExplanation: document.getElementById("guard-explanation"),
    timeline: document.getElementById("timeline"),
    directCenter: document.getElementById("direct-center"),
    directWidth: document.getElementById("direct-width"),
    directAttack: document.getElementById("direct-attack"),
    guardedCenter: document.getElementById("guarded-center"),
    guardedWidth: document.getElementById("guarded-width"),
    guardedAttack: document.getElementById("guarded-attack")
  };

  function currentScenario() {
    return data.scenarios[state.scenarioIndex];
  }

  function currentStage() {
    return currentScenario().stages[state.stageIndex];
  }

  function formatNumber(value) {
    return Number(value).toFixed(6).replace(/0+$/, "").replace(/\.$/, "");
  }

  function boolLabel(value) {
    return value ? "true" : "false";
  }

  function decisionClass(value) {
    if (value === "AUTH_STABLE" || value === "ACCEPT") return "value-success";
    if (value === "RECONVERGING" || value === "REAUTH_REQUIRED" || value === "DEFER") return "value-warning";
    if (value === "AUTH_FAIL" || value === "FREEZE" || value === "ROLLBACK") return "value-danger";
    return "";
  }

  function setValue(element, value, className = "") {
    element.textContent = value;
    element.className = className;
  }

  function renderScenarioButtons() {
    elements.buttons.replaceChildren();
    data.scenarios.forEach((scenario, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = scenario.shortName;
      button.setAttribute("aria-pressed", index === state.scenarioIndex ? "true" : "false");
      button.addEventListener("click", () => {
        state.scenarioIndex = index;
        state.stageIndex = 0;
        render();
      });
      elements.buttons.appendChild(button);
    });
  }

  function renderTimeline() {
    const scenario = currentScenario();
    elements.timeline.replaceChildren();

    scenario.stages.forEach((stage, index) => {
      const item = document.createElement("li");
      if (index === state.stageIndex) {
        item.setAttribute("aria-current", "step");
      }

      const button = document.createElement("button");
      button.type = "button";
      button.setAttribute("aria-label", `Go to stage ${stage.stage}: ${stage.label}`);
      button.addEventListener("click", () => {
        state.stageIndex = index;
        render();
      });

      const stageLabel = document.createElement("strong");
      stageLabel.textContent = `Stage ${stage.stage}`;
      const description = document.createElement("span");
      description.textContent = stage.label;
      const response = document.createElement("span");
      response.className = "timeline-response";
      response.textContent = `${stage.authDecision} / ${stage.criterionResponse}`;

      button.append(stageLabel, description, response);
      item.appendChild(button);
      elements.timeline.appendChild(item);
    });
  }

  function renderCombination() {
    const stage = currentStage();
    const combination = `${stage.authDecision} + ${stage.criterionResponse}`;
    elements.combinationTitle.textContent = combination;
    elements.combinationCopy.textContent = stage.note;

    if (stage.authDecision === "AUTH_STABLE" && stage.criterionResponse === "FREEZE") {
      elements.guardExplanation.textContent = "Current Authentication Relation may continue. Future criterion adaptation is blocked.";
      elements.combinationPanel.setAttribute("data-highlight", "auth-stable-freeze");
    } else {
      elements.guardExplanation.textContent = "Auth Decision and Criterion Update Response remain independently selected.";
      elements.combinationPanel.removeAttribute("data-highlight");
    }
  }

  function renderComparison() {
    const comparison = currentScenario().comparison;
    setValue(elements.directCenter, formatNumber(comparison.direct.finalCenter));
    setValue(elements.directWidth, formatNumber(comparison.direct.finalWidth));
    setValue(
      elements.directAttack,
      boolLabel(comparison.direct.attackReferenceAdmissible),
      comparison.direct.attackReferenceAdmissible ? "value-danger" : "value-success"
    );
    setValue(elements.guardedCenter, formatNumber(comparison.guarded.finalCenter));
    setValue(elements.guardedWidth, formatNumber(comparison.guarded.finalWidth));
    setValue(
      elements.guardedAttack,
      boolLabel(comparison.guarded.attackReferenceAdmissible),
      comparison.guarded.attackReferenceAdmissible ? "value-danger" : "value-success"
    );
  }

  function renderStage() {
    const scenario = currentScenario();
    const stage = currentStage();

    elements.stageTitle.textContent = stage.label;
    elements.stageCount.textContent = `${stage.stage} / ${scenario.stages.length}`;
    setValue(elements.authDecision, stage.authDecision, decisionClass(stage.authDecision));
    setValue(elements.criterionResponse, stage.criterionResponse, decisionClass(stage.criterionResponse));
    setValue(elements.criterionCenter, formatNumber(stage.criterionCenter));
    setValue(elements.criterionWidth, formatNumber(stage.criterionWidth));
    setValue(
      elements.attackAdmissible,
      boolLabel(stage.attackReferenceAdmissible),
      stage.attackReferenceAdmissible ? "value-danger" : "value-success"
    );
    setValue(elements.criterionState, stage.criterionState, decisionClass(stage.criterionResponse));

    elements.previous.disabled = state.stageIndex === 0;
    elements.next.disabled = state.stageIndex === scenario.stages.length - 1;
  }

  function render() {
    renderScenarioButtons();
    renderStage();
    renderCombination();
    renderTimeline();
    renderComparison();
  }

  elements.previous.addEventListener("click", () => {
    if (state.stageIndex > 0) {
      state.stageIndex -= 1;
      render();
    }
  });

  elements.next.addEventListener("click", () => {
    if (state.stageIndex < currentScenario().stages.length - 1) {
      state.stageIndex += 1;
      render();
    }
  });

  render();
})();
