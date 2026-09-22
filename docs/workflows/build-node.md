# Build · Node.js

Installs dependencies, then runs lint, tests and the build of a Node.js project. It caches
dependencies for npm, yarn or pnpm, and uploads the build output and coverage as artifacts.

## Minimal usage

```yaml
jobs:
  build:
    permissions:
      contents: read
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/build-node.yml@v2
```

## Typical usage

```yaml
jobs:
  build:
    permissions:
      contents: read
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/build-node.yml@v2
    with:
      node_version_file: .nvmrc
      package_manager: pnpm
      install_cmd: pnpm install --frozen-lockfile
      lint_cmd: pnpm lint
      test_cmd: pnpm test -- --coverage
      build_cmd: pnpm build
      artifact_path: dist/
      artifact_name: web-dist        # downstream jobs: actions/download-artifact name=web-dist
```

## Notes

- `npm ci` is the default install command. It needs a committed `package-lock.json`, which keeps builds reproducible.
- For a private registry, set `registry_url` and pass `secrets: npm_token: ${{ secrets.NPM_TOKEN }}`.
- For a monorepo package, set `working_directory: packages/api`. All paths, including artifacts, are relative to it.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`build-node.yml`](../../.github/workflows/build-node.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `node_version` | string | no | `24` | Node.js version. Ignored when node_version_file is set. |
| `node_version_file` | string | no |  | File to read the Node.js version from (e.g. .nvmrc, package.json). |
| `package_manager` | string | no | `npm` | Package manager used for dependency caching: npm \| yarn \| pnpm. |
| `working_directory` | string | no | `.` | Directory containing package.json. |
| `registry_url` | string | no |  | Private npm registry URL (used with the npm_token secret). |
| `install_cmd` | string | no | `npm ci` | Command that installs dependencies. |
| `lint_cmd` | string | no |  | Lint command. Leave empty to skip. |
| `test_cmd` | string | no | `npm test --if-present` | Test command. Leave empty to skip. |
| `build_cmd` | string | no | `npm run build --if-present` | Build command. Leave empty to skip. |
| `artifact_path` | string | no |  | Build output to upload (e.g. dist/). Leave empty to skip the upload. |
| `artifact_name` | string | no | `node-build` | Name of the uploaded build artifact. |
| `coverage_path` | string | no | `coverage` | Coverage report directory, uploaded as the "<artifact_name>-coverage" artifact when present. |
| `retention_days` | number | no | `7` | Artifact retention in days. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels (e.g. '["self-hosted","linux"]'). |
| `timeout_minutes` | number | no | `30` | Job timeout in minutes. |

### Secrets

| Name | Required | Description |
|---|---|---|
| `npm_token` | no | Auth token for a private npm registry. |

### Outputs

| Name | Description |
|---|---|
| `artifact_name` | Name of the uploaded build artifact (empty when nothing was uploaded). |

<!-- END GENERATED REFERENCE -->
