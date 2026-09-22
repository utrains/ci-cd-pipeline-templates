# Getting started

This guide covers the one-time setup to use the templates from your application repositories. It
takes about 30 minutes for a new AWS account and GitHub organization.

- [1. Let repositories call the templates](#1-let-repositories-call-the-templates)
- [2. Connect GitHub to AWS with OIDC (no access keys)](#2-connect-github-to-aws-with-oidc-no-access-keys)
- [3. Create environments and approvals](#3-create-environments-and-approvals)
- [4. Add secrets and variables](#4-add-secrets-and-variables)
- [5. Write your first pipeline](#5-write-your-first-pipeline)
- [6. Recommended organization settings](#6-recommended-organization-settings)
- [Troubleshooting](#troubleshooting)

---

## 1. Let repositories call the templates

| Template repo visibility | What to do |
|---|---|
| **Public** | Nothing. Any repository can call it. |
| **Internal / private** | In *this* repo go to **Settings → Actions → General → Access**, and choose *Accessible from repositories in the organization* (or enterprise). |

Callers reference a template as `<org>/<repo>/.github/workflows/<file>.yml@<ref>`, for example:

```yaml
uses: utrains/ci-cd-pipeline-templates/.github/workflows/build-node.yml@v2
```

## 2. Connect GitHub to AWS with OIDC (no access keys)

Templates that touch AWS (`docker-build`, `ecs-deploy`, `deploy-eks-helm`, `terraform`, `trivy-scan` with ECR)
assume an IAM role through GitHub's OIDC provider. Each job gets short-lived credentials, and no access keys are stored anywhere.

### 2.1 Create the identity provider (once per AWS account)

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com
```

### 2.2 Create one role per purpose and environment

Scope the trust policy to **the repository and the environment** that may assume the role, so a PR build
can never assume the production deploy role:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com" },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
        "token.actions.githubusercontent.com:sub": "repo:<ORG>/<REPO>:environment:prod"
      }
    }
  }]
}
```

Useful `sub` patterns:

| Job | `sub` claim |
|---|---|
| Runs in environment `prod` | `repo:<ORG>/<REPO>:environment:prod` |
| Push to `main`, no environment | `repo:<ORG>/<REPO>:ref:refs/heads/main` |
| Any pull request (read-only roles only) | `repo:<ORG>/<REPO>:pull_request` |

> A job that declares an `environment:` gets the environment-based `sub`, **not** the branch-based one.
> Match the trust policy to how the template is called.

The same setup in Terraform:

```hcl
resource "aws_iam_openid_connect_provider" "github" {
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
}

data "aws_iam_policy_document" "deploy_prod_trust" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:my-org/web-app:environment:prod"]
    }
  }
}

resource "aws_iam_role" "deploy_prod" {
  name               = "gha-web-app-deploy-prod"
  assume_role_policy = data.aws_iam_policy_document.deploy_prod_trust.json
  max_session_duration = 3600
}
```

### 2.3 Permissions each role needs

| Role for | Minimum permissions |
|---|---|
| `docker-build` (ECR push) | `ecr:GetAuthorizationToken`, plus on the repository: `ecr:BatchCheckLayerAvailability`, `ecr:InitiateLayerUpload`, `ecr:UploadLayerPart`, `ecr:CompleteLayerUpload`, `ecr:PutImage`, `ecr:BatchGetImage`, `ecr:GetDownloadUrlForLayer` |
| `trivy-scan` (ECR pull) | `ecr:GetAuthorizationToken`, `ecr:BatchGetImage`, `ecr:GetDownloadUrlForLayer` |
| `ecs-deploy` | `ecs:DescribeServices`, `ecs:DescribeTaskDefinition`, `ecs:RegisterTaskDefinition`, `ecs:UpdateService`, `iam:PassRole` (task and execution roles) |
| `deploy-eks-helm` | `eks:DescribeCluster`, plus an EKS access entry with a namespace-scoped policy (see [deploy-eks-helm](workflows/deploy-eks-helm.md#prerequisites)) |
| `terraform` | Plan role: read-only plus state bucket and lock access. Apply role: whatever the infrastructure needs |

## 3. Create environments and approvals

In each application repository go to **Settings → Environments** and create, for example:

| Environment | Protection rules |
|---|---|
| `dev` | Deployment branches: `main` |
| `staging` | Deployment branches: `main`, tags `v*` |
| `prod` | **Required reviewers** (a team), **prevent self-review**, deployment branches: `main`, tags `v*` |
| `prod-infra` | Required reviewers (platform team), deployment branches: `main` |

Put secrets that differ per environment (deploy role ARNs, API tokens) into the **environment's** secrets.
They are only released to jobs that run in that environment, after approval.

## 4. Add secrets and variables

Suggested names, as used in the examples:

| Name | Scope | Used by |
|---|---|---|
| `AWS_DEPLOY_ROLE_DEV` / `_PROD` | environment secret | docker-build, ecs-deploy, deploy-eks-helm |
| `AWS_TF_ROLE_DEV` / `_PROD` | environment secret | terraform |
| `SONAR_TOKEN` | org secret (selected repos) | sonar |
| `SLACK_WEBHOOK_URL` | org or repo secret | notify-slack |
| `ARGOCD_TOKEN` | environment secret | deploy-eks-argocd |
| `GITOPS_TOKEN` | org secret (GitHub App token recommended) | gitops-update |

A reusable workflow **only receives the secrets you pass explicitly** under `secrets:`. `secrets: inherit` also works,
but explicit passing makes clear what each template can see.

## 5. Write your first pipeline

```yaml
# .github/workflows/pipeline.yml
name: Pipeline
on:
  pull_request:
  push:
    branches: [main]

permissions: {}            # nothing by default; grant per job

jobs:
  build:
    permissions:
      contents: read
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/build-node.yml@v2

  secrets:
    permissions:
      contents: read
      security-events: write
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/secret-scan.yml@v2

  image:
    needs: [build, secrets]
    permissions:
      contents: read
      id-token: write
      packages: write
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/docker-build.yml@v2
    with:
      image_name: web-app
      push: ${{ github.event_name != 'pull_request' }}
    secrets:
      aws_role: ${{ secrets.AWS_DEPLOY_ROLE_DEV }}
```

Then grow it using the [examples](../examples/).

**Passing data between templates:** use `needs.<job>.outputs.<output>`, e.g.
`image: ${{ needs.image.outputs.image_ref }}`. Artifacts (build output, coverage) are shared between jobs
of the same run by name.

## 6. Recommended organization settings

- **Settings → Actions → General → Policies:** allow only actions from your org plus selected verified creators.
  Turn on **Require actions to be pinned to a full-length commit SHA**.
- **Workflow permissions:** set the default `GITHUB_TOKEN` to **read-only**. The templates request what they need.
- **Branch protection / rulesets** on `main` in this repository: require PR review from CODEOWNERS and require the
  `Self CI` checks to pass.
- **Code security:** turn on the dependency graph, Dependabot alerts, secret scanning and push protection.

---

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `The nested job 'x' is requesting 'id-token: write', but is only allowed 'id-token: none'` | The calling job must grant every permission the template needs. See the *Permissions* block on the template's doc page. |
| `workflow was not found` / `access denied` when calling | The template repo is private or internal and not shared. See [step 1](#1-let-repositories-call-the-templates). |
| `Not authorized to perform sts:AssumeRoleWithWebIdentity` | The trust policy's `sub` doesn't match. Jobs with `environment:` use `repo:ORG/REPO:environment:NAME`. |
| `Resource not accessible by integration` when uploading SARIF | The caller didn't grant `security-events: write`, or code scanning is not available for the repo (private repo without Advanced Security). Set `upload_sarif: false`. |
| Deploy waits forever | The environment has required reviewers. Approve it in the run's summary page. |
| `Error: Input required and not supplied: aws-region` | You passed an empty `aws_region`. Leave it out to use the default. |
