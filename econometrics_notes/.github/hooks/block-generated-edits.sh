#!/usr/bin/env bash
set -euo pipefail

payload_file="$(mktemp)"
trap 'rm -f "$payload_file"' EXIT
cat > "$payload_file"

python3 - "$payload_file" <<'PY'
import json
import re
import sys
from pathlib import Path


def allow():
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                }
            }
        )
    )


def deny(path):
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "Generated artifact protection: edit the source .qmd file instead.",
                },
                "systemMessage": f"Blocked edit targeting generated artifact path: {path}",
            }
        )
    )


def is_generated_artifact_path(path_value):
    p = path_value.strip().strip('"').strip("'").replace("\\", "/")
    lower = p.lower()

    forbidden_exts = (".pdf", ".html", ".docx", ".tex", ".aux", ".log", ".loe")
    if any(lower.endswith(ext) for ext in forbidden_exts):
        return True

    segments = [segment for segment in lower.split("/") if segment]
    if any(segment.endswith("_cache") or segment.endswith("_files") for segment in segments):
        return True

    return False


raw = Path(sys.argv[1]).read_text(encoding="utf-8")
if not raw.strip():
    allow()
    raise SystemExit(0)

all_text = raw.lower()
edit_tool_markers = ("apply_patch", "create_file", "edit_notebook_file")
if not any(marker in all_text for marker in edit_tool_markers):
    allow()
    raise SystemExit(0)

target_paths = []

# Paths from apply_patch payload text (escaped-newline JSON representation).
target_paths.extend(
    re.findall(r"\*\*\*\s+(?:Add|Update|Delete)\s+File:\s*([^\\\"\n\r]+)", raw)
)

# Direct path-bearing keys used by file-editing tools.
target_paths.extend(
    re.findall(
        r'"(?:filePath|filepath|path|file_path|old_path|new_path|dirPath|dirpath)"\s*:\s*"([^"]+)"',
        raw,
        flags=re.IGNORECASE,
    )
)

for candidate in target_paths:
    if is_generated_artifact_path(candidate):
        deny(candidate)
        raise SystemExit(0)

allow()
PY
