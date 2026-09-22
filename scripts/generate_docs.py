#!/usr/bin/env python3
"""Regenerate the reference section of docs/workflows/<name>.md from the workflow files.

Every reusable workflow (one with `on.workflow_call`) gets an auto-generated block with its
inputs, secrets, outputs and the permissions a caller must grant. The block lives between
the BEGIN/END markers below; everything outside the markers is hand-written and preserved.

Usage:
    python scripts/generate_docs.py          # rewrite docs in place
    python scripts/generate_docs.py --check  # exit 1 if any doc is out of date (used in CI)
"""
import argparse
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"
DOCS = ROOT / "docs" / "workflows"
BEGIN = "<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->"
END = "<!-- END GENERATED REFERENCE -->"
PERMISSION_RANK = {"none": 0, "read": 1, "write": 2}


def cell(value) -> str:
    """Render a value for a markdown table cell."""
    if value is None or value == "":
        return ""
    if isinstance(value, bool):
        value = str(value).lower()
    text = str(value).strip()
    if "\n" in text:
        text = "<br>".join(f"`{line}`" for line in text.splitlines())
        return text
    return f"`{text}`".replace("|", "\\|")


def describe(value) -> str:
    return str(value or "").strip().replace("\n", " ").replace("|", "\\|")


def load(path: pathlib.Path):
    # PyYAML (YAML 1.1) parses the bare key `on` as boolean True.
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    on = data.get("on", data.get(True)) or {}
    return data, (on.get("workflow_call") if isinstance(on, dict) else None)


def caller_permissions(data) -> dict:
    """Union of the permissions requested by the workflow's jobs = what the caller must grant."""
    top = data.get("permissions") or {}
    merged: dict = {}
    for job in (data.get("jobs") or {}).values():
        perms = job.get("permissions", top) or {}
        if isinstance(perms, str):  # read-all / write-all
            continue
        for scope, level in perms.items():
            if PERMISSION_RANK.get(level, 0) > PERMISSION_RANK.get(merged.get(scope, "none"), 0):
                merged[scope] = level
    return merged


def render(path: pathlib.Path, data, call) -> str:
    inputs = call.get("inputs") or {}
    secrets = call.get("secrets") or {}
    outputs = call.get("outputs") or {}
    perms = caller_permissions(data)
    out = [BEGIN, "", "## Reference", ""]
    out.append(f"**Workflow file:** [`{path.name}`](../../.github/workflows/{path.name})")
    out.append("")
    out.append("### Permissions the calling job must grant")
    out.append("")
    out.append("```yaml")
    out.append("permissions:")
    for scope, level in sorted(perms.items()):
        out.append(f"  {scope}: {level}")
    out.append("```")
    out.append("")
    if inputs:
        out += ["### Inputs", "", "| Name | Type | Required | Default | Description |", "|---|---|---|---|---|"]
        for name, spec in inputs.items():
            spec = spec or {}
            required = "yes" if spec.get("required") else "no"
            out.append(
                f"| `{name}` | {spec.get('type', 'string')} | {required} | "
                f"{cell(spec.get('default'))} | {describe(spec.get('description'))} |"
            )
        out.append("")
    if secrets:
        out += ["### Secrets", "", "| Name | Required | Description |", "|---|---|---|"]
        for name, spec in secrets.items():
            spec = spec or {}
            required = "yes" if spec.get("required") else "no"
            out.append(f"| `{name}` | {required} | {describe(spec.get('description'))} |")
        out.append("")
    if outputs:
        out += ["### Outputs", "", "| Name | Description |", "|---|---|"]
        for name, spec in outputs.items():
            out.append(f"| `{name}` | {describe((spec or {}).get('description'))} |")
        out.append("")
    out.append(END)
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if docs are out of date")
    args = parser.parse_args()
    DOCS.mkdir(parents=True, exist_ok=True)
    stale = []
    for path in sorted(WORKFLOWS.glob("*.yml")):
        data, call = load(path)
        if call is None:
            continue
        doc = DOCS / f"{path.stem}.md"
        block = render(path, data, call)
        if doc.exists():
            current = doc.read_text(encoding="utf-8")
            if BEGIN in current and END in current:
                head, rest = current.split(BEGIN, 1)
                tail = rest.split(END, 1)[1]
                new = head + block + tail
            else:
                new = current.rstrip() + "\n\n" + block + "\n"
        else:
            current = ""
            new = f"# {data.get('name', path.stem)}\n\n_TODO: describe usage._\n\n{block}\n"
        if new != current:
            stale.append(doc.relative_to(ROOT))
            if not args.check:
                doc.write_text(new, encoding="utf-8", newline="\n")
    if args.check and stale:
        print("Out-of-date docs (run: python scripts/generate_docs.py):")
        for doc in stale:
            print(f"  {doc}")
        return 1
    if not args.check:
        print(f"Updated {len(stale)} doc(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
