# Scan · Dependency review

On pull requests, compares the dependency manifests and lockfiles between base and head. It fails when the
PR **introduces** a vulnerable package above the severity threshold, or a license you disallow.

## Usage

```yaml
on: pull_request

jobs:
  dependency_review:
    permissions:
      contents: read
      pull-requests: write
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/dependency-review.yml@v2
    with:
      fail_on_severity: high
      deny_licenses: GPL-3.0-only, AGPL-3.0-only
```

## Notes

- It is skipped automatically on non-PR events, so it is safe to call from a shared pipeline.
- It needs the dependency graph, which is on by default for public repos. Private repos need GitHub Advanced Security.
- For central policy, keep a config file in a shared repo and pass `config_file: org/policies/.github/dependency-review.yml@main`.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`dependency-review.yml`](../../.github/workflows/dependency-review.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
  pull-requests: write
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `fail_on_severity` | string | no | `high` | low \| moderate \| high \| critical |
| `fail_on_scopes` | string | no | `runtime` | Comma-separated dependency scopes to check (runtime, development, unknown). |
| `allow_licenses` | string | no |  | Comma-separated SPDX licenses that are allowed (mutually exclusive with deny_licenses). |
| `deny_licenses` | string | no |  | Comma-separated SPDX licenses that are denied (e.g. "GPL-3.0-only, AGPL-3.0-only"). |
| `config_file` | string | no |  | Path to a dependency-review config file (overrides the inputs above). |
| `comment_summary` | string | no | `on-failure` | Post a summary comment on the PR: always \| on-failure \| never |
| `warn_only` | boolean | no | `false` | Report findings without failing the check. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |

<!-- END GENERATED REFERENCE -->
