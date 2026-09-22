# Build · Java (Maven / Gradle)

Compiles, tests and packages a Java project. It uses `./mvnw` or `./gradlew` when the project has one,
and uploads the Surefire/JUnit and JaCoCo reports on every run, including failed ones.

## Usage: Maven

```yaml
jobs:
  build:
    permissions:
      contents: read
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/build-java.yml@v2
    with:
      java_version: "21"
      artifact_path: target/*.jar
```

## Usage: Gradle

```yaml
jobs:
  build:
    permissions:
      contents: read
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/build-java.yml@v2
    with:
      build_tool: gradle
      java_version: "21"
      build_args: build jacocoTestReport
      artifact_path: build/libs/*.jar
```

## Private Maven repository (Nexus / Artifactory / CodeArtifact)

```yaml
    with:
      maven_server_id: internal-nexus   # must match <repository><id> in your pom.xml
    secrets:
      maven_username: ${{ secrets.NEXUS_USER }}
      maven_password: ${{ secrets.NEXUS_PASSWORD }}
```

## Notes

- `run_tests: false` passes `-DskipTests=true` to Maven or `-x test` to Gradle. It is meant for fast packaging builds, not the main CI path.
- For SonarQube on Java, upload `target/` (`artifact_path: target/`). Then pass it to [sonar](sonar.md) with `-Dsonar.java.binaries=target/classes`.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`build-java.yml`](../../.github/workflows/build-java.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `java_version` | string | no | `21` | JDK version. |
| `java_distribution` | string | no | `temurin` | JDK distribution (temurin, corretto, zulu, microsoft, ...). |
| `build_tool` | string | no | `maven` | maven \| gradle |
| `working_directory` | string | no | `.` | Directory containing pom.xml or build.gradle(.kts). |
| `run_tests` | boolean | no | `true` | Run unit tests. |
| `build_args` | string | no |  | Arguments passed to the build tool. Defaults to 'clean verify' (Maven) or 'build' (Gradle). |
| `maven_server_id` | string | no |  | settings.xml <server> id for a private Maven repository (used with maven_username / maven_password). |
| `artifact_path` | string | no |  | Glob of packages to upload, relative to working_directory (e.g. target/*.jar). Leave empty to skip. |
| `artifact_name` | string | no | `java-build` | Base name for uploaded artifacts (test reports / coverage get a suffix). |
| `retention_days` | number | no | `7` | Artifact retention in days. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |
| `timeout_minutes` | number | no | `45` | Job timeout in minutes. |

### Secrets

| Name | Required | Description |
|---|---|---|
| `maven_username` | no | Username for the private Maven repository (maven_server_id). |
| `maven_password` | no | Password / token for the private Maven repository (maven_server_id). |

### Outputs

| Name | Description |
|---|---|
| `artifact_name` | Base name for uploaded artifacts (test reports / coverage get a suffix). |

<!-- END GENERATED REFERENCE -->
