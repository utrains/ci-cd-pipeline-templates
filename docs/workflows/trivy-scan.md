# Scan · Trivy

Vulnerability, misconfiguration and secret scanning with Trivy. It makes two passes:
1. The full result goes to GitHub code scanning as SARIF.
2. A table goes to the log, and this pass is the gate that fails the job.

## Usage: scan an image already in a registry

```yaml
jobs:
  scan:
    needs: image
    permissions:
      contents: read
      id-token: write
      security-events: write
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/trivy-scan.yml@v2
    with:
      scan_type: image
      image: ${{ needs.image.outputs.image_ref }}
      registry: ecr
    secrets:
      aws_role: ${{ secrets.AWS_ECR_READ_ROLE }}
```

## Usage: scan the repository's dependencies

```yaml
    with:
      scan_type: fs
```

## Usage: scan IaC for misconfigurations

```yaml
    with:
      scan_type: config
      scan_ref: infra/
```

## Notes

- [docker-build](docker-build.md) already scans images **before** pushing. Use this workflow for
  scheduled re-scans of images that are already deployed, where new CVEs show up daily, or for fs/config scans.
- To accept a known risk, add its CVE ID to `.trivyignore` with a comment and an expiry date (`exp:2026-12-31`).
- Set `fail_on_findings: false` for report-only runs, for example nightly scans.
- `id-token: write` is always requested (needed for `registry: ecr`), so callers must grant it.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`trivy-scan.yml`](../../.github/workflows/trivy-scan.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
  id-token: write
  security-events: write
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `scan_type` | string | no | `image` | image \| fs \| config |
| `image` | string | no |  | Image reference to scan (required when scan_type=image). |
| `scan_ref` | string | no | `.` | Path to scan for fs / config scans. |
| `severity` | string | no | `CRITICAL,HIGH` | Severities that fail the job. |
| `ignore_unfixed` | boolean | no | `true` | Ignore vulnerabilities without an available fix. |
| `fail_on_findings` | boolean | no | `true` | Fail the job when findings at the given severity exist. |
| `trivyignores` | string | no | `.trivyignore` | Path to a .trivyignore file in the calling repository. |
| `upload_sarif` | boolean | no | `true` | Upload results to GitHub code scanning (needs security-events write). |
| `registry` | string | no | `none` | Registry login before pulling the image: none \| ecr |
| `aws_region` | string | no | `us-east-1` | AWS region. |
| `trivy_version` | string | no | `v0.70.0` | Trivy version. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |
| `timeout_minutes` | number | no | `20` | Job timeout in minutes. |

### Secrets

| Name | Required | Description |
|---|---|---|
| `aws_role` | no | IAM role ARN used to pull from ECR (registry=ecr). |

<!-- END GENERATED REFERENCE -->
