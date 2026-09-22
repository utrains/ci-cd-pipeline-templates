# Container · Build, scan & push

Builds an image with BuildKit and runs a **Trivy scan before anything is pushed**, so a vulnerable image never
reaches the registry. It then pushes to **ECR, GHCR, Docker Hub or any registry**, attaches an **SBOM** and **SLSA
provenance**, and can optionally **sign** with cosign keyless.

## Usage: Amazon ECR

```yaml
jobs:
  image:
    permissions:
      contents: read
      id-token: write
      packages: write
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/docker-build.yml@v2
    with:
      image_name: payments/api                 # ECR repository (must exist)
      aws_region: eu-west-1
      push: ${{ github.event_name != 'pull_request' }}
    secrets:
      aws_role: ${{ secrets.AWS_ECR_PUSH_ROLE }}

  deploy:
    needs: image
    # deploy the immutable digest reference:
    #   ${{ needs.image.outputs.image_ref }}
    #   → 123456789012.dkr.ecr.eu-west-1.amazonaws.com/payments/api@sha256:…
```

## Usage: GHCR (no extra secrets)

```yaml
    with:
      registry: ghcr
      image_name: ${{ github.repository }}
```

## Usage: Docker Hub / other registry, multi-arch, signed

```yaml
    with:
      registry: dockerhub                      # or: custom + registry_host: registry.example.com
      image_name: myorg/api
      platforms: linux/amd64,linux/arm64
      sign: true
      build_args: |
        APP_VERSION=${{ github.ref_name }}
    secrets:
      registry_username: ${{ secrets.DOCKERHUB_USERNAME }}
      registry_password: ${{ secrets.DOCKERHUB_TOKEN }}
      build_secrets: |
        npm_token=${{ secrets.NPM_TOKEN }}
```

## Default tags

| Trigger | Tags |
|---|---|
| push to `main` | `main`, `sha-<full sha>` |
| pull request #42 | `pr-42`, `sha-<full sha>` |
| tag `v1.4.2` | `1.4.2`, `1.4`, `sha-<full sha>` |

Deploy with `image_ref` (the digest) or the `sha-<sha>` tag. Both are immutable. Branch tags move.

## Notes

- **Breaking change from v1:** `image_name` is now the repository name only. Before, it was the full URI with a tag.
- Callers must grant `packages: write` even for ECR, because a called workflow cannot request permissions conditionally.
- With an ECR repository set to **immutable tags**, override `tags` to drop `type=ref,event=branch`.
- Layer cache is stored in the GitHub Actions cache, scoped per image.
- The pre-push scan builds the first platform in `platforms` only. The final multi-arch build reuses the cache.
- Verify a signed image:
  `cosign verify <image_ref> --certificate-identity-regexp 'https://github.com/<org>/.*' --certificate-oidc-issuer https://token.actions.githubusercontent.com`

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`docker-build.yml`](../../.github/workflows/docker-build.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
  id-token: write
  packages: write
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `image_name` | string | yes |  | Repository name without registry or tag, e.g. "payments/api" (for GHCR use "<owner>/<name>"). |
| `registry` | string | no | `ecr` | ecr \| ghcr \| dockerhub \| custom |
| `registry_host` | string | no |  | Registry hostname when registry=custom (e.g. registry.example.com). |
| `aws_region` | string | no | `us-east-1` | AWS region. |
| `dockerfile` | string | no | `./Dockerfile` | Path to the Dockerfile. |
| `context` | string | no | `.` | Docker build context. |
| `target` | string | no |  | Multi-stage build target. |
| `build_args` | string | no |  | Newline-separated KEY=VALUE build arguments. |
| `platforms` | string | no | `linux/amd64` | Comma-separated target platforms, e.g. linux/amd64,linux/arm64. |
| `tags` | string | no | `type=ref,event=branch`<br>`type=ref,event=pr`<br>`type=semver,pattern={{version}}`<br>`type=semver,pattern={{major}}.{{minor}}`<br>`type=sha,format=long` | docker/metadata-action tag rules (newline-separated). |
| `push` | boolean | no | `true` | Push the image. Set to false on pull requests to only build (and scan). |
| `scan_image` | boolean | no | `true` | Scan the image with Trivy before pushing; the push is blocked on findings. |
| `scan_severity` | string | no | `CRITICAL,HIGH` | Severities that block the push. |
| `sbom` | boolean | no | `true` | Attach an SBOM attestation. |
| `provenance` | boolean | no | `true` | Attach SLSA provenance (mode=max). |
| `sign` | boolean | no | `false` | Sign the pushed image with cosign keyless (Sigstore / GitHub OIDC). |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |
| `timeout_minutes` | number | no | `45` | Job timeout in minutes. |

### Secrets

| Name | Required | Description |
|---|---|---|
| `aws_role` | no | IAM role ARN to assume via OIDC (registry=ecr). |
| `registry_username` | no | Username for dockerhub / custom registries. |
| `registry_password` | no | Password / token for dockerhub / custom registries (optional for ghcr; defaults to GITHUB_TOKEN). |
| `build_secrets` | no | Newline-separated id=value BuildKit secrets (mounted with RUN --mount=type=secret). |

### Outputs

| Name | Description |
|---|---|
| `image` | Fully qualified image repository (registry/name). |
| `digest` | Image digest (sha256:...). Empty when push=false. |
| `image_ref` | Immutable reference image@digest. Use this for deployments. |
| `version` | Primary version tag computed by docker/metadata-action. |
| `tags` | All tags that were applied (newline-separated). |

<!-- END GENERATED REFERENCE -->
