# Release · Drafter + changelog

- On every push to `main`, it keeps a **draft GitHub Release** up to date from merged PRs. PRs are grouped by label, and the
  next version is worked out from labels (`breaking-change` = major, `feature` = minor, anything else = patch).
- When the release is **published**, it opens a PR that adds the release notes to `CHANGELOG.md`. It uses a PR so that
  branch protection is respected.

It runs for this repository and can be called from others.

## Usage from an application repo

```yaml
name: Release
on:
  push:
    branches: [main]
  release:
    types: [published]

jobs:
  release:
    permissions:
      contents: write
      pull-requests: write
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/release-drafter.yml@v2
```

The calling repo needs its own `.github/release-drafter.yml`. Copy [this repo's config](../../.github/release-drafter.yml) as a start.

## Notes

- Label every PR. The PR template in this repo lists the labels.
- PRs labelled `skip-changelog` are left out of the notes.
- The changelog PR is created with `GITHUB_TOKEN`, which **does not trigger other workflows**. If CI must run on it,
  use a GitHub App token.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`release-drafter.yml`](../../.github/workflows/release-drafter.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: write
  pull-requests: write
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `config_name` | string | no | `release-drafter.yml` | Release Drafter config file in the calling repo's .github directory. |
| `changelog_file` | string | no | `CHANGELOG.md` | Changelog file to update when a release is published. |

<!-- END GENERATED REFERENCE -->
