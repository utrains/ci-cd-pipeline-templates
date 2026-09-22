# Deploy · EKS (Helm)

Runs `helm upgrade --install` into an Amazon EKS cluster with `--atomic --wait`. **If the release does not become
healthy, it rolls back automatically.**

## Usage

```yaml
jobs:
  deploy:
    needs: image
    permissions:
      contents: read
      id-token: write
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/deploy-eks-helm.yml@v2
    with:
      environment: production
      cluster_name: prod-eks
      aws_region: us-east-1
      namespace: orders
      release_name: orders
      chart: ./charts/orders                       # or oci://… with chart_version
      values_files: |
        ./charts/orders/values.yaml
        ./charts/orders/values-production.yaml
      image_repository: ${{ needs.image.outputs.image }}
      image_tag: sha-${{ github.sha }}
      set_values: |
        replicaCount=3
    secrets:
      aws_role: ${{ secrets.AWS_EKS_DEPLOY_ROLE }}
```

## Prerequisites

The IAM role needs `eks:DescribeCluster`, and it must be mapped to Kubernetes RBAC. Use an **EKS access entry**, scoped
to the namespace where possible:

```bash
aws eks create-access-entry --cluster-name prod-eks --principal-arn <role-arn>
aws eks associate-access-policy --cluster-name prod-eks --principal-arn <role-arn> \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSEditPolicy \
  --access-scope type=namespace,namespaces=orders
```

## Notes

- `dry_run: true` renders the chart and validates it against the API server (`--dry-run=server`) without changing anything.
- The default Helm is 3.x. Helm 4 renamed several flags, including `--atomic`, so test before you raise `helm_version`.
- The EKS API endpoint must be reachable from the runner. For private clusters, use self-hosted runners in the VPC.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`deploy-eks-helm.yml`](../../.github/workflows/deploy-eks-helm.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
  id-token: write
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `cluster_name` | string | yes |  | EKS cluster name. |
| `aws_region` | string | no | `us-east-1` | AWS region. |
| `namespace` | string | yes |  | Kubernetes namespace of the release. |
| `release_name` | string | yes |  | Helm release name. |
| `chart` | string | yes |  | Local chart path (./charts/app), repo/chart, or oci:// reference. |
| `chart_version` | string | no |  | Chart version (for remote charts). |
| `values_files` | string | no |  | Newline-separated values files, applied in order. |
| `set_values` | string | no |  | Newline-separated key=value overrides (passed with --set). |
| `image_repository` | string | no |  | Sets image.repository (leave empty to keep the chart value). |
| `image_tag` | string | no |  | Sets image.tag (leave empty to keep the chart value). |
| `create_namespace` | boolean | no | `false` | Create the namespace if it does not exist. |
| `atomic` | boolean | no | `true` | Roll back automatically when the upgrade fails. |
| `helm_timeout` | string | no | `10m` | Time to wait for the release to become ready (Go duration). |
| `dry_run` | boolean | no | `false` | Render and validate against the cluster without changing anything. |
| `helm_version` | string | no | `v3.22.0` | Helm version (3.x recommended). |
| `environment` | string | no |  | GitHub Environment to deploy into (approvals, env secrets, deployment history). |
| `environment_url` | string | no |  | URL shown on the deployment in GitHub. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |
| `timeout_minutes` | number | no | `30` | Job timeout in minutes. |

### Secrets

| Name | Required | Description |
|---|---|---|
| `aws_role` | yes | IAM role ARN to assume via OIDC. It must be mapped to Kubernetes RBAC (EKS access entry). |

<!-- END GENERATED REFERENCE -->
