# Scan · SonarQube

Runs a SonarQube Server or SonarCloud analysis and, by default, **waits for the quality gate and
fails the job when it is red**.

## Usage

```yaml
jobs:
  sonar:
    needs: build                       # so coverage artifacts exist
    permissions:
      contents: read
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/sonar.yml@v2
    with:
      sonar_host: https://sonar.mycompany.com
      project_key: payments-api
      project_name: Payments API
      coverage_artifact: node-build-coverage     # artifact uploaded by build-node.yml
      extra_args: -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info
    secrets:
      sonar_token: ${{ secrets.SONAR_TOKEN }}
```

## SonarCloud

```yaml
    with:
      sonar_host: https://sonarcloud.io
      organization: my-org
```

## Notes

- A `sonar-project.properties` file in the repo is still honoured. Inputs here override it.
- Project key and name are passed as JSON (`SONAR_SCANNER_JSON_PARAMS`), so names with spaces are safe.
- Full git history is fetched, so new-code detection and blame work.
- For Java, the scanner needs compiled classes. See [build-java](build-java.md#notes).
- Use a **project analysis token** stored as an org secret, not a user token.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`sonar.yml`](../../.github/workflows/sonar.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `sonar_host` | string | yes |  | SonarQube server URL (https://sonarcloud.io for SonarCloud). |
| `project_key` | string | yes |  | Sonar project key. |
| `project_name` | string | yes |  | Sonar project display name. |
| `organization` | string | no |  | SonarCloud organization key. Leave empty for SonarQube Server. |
| `quality_gate` | boolean | no | `true` | Wait for the quality gate result and fail the job if it is not green. |
| `quality_gate_timeout` | number | no | `300` | Seconds to wait for the quality gate. |
| `working_directory` | string | no | `.` | Project base directory for the scanner. |
| `extra_args` | string | no |  | Extra scanner arguments, e.g. "-Dsonar.sources=src -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info". |
| `coverage_artifact` | string | no |  | Name of an artifact (e.g. produced by a build workflow) to download into working_directory before scanning. |
| `coverage_artifact_path` | string | no | `coverage` | Where to extract coverage_artifact, relative to working_directory. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |
| `timeout_minutes` | number | no | `30` | Job timeout in minutes. |

### Secrets

| Name | Required | Description |
|---|---|---|
| `sonar_token` | yes | Sonar analysis token. |

<!-- END GENERATED REFERENCE -->
