# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/). New releases are added automatically by
[`release-drafter.yml`](.github/workflows/release-drafter.yml).

## [Unreleased]

## [v2.0.0] - 2026-09-21

A hardening release. Every template was rewritten for supply-chain security, least privilege and safe deployments,
and nine templates were added. **This release contains breaking changes. See "Migrating from v1" below.**

### Added
- `build-python.yml`: pip, poetry and uv; lint, pytest, optional wheel build.
- `codeql.yml`: CodeQL SAST, multi-language matrix.
- `dependency-review.yml`: blocks PRs that add vulnerable or disallowed-license dependencies.
- `secret-scan.yml`: gitleaks (checksum-verified), PR-diff, push-range or full-history scanning, SARIF upload.
- `iac-scan.yml`: Checkov policy-as-code for Terraform, Kubernetes, Helm, Dockerfile and GitHub Actions.
- `deploy-eks-helm.yml`: atomic Helm upgrade into EKS with automatic rollback.
- `deploy-eks-argocd.yml`: Argo CD sync and wait for health. Both of these EKS templates were documented in v1 but never existed.
- `gitops-update.yml`: bumps an image tag in a GitOps config repo, by PR or direct commit.
- `approval.yml`: environment-backed manual approval gate. It replaces the empty `approval.yml.bk`.
- `notify-slack.yml`: Block Kit status messages.
- `pr-title-lint.yml`: Conventional Commit PR titles.
- `release-drafter.yml` can now be called from other repositories.
- Every template: a `runs_on` input (label or JSON array for self-hosted runners) and job timeouts.
- `examples/`: five complete caller pipelines (Node→ECS, Java→EKS/Helm, Python→GitOps/Argo CD, Terraform, scheduled security).
- `docs/`: getting-started guide, and one page per template with generated reference tables.
- Repository tooling: `self-ci.yml` (actionlint, zizmor, docs check), Dependabot for actions, CODEOWNERS, PR template.

### Changed
- All third-party actions are pinned to full commit SHAs and updated to their current major versions.
- All jobs declare least-privilege `permissions`. Inputs reach shell scripts through `env:` only, which closes script injection.
- `build-node.yml`: the default install is `npm ci` (was `npm install`) and the default Node is 24 (was 20). Adds lint and test steps, caching and artifact uploads.
- `build-java.yml`: default JDK 21 (was 17), `clean verify` (was `clean package`), Gradle support, wrapper detection, test report upload.
- `build-dotnet.yml`: default SDK `10.0.x` (was `8.0`), `--no-restore`/`--no-build` chaining, coverage, TRX results, optional publish.
- `build-go.yml`: the Go version is read from `go.mod` by default. Adds golangci-lint, the race detector and coverage.
- `sonar.yml`: scanner action v8, and the quality gate uses `sonar.qualitygate.wait` (the separate gate action is removed). Adds SonarCloud `organization` and coverage-artifact download.
- `docker-build.yml`: Buildx with GHA cache, metadata-based tags, Trivy scan **before** push, SBOM and provenance attestations, optional cosign signing, multi-arch builds, and GHCR, Docker Hub and custom registries.
- `terraform.yml`: fmt check, tflint, plan posted as a PR comment, and `action: apply` applies the saved plan in an environment-gated job. Default Terraform is 1.16.3 (was 1.9.5).
- `trivy-scan.yml` (was `trivy-scan.yaml`): uses the official action, supports `image`, `fs` and `config` scans and private ECR, uploads SARIF and fails on findings.
- `release-drafter.yml`: CHANGELOG updates arrive as a PR instead of a direct push to `main`. Labels drive the version.

### Fixed
- `ecs-deploy.yml` ignored its `image` input and only force-redeployed the existing task definition.
- `release-drafter.yml` referenced `release-drafter.yml` while the config file was named `.yaml`. It also interpolated the
  release body into a shell script (script injection) and failed when `CHANGELOG.md` was missing.
- `trivy-scan.yaml` downloaded a hard-coded Trivy 0.50.2 package from a `latest` URL and never failed on vulnerabilities.
- The README's examples used inconsistent template paths (`Utrains/pipeline-templates`, `Utrains-pipeline-templates`).

### Security
- The Slack webhook URL is now a secret instead of a plain input that showed up in logs.
- Downloaded binaries (gitleaks, Argo CD CLI) are verified against the published checksums.

### Migrating from v1

| Template | Change needed in the caller |
|---|---|
| all | Add `permissions:` to each calling job, as listed on each template's doc page. |
| `docker-build` | `image_name` is now the **repository name only** (e.g. `web-app`, not `…amazonaws.com/web-app:latest`). Grant `packages: write`. Use the `image_ref` output to deploy. |
| `ecs-deploy` | Add the required `container_name`. Pass `image: ${{ needs.<build>.outputs.image_ref }}`. |
| `slack-team-notifica` | Switch to `notify-slack.yml` and move `webhook_url` to `secrets: slack_webhook_url`. |
| `trivy-scan.yaml` | Change the file name to `trivy-scan.yml`. Grant `security-events: write` and `id-token: write`. |
| `build-node` | If you have no lockfile, set `install_cmd: npm install`. Set `node_version: "20"` to keep the old runtime. |
| `build-java` | Set `java_version: "17"` to keep the old JDK. |
| `build-dotnet` | Set `dotnet_version: "8.0.x"` to keep the old SDK. |
| `terraform` | Set `tf_version` to the version that manages your state. |

## [v1.0.0] - 2025-02-13

### Added
- First set of templates: `sonar`, `build-java`, `build-dotnet`, `build-go`, `build-node`, `terraform`,
  `docker-build`, `trivy-scan`, `ecs-deploy`, `slack-team-notifica`, `release-drafter`.
