const currency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

const form = document.querySelector("#lead-form");
const steps = document.querySelector("#workflow-steps");
const status = document.querySelector("#queue-status");
const summary = document.querySelector("#crm-summary");

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

function runWorkflow(event) {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form).entries());
  const items = workflowSteps(data)
    .map((item) => `<li>${item}</li>`)
    .join("");

  steps.innerHTML = items;
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

calculateRoi();

