## What & why

<!-- What does this change and why is it needed? -->

## Type

<!-- Add ONE label to the PR; it drives the release version and notes: -->
<!-- breaking-change (major) · feature (minor) · fix / change / security / documentation (patch) -->

## Checklist

- [ ] Any new action is pinned to a full commit SHA with a `# vX.Y.Z` comment
- [ ] New or changed inputs, secrets or outputs are documented in `docs/workflows/`
- [ ] Job-level `permissions:` are least-privilege, and the doc lists what callers must grant
- [ ] Untrusted values reach `run:` only through `env:` (no `${{ }}` inside scripts)
- [ ] Breaking changes (renamed or removed inputs, changed defaults) carry the `breaking-change` label and a note in CHANGELOG.md
- [ ] Tested from a caller repository (link to the run):
