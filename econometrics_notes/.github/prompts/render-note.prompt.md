---
description: "Render a single Quarto note and report diagnostics. Use when: render note, rerender note, stale cache, validate Quarto output."
name: "Render Quarto Note"
argument-hint: "Target .qmd path (optional) and output format: pdf/html/docx"
agent: "agent"
---

Render one Quarto note in this workspace.

## Workflow

1. Resolve the target file:
- If the user provides a `.qmd` path, use it.
- Otherwise use the active `.qmd` file.
- If no target is available, ask for a specific `.qmd` file.

2. Resolve format:
- Default to `pdf`.
- If the user requests `html` or `docx`, use that format.

3. Run render:
- `quarto render <file>.qmd --to <format>`
- If output looks stale after computational changes, or if the user requests a fresh run, clear only that note's cache and render again:
  - `rm -rf <file_stem>_cache/`

4. Return concise diagnostics:
- Command(s) run
- Render status (success/failure)
- Key error lines when failed
- Output artifact path
