# Deploy · Amazon ECS

Deploys a new image to an ECS service:
1. It takes the service's current task definition, or a JSON file from the repo.
2. It swaps the container image and registers a new revision.
3. It updates the service and **waits until it is stable**.

## Usage

```yaml
jobs:
  deploy_prod:
    needs: image
    permissions:
      contents: read
      id-token: write
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/ecs-deploy.yml@v2
    with:
      environment: prod                          # GitHub Environment → approvals + history
      environment_url: https://app.example.com
      cluster: prod-cluster
      service: payments-api
      container_name: api
      image: ${{ needs.image.outputs.image_ref }}
      aws_region: eu-west-1
    secrets:
      aws_role: ${{ secrets.AWS_ECS_DEPLOY_ROLE_PROD }}
```

## Notes

- **Breaking change from v1:** `container_name` is now required, and the `image` input is actually applied.
  v1 only forced a redeploy of the old task definition.
- Turn on the ECS **deployment circuit breaker with rollback** on the service, so a failed rollout reverts on its own.
- Deploys to the same cluster/service are queued, never run in parallel.
- Minimal IAM for the role: `ecs:DescribeServices`, `ecs:DescribeTaskDefinition`, `ecs:RegisterTaskDefinition`,
  `ecs:UpdateService`, and `iam:PassRole` on the task and execution roles.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`ecs-deploy.yml`](../../.github/workflows/ecs-deploy.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
  id-token: write
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `cluster` | string | yes |  | ECS cluster name. |
| `service` | string | yes |  | ECS service name. |
| `image` | string | yes |  | Image to deploy. Prefer the immutable image_ref (image@sha256:...) output of docker-build.yml. |
| `container_name` | string | yes |  | Name of the container in the task definition that receives the new image. |
| `task_definition_file` | string | no |  | Task-definition JSON in the calling repo. Empty = start from the service's current task definition. |
| `environment_variables` | string | no |  | Newline-separated KEY=VALUE pairs to set on the container. |
| `aws_region` | string | no | `us-east-1` | AWS region. |
| `environment` | string | no |  | GitHub Environment to deploy into (enables approvals, environment secrets and deployment history). |
| `environment_url` | string | no |  | URL shown on the deployment in GitHub. |
| `wait_for_stability` | boolean | no | `true` | Wait for the ECS service to reach a steady state. |
| `wait_minutes` | number | no | `15` | Maximum minutes to wait for the service to stabilise. |
| `timeout_minutes` | number | no | `30` | Job timeout; keep it above wait_minutes. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |

### Secrets

| Name | Required | Description |
|---|---|---|
| `aws_role` | yes | IAM role ARN to assume via OIDC. |

### Outputs

| Name | Description |
|---|---|
| `task_definition_arn` | ARN of the task-definition revision that was deployed. |

<!-- END GENERATED REFERENCE -->
