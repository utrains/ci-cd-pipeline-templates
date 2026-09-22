# Build · .NET

Restores, builds and tests a .NET solution or project. It collects test results (TRX) and coverage,
and can optionally `dotnet publish` the result and upload it.

## Usage

```yaml
jobs:
  build:
    permissions:
      contents: read
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/build-dotnet.yml@v2
    with:
      dotnet_version: "8.0.x"
      project_path: ./src/MyApp.sln
      publish: true
      artifact_name: myapp-publish
```

## Notes

- Set `global_json_file: global.json` to take the SDK version from the repo.
- For a private NuGet feed, set `nuget_source` and pass `secrets: nuget_token`.
- Coverage is written in Cobertura format to `test-results/**/coverage.cobertura.xml` and uploaded as `<artifact_name>-test-results`.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`build-dotnet.yml`](../../.github/workflows/build-dotnet.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `dotnet_version` | string | no | `10.0.x` | .NET SDK version (e.g. 8.0.x, 10.0.x). Ignored when global_json_file is set. |
| `global_json_file` | string | no |  | Path to global.json to read the SDK version from. |
| `project_path` | string | no | `.` | Solution or project file / directory. |
| `configuration` | string | no | `Release` | Build configuration (Release / Debug). |
| `run_tests` | boolean | no | `true` | Run `dotnet test` with coverage collection. |
| `publish` | boolean | no | `false` | Run `dotnet publish` and upload the output as an artifact. |
| `nuget_source` | string | no |  | Private NuGet feed URL (used with the nuget_token secret). |
| `artifact_name` | string | no | `dotnet-build` | Base name for uploaded artifacts (test reports / coverage get a suffix). |
| `retention_days` | number | no | `7` | Artifact retention in days. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |
| `timeout_minutes` | number | no | `30` | Job timeout in minutes. |

### Secrets

| Name | Required | Description |
|---|---|---|
| `nuget_token` | no | Auth token for the private NuGet feed (nuget_source). |

### Outputs

| Name | Description |
|---|---|
| `artifact_name` | Base name for uploaded artifacts (test reports / coverage get a suffix). |

<!-- END GENERATED REFERENCE -->
