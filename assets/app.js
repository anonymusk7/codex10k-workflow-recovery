const currency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

const form = document.querySelector("#lead-form");
const steps = document.querySelector("#workflow-steps");
const status = document.querySelector("#queue-status");
const summary = document.querySelector("#crm-summary");
const floorplanForm = document.querySelector("#floorplan-form");
const planStatus = document.querySelector("#plan-status");
const planSteps = document.querySelector("#plan-steps");
const planSchema = document.querySelector("#plan-schema");

function workflowSteps(data) {
  const owner = data.urgency === "Same day" ? "priority owner" : "sales owner";
  return [
    `Captured ${data.name}'s ${data.segment.toLowerCase()} request and assigned it to the ${owner}.`,
    `Extracted requirements: ${data.request}`,
    `Generated a customer-safe acknowledgement asking for any missing quantity, delivery, budget, or timing details.`,
    `Created a CRM task with urgency marked as ${data.urgency.toLowerCase()} and a follow-up deadline.`,
    "Added the request to the team queue with source, status, next action, and audit notes.",
  ];
}

function renderList(list, items) {
  list.replaceChildren();
  items.forEach((item) => {
    const element = document.createElement("li");
    element.textContent = item;
    list.append(element);
  });
}

function runWorkflow(event) {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form).entries());

  renderList(steps, workflowSteps(data));
  status.textContent = data.urgency === "Same day" ? "Escalated" : "Queued";
  summary.textContent = `${data.name} | ${data.segment} | ${data.urgency} urgency | Next action: confirm exact requirements and send quote path.`;
}

function calculateRoi() {
  const leads = Number(document.querySelector("#leads").value) || 0;
  const deal = Number(document.querySelector("#deal").value) || 0;
  const close = Number(document.querySelector("#close").value) || 0;
  const hours = Number(document.querySelector("#hours").value) || 0;
  const recoveredRevenue = leads * 4.33 * deal * (close / 100);
  const savedTime = hours * 4.33 * 50;
  document.querySelector("#roi").textContent = currency.format(recoveredRevenue + savedTime);
}

form.addEventListener("submit", runWorkflow);
document.querySelectorAll("#leads, #deal, #close, #hours").forEach((input) => {
  input.addEventListener("input", calculateRoi);
});

function floorplanAssessment(data) {
  const complexity = Number(data.complexity) || 1;
  const scaleRisk = data.scale === "No scale visible" ? 2 : data.scale === "Known room dimension only" ? 1 : 0;
  const outputRisk = data.output === "Measurement estimate packet" ? 1 : data.output === "Quote-ready scope summary" ? 2 : 0;
  const riskScore = complexity + scaleRisk + outputRisk;
  const statusLabel = riskScore >= 7 ? "Human review first" : riskScore >= 5 ? "Feasible with guardrails" : "Feasible";

  return {
    statusLabel,
    steps: [
      `Classify plan as ${data.planType.toLowerCase()} with complexity ${complexity}/5.`,
      data.scale === "Explicit scale on plan"
        ? "Use visible scale as the first measurement assumption."
        : `Request reviewer confirmation because scale source is: ${data.scale.toLowerCase()}.`,
      "Segment rooms and surfaces into a checklist before attempting any quote logic.",
      statusLabel === "Human review first"
        ? "Route to human review before measurement or quote output."
        : "Generate contractor draft with confidence flags and missing-information notes.",
      "Store original file, output schema, risk score, reviewer status, and next action.",
    ],
    schema: {
      plan_type: data.planType,
      output_target: data.output,
      risk_score: riskScore,
      confidence_gate: statusLabel,
      required_review: riskScore >= 5,
      fields: ["room_name", "surface_type", "quantity_or_area", "confidence", "review_note"],
    },
  };
}

function runFloorplanAssessment(event) {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(floorplanForm).entries());
  const assessment = floorplanAssessment(data);

  planStatus.textContent = assessment.statusLabel;
  renderList(planSteps, assessment.steps);
  planSchema.textContent = JSON.stringify(assessment.schema, null, 2);
}

floorplanForm.addEventListener("submit", runFloorplanAssessment);
calculateRoi();
