# Quality · PR title lint

Requires pull-request titles to follow [Conventional Commits](https://www.conventionalcommits.org/),
e.g. `feat(api): add refunds endpoint`. With squash merges, the PR title becomes the commit message,
which gives a clean history and reliable release notes.

## Usage

```yaml
on:
  pull_request:
    types: [opened, edited, synchronize, reopened]

jobs:
  pr_title:
    permissions:
      pull-requests: read
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/pr-title-lint.yml@v2
    with:
      scopes: |
        api
        web
        infra
```

Include the `edited` event type so the check re-runs when someone fixes the title.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`pr-title-lint.yml`](../../.github/workflows/pr-title-lint.yml)

### Permissions the calling job must grant

```yaml
permissions:
  pull-requests: read
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `types` | string | no |  | Newline-separated allowed types. Empty = the Conventional Commits defaults. |
| `scopes` | string | no |  | Newline-separated allowed scopes. Empty = any scope. |
| `require_scope` | boolean | no | `false` | Require a scope, e.g. feat(api): ... |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |

<!-- END GENERATED REFERENCE -->
