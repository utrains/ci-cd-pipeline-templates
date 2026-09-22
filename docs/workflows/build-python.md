# Build · Python

Installs, lints, tests (pytest by default) and optionally builds a wheel/sdist, with **pip**, **poetry**
or **uv**.

## Usage: uv

```yaml
jobs:
  build:
    permissions:
      contents: read
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/build-python.yml@v2
    with:
      package_manager: uv
      python_version: "3.13"
      lint_cmd: ruff check .
      test_cmd: pytest --junitxml=test-results/junit.xml --cov --cov-report=xml
```

## Usage: pip with requirements files

```yaml
    with:
      package_manager: pip   # installs requirements.txt, requirements-dev.txt, then `pip install -e .` if pyproject.toml exists
```

## Notes

- Lint and test commands run inside the project environment, as `uv run …` or `poetry run …`, so tools only need to be dev dependencies.
- `coverage.xml` and `test-results/` are uploaded as `<artifact_name>-test-results` for Sonar (`-Dsonar.python.coverage.reportPaths=coverage.xml`).
- `build_package: true` uploads `dist/`. You can publish it with a PyPI trusted-publishing job.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`build-python.yml`](../../.github/workflows/build-python.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `python_version` | string | no | `3.13` | Python version. |
| `package_manager` | string | no | `pip` | pip \| poetry \| uv |
| `working_directory` | string | no | `.` | Directory containing pyproject.toml / requirements.txt. |
| `install_cmd` | string | no |  | Override the install command. Empty = sensible default for the package manager. |
| `lint_cmd` | string | no |  | Lint command, run inside the project environment (e.g. "ruff check ."). Leave empty to skip. |
| `test_cmd` | string | no | `pytest --junitxml=test-results/junit.xml` | Test command, run inside the project environment. Leave empty to skip. |
| `build_package` | boolean | no | `false` | Build sdist/wheel and upload them as an artifact. |
| `artifact_name` | string | no | `python-build` | Base name for uploaded artifacts (test reports / coverage get a suffix). |
| `retention_days` | number | no | `7` | Artifact retention in days. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |
| `timeout_minutes` | number | no | `30` | Job timeout in minutes. |

### Outputs

| Name | Description |
|---|---|
| `artifact_name` | Base name for uploaded artifacts (test reports / coverage get a suffix). |

<!-- END GENERATED REFERENCE -->
