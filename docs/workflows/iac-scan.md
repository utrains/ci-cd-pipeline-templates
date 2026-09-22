# Scan · IaC (Checkov)

Policy-as-code checks for Terraform, CloudFormation, Kubernetes manifests, Helm charts, Dockerfiles and
GitHub Actions: more than 1,000 built-in checks for CIS and AWS best practices.

## Usage

```yaml
jobs:
  iac:
    permissions:
      contents: read
      security-events: write
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/iac-scan.yml@v2
    with:
      directory: infra/
      framework: terraform
      skip_check: CKV_AWS_144,CKV2_AWS_62   # document why in the PR
```

## Notes

- Suppress a finding inline with `#checkov:skip=CKV_AWS_18:Access logs go to central bucket`.
- `soft_fail: true` reports without failing. It is useful while you adopt the tool on an existing codebase.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`iac-scan.yml`](../../.github/workflows/iac-scan.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
  security-events: write
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `directory` | string | no | `.` | Directory to scan. |
| `framework` | string | no |  | Comma-separated frameworks (terraform, kubernetes, helm, dockerfile, cloudformation, github_actions, ...). Empty = all. |
| `skip_check` | string | no |  | Comma-separated check IDs to skip (e.g. CKV_AWS_18,CKV_AWS_144). |
| `config_file` | string | no |  | Path to a .checkov.yaml config file. |
| `soft_fail` | boolean | no | `false` | Report findings without failing the job. |
| `download_external_modules` | boolean | no | `true` | Download external Terraform modules before scanning. |
| `upload_sarif` | boolean | no | `true` | Upload findings to GitHub code scanning (needs security-events write). |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |

<!-- END GENERATED REFERENCE -->
