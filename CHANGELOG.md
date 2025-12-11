# 📦 CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on **Semantic Versioning (https://semver.org/)**  
and this changelog adheres to **Keep a Changelog (https://keepachangelog.com/en/1.0.0/)**.

---

# 🚀 v1.0.0 — Initial Release  
**Release Date:** 2025-02-13

### Added  
- Introduced fully modular CI/CD template architecture.  
- Added SonarQube scanning workflow template (`sonar.yml`).  
- Added Java Maven build workflow template (`build-java.yml`).  
- Added .NET build workflow template (`build-dotnet.yml`).  
- Added Go build workflow template (`build-go.yml`).  
- Added Node.js build workflow template (`build-node.yml`).  
- Added Terraform automation workflow (`terraform.yml`).  
- Added Docker build & ECR push workflow (`docker-build.yml`).  
- Added Trivy image scanning workflow (`trivy-scan.yml`).  
- Added manual approval workflow (`approval.yml`).  
- Added EKS deployments via Helm (`deploy-eks-helm.yml`).  
- Added EKS deployments via ArgoCD GitOps (`deploy-eks-argocd.yml`).  
- Added full README documentation with inputs, secrets, examples.

---

# 🔄 Unreleased  
(This section will automatically grow as new changes are added.)

### Added  
- _Place new "added" items here._

### Changed  
- _Place improvements or modifications here._

### Deprecated  
- _Place deprecated features here._

### Removed  
- _Place removed content here._

### Fixed  
- _Place bug fixes here._

### Security  
- _Place security-related changes here._

---

# 🛠 Automation Note  
To automate changelog updates in CI/CD:

1. Add a GitHub Action that appends entries to the **Unreleased** section.  
2. On creating a new tag (e.g., `v1.1.0`), the pipeline should:
   - Move the Unreleased section into a new `## vX.Y.Z` heading.
   - Clear the Unreleased section for future changes.

A template for automation can be added on request.

