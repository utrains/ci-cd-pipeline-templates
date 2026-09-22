# Scan · CodeQL (SAST)

GitHub's semantic code analysis. Findings go to the repository's **Security → Code scanning** tab and
are shown as annotations on pull requests.

## Usage: interpreted languages

```yaml
jobs:
  codeql:
    permissions:
      contents: read
      actions: read
      security-events: write
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/codeql.yml@v2
    with:
      languages: '["javascript-typescript","python","actions"]'
```

## Usage: compiled Java with a manual build

```yaml
    with:
      languages: '["java-kotlin"]'
      build_mode: manual
      java_version: "21"
      build_cmd: ./mvnw -B -ntp -DskipTests package
```

## Notes

- Private repositories need **GitHub Advanced Security / Code Security**.
- `build_mode: none` works for Java and C# in most projects and is much faster than a full build.
- Add a `.github/codeql/codeql-config.yml` and pass `config_file` to exclude paths or add query packs.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`codeql.yml`](../../.github/workflows/codeql.yml)

### Permissions the calling job must grant

```yaml
permissions:
  actions: read
  contents: read
  security-events: write
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `languages` | string | no | `["javascript-typescript"]` | JSON array of CodeQL languages, e.g. ["javascript-typescript","python"]. Valid: actions, c-cpp, csharp, go, java-kotlin, javascript-typescript, python, ruby, rust, swift. |
| `build_mode` | string | no | `none` | none \| autobuild \| manual. Compiled languages usually need autobuild or manual. |
| `build_cmd` | string | no |  | Build command when build_mode is manual. |
| `queries` | string | no | `security-extended` | Query suite: security-extended \| security-and-quality \| (empty = default). |
| `config_file` | string | no |  | Path to a CodeQL config file in the calling repository. |
| `java_version` | string | no |  | Install this JDK before analysis (compiled Java/Kotlin). Empty = runner default. |
| `dotnet_version` | string | no |  | Install this .NET SDK before analysis. Empty = runner default. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |
| `timeout_minutes` | number | no | `60` | Job timeout in minutes. |

<!-- END GENERATED REFERENCE -->
