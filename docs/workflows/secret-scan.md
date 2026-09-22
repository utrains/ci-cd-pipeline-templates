# Scan · Secrets (gitleaks)

Detects committed credentials with [gitleaks](https://github.com/gitleaks/gitleaks). The binary is
downloaded from the official release and **checksum-verified**. Findings are redacted in the logs and
uploaded to code scanning.

| Event | Scope scanned |
|---|---|
| `pull_request` | only the PR's commits |
| `push` | only the pushed commits |
| anything else, or `full_history: true` | the entire history |

## Usage

```yaml
jobs:
  secrets:
    permissions:
      contents: read
      security-events: write
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/secret-scan.yml@v2
```

Run a nightly full-history sweep as well (see [examples/scheduled-security.yml](../../examples/scheduled-security.yml)):

```yaml
    with:
      full_history: true
```

## Handling false positives

Add a `.gitleaks.toml` to the repo, for example an allowlist of test fixtures, or put a
`gitleaks:allow` comment on the offending line. **Rotate any real secret that was found.**
Removing it from git does not make it safe again.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`secret-scan.yml`](../../.github/workflows/secret-scan.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
  security-events: write
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `gitleaks_version` | string | no | `8.30.1` | gitleaks release to install (without the leading v). |
| `config_path` | string | no |  | Path to a .gitleaks.toml in the calling repository. Empty = gitleaks defaults (or .gitleaks.toml at the root, if present). |
| `full_history` | boolean | no | `false` | Always scan the full git history, regardless of the event. |
| `upload_sarif` | boolean | no | `true` | Upload findings to GitHub code scanning (needs security-events write). |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |

<!-- END GENERATED REFERENCE -->
