# Project Guidelines

## Code Style
- This repository is Quarto-first: edit source in `.qmd` files and preserve Markdown + LaTeX structure.
- Keep YAML frontmatter settings local to each document; do not standardize engines or format options across files unless explicitly asked.
- Preserve existing mathematical macro conventions (for example `\symbf`, `\betahat`, `\E`, `\Var`) and theorem environments defined in each file header.
- For stochastic R computations, use an explicit `set.seed(...)` in the relevant chunk.
- Keep chunk options explicit for teaching notes (`echo`, `warning`, `message`, and `cache` where needed).

## Architecture
- Primary sources are root `.qmd` files, especially:
  - `clrm_notes_r_final.qmd`
  - `clrm_notes_r.qmd`
  - `monte_carlo_spherical_errors_advanced.qmd`
  - `clrm.qmd`
  - `test_marking_guide.qmd`
- Citation assets are shared in root:
  - `references.bib`
  - `chicago-author-date.csl`
- Treat generated artifacts as build output, not source:
  - `*.pdf`, `*.html`, `*.docx`, `*.tex`, `*.aux`, `*.log`, `*.loe`
  - `*_cache/`, `*_files/`

## Build and Test
- Render only the file you changed unless asked to batch-render everything.
- Standard render command:
  - `quarto render <file>.qmd --to pdf`
- Examples:
  - `quarto render clrm_notes_r_final.qmd --to pdf`
  - `quarto render monte_carlo_spherical_errors_advanced.qmd --to pdf`
- Optional alternate outputs (on request):
  - `quarto render <file>.qmd --to html`
  - `quarto render <file>.qmd --to docx`
- If results look stale after computational changes, clear the matching cache directory (for example `rm -rf clrm_notes_r_final_cache/`) and re-render.
- There is no dedicated unit-test suite in this repo; validation is successful render of the modified document.

## Conventions
- Respect each document's `pdf-engine` choice (`xelatex` and `lualatex` are both used in this workspace).
- Keep bibliography and CSL paths relative and unchanged unless the user asks for a reorganization.
- Do not edit generated files to make content changes; edit the corresponding `.qmd` source and re-render.
- When multiple variants exist (`*_final`, `*_restored`, `*_word_r`), modify only the file requested by the user.