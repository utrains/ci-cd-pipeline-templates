# Deploy · GitOps image bump

Sets a YAML value (usually the image tag) in a **GitOps config repository**. By default it opens a pull
request, so the change is reviewable and the merge is the approval. It can also commit directly for
lower environments.

## Usage

```yaml
jobs:
  bump_prod:
    needs: image
    permissions:
      contents: read
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/gitops-update.yml@v2
    with:
      config_repo: my-org/k8s-config
      file_path: apps/orders/prod/values.yaml
      yaml_path: .image.tag
      value: sha-${{ github.sha }}
      create_pr: true          # false = commit straight to config_branch (dev/staging)
    secrets:
      gitops_token: ${{ secrets.GITOPS_TOKEN }}
```

## Notes

- `GITHUB_TOKEN` cannot write to another repository. Use a **GitHub App** installation token:
  `actions/create-github-app-token` in the caller, passed as `gitops_token`. A fine-grained PAT scoped to the config repo
  also works, with Contents and Pull requests set to Read & write.
- `yaml_path` uses [yq](https://mikefarah.gitbook.io/yq/) syntax, e.g. `.spec.template.spec.containers[0].image`,
  or `.images[0].newTag` for a Kustomize `kustomization.yaml`.
- In direct-commit mode, a rejected push is retried with a rebase up to three times.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`gitops-update.yml`](../../.github/workflows/gitops-update.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `config_repo` | string | yes |  | owner/name of the GitOps config repository. |
| `config_branch` | string | no | `main` | Branch of the config repository to update / target with the PR. |
| `file_path` | string | yes |  | YAML file to edit, e.g. envs/prod/values.yaml. |
| `yaml_path` | string | no | `.image.tag` | yq path of the value to set, e.g. .image.tag |
| `value` | string | yes |  | New value, e.g. the image tag or digest. |
| `create_pr` | boolean | no | `true` | Open a pull request instead of committing directly to config_branch. |
| `pr_labels` | string | no | `gitops,automated` | Comma-separated labels for the pull request. |
| `commit_message` | string | no |  | Commit message / PR title. Empty = generated. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |

### Secrets

| Name | Required | Description |
|---|---|---|
| `gitops_token` | yes | Token with contents (+ pull-requests) write on config_repo — a GitHub App token is recommended. |

### Outputs

| Name | Description |
|---|---|
| `pull_request_url` | URL of the pull request opened in the config repo (create_pr=true). |

<!-- END GENERATED REFERENCE -->
