---
description: "Use when editing Quarto .qmd lecture notes in this repository. Covers YAML/frontmatter preservation, R chunk options, reproducible simulations, citation paths, and render validation."
name: "Quarto Notes Editing"
applyTo: "**/*.qmd"
---

# Quarto Notes Editing Guidelines

- Preserve each file's existing YAML frontmatter structure, especially `format`, `pdf-engine`, font settings, and `include-in-header` blocks.
- Do not move or rename shared citation assets. Keep `bibliography: references.bib` and `csl: chicago-author-date.csl` paths unchanged unless explicitly requested.
- Keep mathematical macro and theorem definitions consistent with the document you are editing (for example `\symbf`, `\betahat`, `\E`, `\Var`, and custom theorem environments).
- For R chunks, prefer explicit chunk options (`echo`, `warning`, `message`, and `cache`) over implicit defaults.
- Any stochastic simulation or randomized example should include `set.seed(...)` in the relevant chunk.
- Use clear, stable chunk labels in lowercase kebab-case when adding new chunks.
- Validate edits by rendering only the modified document first: `quarto render <file>.qmd --to pdf`.
- If computational output appears stale after logic changes, clear the matching cache directory (for example `rm -rf <file>_cache/`) and render again.
- Treat generated files and folders as artifacts. Do not edit `*.pdf`, `*.html`, `*.docx`, `*.tex`, `*_cache/`, or `*_files/` to make source changes.

## Preferred R Chunk Pattern

````markdown
```{r}
#| label: simulation-example
#| echo: true
#| warning: false
#| message: false
#| cache: true
set.seed(123)
```
````