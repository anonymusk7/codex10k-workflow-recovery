# Bluestork / BygAI Phase 0 Brief

Use this for the next Bluestork reply or meeting. The buyer corrected the scope: BygAI.dk already has a semi-automatic product, and the valuable question is whether computer vision can automate more of the current floor-plan measurement workflow.

## Current Signals

- Public site positioning: BygAI.dk offers AI-driven measurement for the building trades, moving from floor plan to painter quote quickly.
- Buyer says the live system is semi-automatic.
- Buyer says a DTU master's student worked on the computer-vision problem for months without a consistently generalizable solution.
- Buyer is open to a video meeting if we can approach further automation realistically.

## Meeting Goals

- Identify the single manual step with the best automation ROI.
- Separate "fully general algorithm" risk from a narrower automation-lift target.
- Get one easy and one failing anonymized example.
- Turn the call into a paid Phase 0, not unpaid R&D.

## Questions

1. What does BygAI.dk currently automate from upload to quote output?
2. Where does the operator spend the most time today: scale confirmation, room detection, wall grouping, ceiling/wall area, manual correction, quote formatting, or customer communication?
3. Which plan formats are common: vector PDFs, raster scans, photos, hand sketches, architectural drawings, or mixed?
4. What did the DTU approach try: classical CV, segmentation, OCR/vision-language models, scale detection, graph extraction, or hybrid human-in-loop?
5. What failure mode matters commercially: inaccurate measurements, missing rooms, wrong wall grouping, slow review, bad quote output, or inability to know when the result is unsafe?
6. What output is enough for the first automation lift: confidence triage, pre-filled review UI, room/surface checklist, wall/ceiling estimates, or quote-ready packet?

## Proposed Phase 0

Price: USD 1,200 fixed, credited toward a later implementation milestone.

Inputs:

- 2-5 anonymized plans: one easy, one current-system success, one current-system failure, and optional edge cases.
- Screenshot or screen share of the current BygAI operator workflow.
- Desired output schema and current manual correction notes.

Deliverables:

- Current workflow map from upload to painter quote.
- Failure taxonomy for plan types and automation boundaries.
- Computer-vision approach recommendation: classical CV, vision-language extraction, OCR, segmentation, graph heuristics, or hybrid review.
- Confidence-gate design for when automation should stop and ask for human review.
- One proof path against a narrow output slice using anonymized examples.
- Implementation recommendation with acceptance checks and a fixed-price milestone range.

Success Criteria:

- A repeatable subset is identified where automation can reduce manual work.
- The system can detect when it is uncertain instead of silently producing bad measurements.
- The buyer can decide whether a USD 4,500-7,500 implementation milestone is commercially rational.

## Boundaries

- Do not claim a fully general floor-plan measurement algorithm.
- Do not request production customer data by email.
- Do not guarantee measurement accuracy before seeing examples and current workflow.
- Treat this as an automation-lift and review-speed project, not pure research.
