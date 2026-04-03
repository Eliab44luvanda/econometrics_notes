# Agent-Customization Skill: Create Skill Template

## Purpose
Provide a concise, reusable template and step-by-step workflow for creating repository- or user-scoped `SKILL.md` files that define custom agent behaviors, prompts, and usage patterns. This skill helps authors extract workflows from conversations, formalize them, and produce a polished `SKILL.md` ready for review and reuse.

## When to use
- You want to turn an observed multi-step conversation, process, or methodology into a reusable skill.
- You need a consistent template for agent-customization that other contributors can follow.
- You want a short checklist plus iteration steps to move from draft → review → finalized skill.

## Inputs
- Conversation transcript or notes describing the workflow.
- Intended outcome of the skill (what it should produce).
- Scope: workspace-scoped or personal (global) preference.

## Outputs
- A drafted `SKILL.md` file located at a repository-chosen path (e.g., `.agents/skills/<skill-name>/SKILL.md`).
- A short list of clarifying questions for ambiguous parts.
- Example prompts and suggested follow-up customizations.

## Step-by-step workflow (recommended)
1. Read the conversation and supporting files to identify a repeatable workflow.
2. Extract the step sequence: list the main steps in order, including decision points.
3. Capture branching logic: when to choose path A vs. B and what triggers each branch.
4. Define success criteria and quality checks that mark the workflow as "done".
5. Draft the `SKILL.md` using the template below.
6. Save the draft under `.agents/skills/<skill-name>/SKILL.md` in the repo.
7. Identify and list any ambiguous or missing details as clarifying questions.
8. Share the draft with the original author or relevant reviewers.
9. Incorporate feedback and finalize the skill.

## Decision points and branching logic (pattern)
- For each step include a short conditional summary: `If <condition> then <next step>, else <alternative>`.
- Mark any steps that require human judgment vs. those that can be fully automated.

## Quality criteria / Completion checks
- The skill must produce a clear, runnable output (a `SKILL.md` file in repo).
- All major steps in the original workflow are represented and ordered.
- Branching logic is captured and easy to follow.
- At least two example prompts are provided for end-users.
- Ambiguities have been listed as explicit questions.

## Iteration guidance
1. Draft quickly — prefer clarity over perfection.
2. Flag unclear or missing requirements as questions in the draft.
3. Ask the original author to confirm decision points and the definition of "done."
4. Update the skill and re-run a short smoke-test by applying it to a small example conversation.

## Template for `SKILL.md` (copy into new skill file)
---
title: <short skill title>
summary: |
  One-line summary of what this skill does and when to use it.
usage: |
  Short usage guidance: who, when, and expected inputs/outputs.
when-to-use:
  - bullet: reason 1
  - bullet: reason 2
scope: workspace | personal
inputs:
  - conversation: text or link
  - files: optional supporting files
outputs:
  - path: where the generated artefact is saved
workflow:
  - step 1: short description
  - step 2: short description
decision-points:
  - condition: "if X then Y else Z"
quality-criteria:
  - criterion 1
  - criterion 2
examples:
  - "Create a skill from a debugging checklist conversation"
  - "Turn a code-review workflow into a reusable skill"
clarifying-questions:
  - "What is the canonical path to save this skill in the repo?"
  - "Who will review and approve changes?"
notes:
  - "Keep the skill concise and focused on a single workflow."
---

## Example prompts to try after creating this skill
- "Create a `SKILL.md` that converts the conversation in `issue-123` into a step-by-step testing workflow."
- "Draft a skill that formalizes our release checklist and saves it under `.agents/skills/release/SKILL.md`."

## Suggested next customizations
- Add a `checklist.md` renderer that converts `workflow` bullets into a user-facing checklist UI.
- Add automated tests that validate the presence of `decision-points` and `quality-criteria` sections.

## Maintainer notes
- Place the final `SKILL.md` under `.agents/skills/<skill-name>/SKILL.md` so tools can discover it.
- Follow repository conventions for naming and scope (workspace vs personal).

---

If you want, I can (choose one):
- draft a concrete `SKILL.md` from a specific conversation you point to,
- or open a short list of clarifying questions about the intended scope and reviewers.
