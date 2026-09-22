# Infra · Terraform

A full Terraform lifecycle in one call:

1. **plan job:** `fmt -check` → `init` → `validate` → `tflint` → `plan -out=tfplan`. The plan is posted as a
   PR comment, and the comment is updated on each push.
2. **apply job** (`action: apply` and only if there are changes): runs inside a **GitHub Environment**. Give it
   required reviewers for a manual approval. It applies **the exact saved plan** that was reviewed.

## Usage: plan on PRs, apply on main

```yaml
jobs:
  infra:
    permissions:
      contents: read
      id-token: write
      pull-requests: write
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/terraform.yml@v2
    with:
      working_directory: infra/envs/prod
      action: ${{ github.event_name == 'push' && 'apply' || 'plan' }}
      environment: prod-infra
      var_file: prod.tfvars
      backend_config: |
        bucket=my-tf-state-prod
        key=network/terraform.tfstate
        region=us-east-1
    secrets:
      aws_role_to_assume: ${{ secrets.AWS_TF_ROLE_PROD }}
```

## Notes

- **Breaking change from v1:** `tf_version` now defaults to `1.16.3`. Pin it to the version that wrote your state.
- Use **separate IAM roles** for plan and apply where possible. Make the plan role read-only, and limit the apply role's trust
  policy to the environment (`token.actions.githubusercontent.com:sub = repo:<org>/<repo>:environment:prod-infra`).
- The plan artifact can contain sensitive values. It is kept for 1 day only, so restrict who can read the repository's Actions artifacts.
- `tflint` reads `.tflint.hcl` for provider rulesets (for example the AWS plugin).
- Runs on the same directory and workspace are queued. An apply is never cancelled halfway.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`terraform.yml`](../../.github/workflows/terraform.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
  id-token: write
  pull-requests: write
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `action` | string | no | `plan` | plan \| apply |
| `tf_version` | string | no | `1.16.3` | Terraform version; pin it to the version that manages your state. |
| `working_directory` | string | no | `./` | Terraform root module directory. |
| `backend_config` | string | no |  | Newline-separated -backend-config values (key=value) or a backend config file path. |
| `var_file` | string | no |  | Path to a .tfvars file, relative to working_directory. |
| `workspace` | string | no |  | Terraform workspace to select (created if missing). |
| `run_tflint` | boolean | no | `true` | Run TFLint. |
| `fmt_check` | boolean | no | `true` | Fail when files are not formatted with `terraform fmt`. |
| `comment_on_pr` | boolean | no | `true` | Post / update the plan as a pull-request comment. |
| `environment` | string | no |  | GitHub Environment that gates the apply job (required when action=apply). |
| `aws_region` | string | no | `us-east-1` | AWS region. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |
| `timeout_minutes` | number | no | `60` | Job timeout in minutes. |

### Secrets

| Name | Required | Description |
|---|---|---|
| `aws_role_to_assume` | no | IAM role ARN to assume via OIDC. Omit for non-AWS providers. |
| `tf_api_token` | no | HCP Terraform / Terraform Enterprise API token (remote backend or private registry). |

### Outputs

| Name | Description |
|---|---|
| `has_changes` | 'true' when the plan contains changes. |

<!-- END GENERATED REFERENCE -->
