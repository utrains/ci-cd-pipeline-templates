# Deploy · Argo CD

Triggers an Argo CD sync and **waits until the app is Synced and Healthy**. Before syncing, it can override
a Helm parameter or a Kustomize image.

> For pure GitOps, where Git is the only source of truth, prefer [gitops-update](gitops-update.md): commit the new
> tag to the config repo and let Argo CD auto-sync. Use this workflow to wait for that sync, or when an
> imperative sync is acceptable.

## Usage

```yaml
jobs:
  deploy:
    needs: image
    permissions:
      contents: read
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/deploy-eks-argocd.yml@v2
    with:
      environment: staging
      argocd_server: argocd.example.com
      argocd_app: orders-staging
      helm_parameters: |
        image.tag=sha-${{ github.sha }}
    secrets:
      argocd_token: ${{ secrets.ARGOCD_TOKEN }}
```

## Notes

- Create a dedicated Argo CD **project-scoped** account token with only `sync`/`get` (and `override` if you use
  parameters) on the target applications.
- Parameter overrides are lost the next time someone changes the Application spec. This is the main reason to prefer GitOps commits.
- The Argo CD CLI is downloaded from the official release and checksum-verified.
- If Argo CD is not reachable from GitHub-hosted runners, set `runs_on` to a self-hosted runner.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`deploy-eks-argocd.yml`](../../.github/workflows/deploy-eks-argocd.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `argocd_server` | string | yes |  | Argo CD API server hostname (no scheme), e.g. argocd.example.com. |
| `argocd_app` | string | yes |  | Argo CD Application name. |
| `helm_parameters` | string | no |  | Newline-separated Helm parameters to set on the app (e.g. image.tag=1.2.3). |
| `kustomize_images` | string | no |  | Newline-separated Kustomize image overrides (e.g. my-app=registry/my-app:1.2.3). |
| `revision` | string | no |  | Git revision to sync to. Empty = the application's target revision. |
| `prune` | boolean | no | `false` | Delete resources that are no longer in Git. |
| `wait_timeout` | number | no | `600` | Seconds to wait for the app to become Synced and Healthy. |
| `grpc_web` | boolean | no | `true` | Use gRPC-Web (needed behind most ingress controllers / load balancers). |
| `argocd_version` | string | no | `v3.5.3` | Argo CD CLI version. |
| `environment` | string | no |  | GitHub Environment to deploy into (approvals, env secrets, deployment history). |
| `environment_url` | string | no |  | URL shown on the deployment in GitHub. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. Use a self-hosted runner if Argo CD is not publicly reachable. |
| `timeout_minutes` | number | no | `20` | Job timeout in minutes. |

### Secrets

| Name | Required | Description |
|---|---|---|
| `argocd_token` | yes | Argo CD API token (project-scoped account token recommended). |

<!-- END GENERATED REFERENCE -->
