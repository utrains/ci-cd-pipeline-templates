# Build · Go

Verifies modules, then runs `go vet`, **golangci-lint**, tests with the race detector and coverage, and the build.

## Usage

```yaml
jobs:
  build:
    permissions:
      contents: read
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/build-go.yml@v2
```

The Go version is read from `go.mod` by default. To force one, set `go_version: "1.25"`.

## Building binaries

```yaml
    with:
      build_cmd: CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o bin/ ./cmd/...
      artifact_path: bin/
      artifact_name: service-binaries
```

## Notes

- golangci-lint reads `.golangci.yml` from the repo when present. Set `run_lint: false` to skip it.
- `coverage.out` is uploaded as `<artifact_name>-coverage`. Pass it to Sonar with `-Dsonar.go.coverage.reportPaths=coverage.out`.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`build-go.yml`](../../.github/workflows/build-go.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `go_version` | string | no |  | Go version. When empty, the version is read from go_version_file. |
| `go_version_file` | string | no | `go.mod` | File to read the Go version from, relative to working_directory. |
| `working_directory` | string | no | `.` | Directory containing go.mod. |
| `run_lint` | boolean | no | `true` | Run golangci-lint. |
| `golangci_lint_version` | string | no | `v2.13.2` | golangci-lint version. |
| `race` | boolean | no | `true` | Run tests with the race detector. |
| `build_cmd` | string | no | `go build -trimpath ./...` | Build command. |
| `artifact_path` | string | no |  | Build output to upload (e.g. bin/). Leave empty to skip. |
| `artifact_name` | string | no | `go-build` | Base name for uploaded artifacts (test reports / coverage get a suffix). |
| `retention_days` | number | no | `7` | Artifact retention in days. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |
| `timeout_minutes` | number | no | `30` | Job timeout in minutes. |

### Outputs

| Name | Description |
|---|---|
| `artifact_name` | Base name for uploaded artifacts (test reports / coverage get a suffix). |

<!-- END GENERATED REFERENCE -->
