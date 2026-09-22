# Gate · Manual approval

A pipeline stage that **waits for a human approval** before later jobs run. The approval comes from the
target GitHub Environment's **required reviewers**.

## Setup (once per repository)

Go to **Settings → Environments → New environment** (e.g. `prod`):
- **Required reviewers:** add people or teams. Up to 6; one approval is enough.
- Optionally turn on **Prevent self-review**, set a **wait timer**, and choose **Deployment branches and tags** (e.g. only `main` and `v*`).

## Usage

```yaml
jobs:
  approve_prod:
    needs: deploy_staging
    permissions:
      contents: read
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/approval.yml@v2
    with:
      environment: prod
      message: "Release ${{ github.ref_name }} passed staging. Approve to deploy to production."

  deploy_prod:
    needs: approve_prod
    # ...
```

## When to use it

Every deploy workflow here (`ecs-deploy`, `deploy-eks-helm`, `deploy-eks-argocd`, `terraform`) accepts an
`environment` input, and that input gates the job directly. Use this separate gate when **one approval should cover
several jobs**, for example a database migration followed by an app deploy.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`approval.yml`](../../.github/workflows/approval.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `environment` | string | yes |  | GitHub Environment with required reviewers configured. |
| `message` | string | no | `Deployment approval required.` | Context shown to approvers in the run summary. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |

<!-- END GENERATED REFERENCE -->
