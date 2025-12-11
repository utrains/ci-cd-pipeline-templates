# 📘 Utrains CI/CD Reusable Pipeline Templates

Welcome to the **Utrains CI/CD Template Repository**.

This repository contains **enterprise-ready reusable GitHub Action workflows** that can be called from any application repository.  
These templates encapsulate **build, scan, deploy, approval, and DevOps automation logic**, ensuring:

- Standardization across all applications  
- Reduced code duplication  
- Faster onboarding for new developers  
- Cleaner, safer CI/CD pipelines  

All templates are stored under:

```
.github/workflows/
```

You can call any template from *another* repo using:

```yaml
uses: Utrains/pipeline-templates/.github/workflows/<template>.yml@v1
```

---

# 📚 Template Overview

| Template | Purpose |
|---------|---------|
| `sonar.yml` | Run SonarQube code scan & quality gate checks |
| `build-java.yml` | Build & test Java/Maven applications |
| `build-dotnet.yml` | Build & test .NET Core applications |
| `build-go.yml` | Build & test Go applications |
| `build-node.yml` | Build Node.js applications |
| `terraform.yml` | Run Terraform init/validate/plan (supports OIDC) |
| `docker-build.yml` | Build & push Docker image to ECR |
| `trivy-scan.yml` | Perform Trivy image scan |
| `approval.yml` | Manual approval stage using GitHub Environments |
| `deploy-eks-helm.yml` | Deploy workloads to EKS using Helm |
| `deploy-eks-argocd.yml` | Deploy workloads to EKS using ArgoCD |

---

# 🧩 How to Use These Templates From Your Application Repo

Create a workflow in your app repo:

```
.github/workflows/main.yml
```

Call any template like:

```yaml
jobs:
  sonar:
    uses: Utrains/pipeline-templates/.github/workflows/sonar.yml@v1
    with:
      sonar_host: "https://sonar.example.com"
      project_name: "my-app"
      project_key: "my-app-key"
    secrets:
      sonar_token: ${{ secrets.SONAR_TOKEN }}
```

---

# 🟦 1. SonarQube Scan Template

**File:** `.github/workflows/sonar.yml`  
**Purpose:** Runs a full SonarQube scan with optional quality gate enforcement.

### Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `sonar_host` | Yes | Sonar server URL |
| `project_name` | Yes | Sonar project name |
| `project_key` | Yes | Sonar project key |
| `quality_gate` | No | Enable quality gate check |

### Secrets

| Secret | Description |
|--------|-------------|
| `sonar_token` | Sonar authentication token |

### Example

```yaml
jobs:
  sonar:
    uses: Utrains/pipeline-templates/.github/workflows/sonar.yml@v1
    with:
      sonar_host: "https://sonar.mycompany.com"
      project_name: "backend"
      project_key: "backend"
      quality_gate: true
    secrets:
      sonar_token: ${{ secrets.SONAR_TOKEN }}
```

---

# 🟦 2. Java Maven Build Template

**File:** `.github/workflows/build-java.yml`

### Inputs

| Input | Default | Description |
|-------|---------|-------------|
| `java_version` | `17` | JDK version |
| `run_tests` | `true` | Run unit tests |

### Example

```yaml
jobs:
  build_java:
    uses: Utrains/pipeline-templates/.github/workflows/build-java.yml@v1
    with:
      java_version: "21"
      run_tests: true
```

---

# 🟦 3. .NET Build Template

**File:** `.github/workflows/build-dotnet.yml`

### Inputs

| Input | Default | Description |
|--------|---------|-------------|
| `dotnet_version` | `8.0` | .NET SDK version |
| `project_path` | `./` | Path to the .NET solution |

### Example

```yaml
jobs:
  build_dotnet:
    uses: Utrains-pipeline-templates/.github/workflows/build-dotnet.yml@v1
    with:
      dotnet_version: "8.0"
      project_path: "./src/MyApp"
```

---

# 🟦 4. Go Build Template

**File:** `.github/workflows/build-go.yml`

### Inputs

| Input | Default | Description |
|--------|---------|-------------|
| `go_version` | `1.22` | Go version |

### Example

```yaml
jobs:
  build_go:
    uses: Utrains-pipeline-templates/.github/workflows/build-go.yml@v1
    with:
      go_version: "1.22"
```

---

# 🟦 5. Node.js Build Template

**File:** `.github/workflows/build-node.yml`

### Inputs

| Input | Default | Description |
|--------|---------|-------------|
| `node_version` | `20` | Node.js version |
| `install_cmd` | `npm install` | Install command |
| `build_cmd` | `npm run build` | Build command |

### Example

```yaml
jobs:
  build_node:
    uses: Utrains-pipeline-templates/.github/workflows/build-node.yml@v1
    with:
      node_version: "20"
```

---

# 🟦 6. Terraform Template

**File:** `.github/workflows/terraform.yml`

### Inputs

| Input | Default | Description |
|--------|---------|-------------|
| `tf_version` | `1.9.5` | Terraform version |
| `working_directory` | `./` | Terraform root directory |

### Secrets

| Secret | Description |
|--------|-------------|
| `aws_role_to_assume` | IAM role for OIDC auth |

### Example

```yaml
jobs:
  terraform:
    uses: Utrains-pipeline-templates/.github/workflows/terraform.yml@v1
    with:
      working_directory: "infra/"
    secrets:
      aws_role_to_assume: ${{ secrets.IAM_ROLE }}
```

---

# 🟦 7. Docker Build & Push Template

**File:** `.github/workflows/docker-build.yml`

### Inputs

| Input | Required | Description |
|--------|---------|-------------|
| `image_name` | Yes | ECR image URI |
| `dockerfile` | No | Dockerfile path |
| `context` | No | Build context |

### Secrets

| Secret | Description |
|--------|-------------|
| `aws_role` | IAM role for ECR push |

### Example

```yaml
jobs:
  docker:
    uses: Utrains-pipeline-templates/.github/workflows/docker-build.yml@v1
    with:
      image_name: "123456789012.dkr.ecr.us-east-1.amazonaws.com/app:latest"
    secrets:
      aws_role: ${{ secrets.AWS_ROLE }}
```

---

# 🟦 8. Trivy Image Scan Template

**File:** `.github/workflows/trivy-scan.yml`

### Inputs

| Input | Required | Description |
|--------|----------|-------------|
| `image` | Yes | Docker image to scan |

### Example

```yaml
jobs:
  trivy:
    uses: Utrains-pipeline-templates/.github/workflows/trivy-scan.yml@v1
    with:
      image: "123456789012.dkr.ecr.us-east-1.amazonaws.com/app:latest"
```

---

# 🟦 9. Approval Workflow Template

**File:** `.github/workflows/approval.yml`

### Inputs

| Input | Required | Description |
|--------|----------|-------------|
| `environment` | Yes | GitHub environment name |
| `message` | No | Approval message |

### Example

```yaml
jobs:
  approve:
    uses: Utrains-pipeline-templates/.github/workflows/approval.yml@v1
    with:
      environment: "prod"
      message: "Prod deployment approval required."
```

---

# 🟦 10. EKS Helm Deployment Template

**File:** `.github/workflows/deploy-eks-helm.yml`

### Inputs

| Input | Required | Description |
|--------|---------|-------------|
| `cluster_name` | Yes | EKS cluster name |
| `region` | Yes | AWS region |
| `namespace` | Yes | Kubernetes namespace |
| `release_name` | Yes | Helm release name |
| `chart_path` | Yes | Helm chart location |
| `chart_version` | No | Chart version |
| `values_file` | No | Values file |

### Secrets

| Secret | Description |
|--------|-------------|
| `aws_role` | IAM role for EKS access |

### Example

```yaml
jobs:
  deploy:
    uses: Utrains-pipeline-templates/.github/workflows/deploy-eks-helm.yml@v1
    with:
      cluster_name: "prod-eks"
      region: "us-east-1"
      namespace: "app"
      release_name: "app-release"
      chart_path: "./chart"
      values_file: "./chart/values-prod.yaml"
    secrets:
      aws_role: ${{ secrets.AWS_ROLE }}
```

---

# 🟦 11. EKS ArgoCD Deployment Template

**File:** `.github/workflows/deploy-eks-argocd.yml`

### Inputs

| Input | Required | Description |
|--------|---------|-------------|
| `cluster_name` | Yes | EKS cluster name |
| `region` | Yes | AWS region |
| `argocd_server` | Yes | ArgoCD API |
| `argocd_app` | Yes | ArgoCD Application name |
| `repo_url` | Yes | GitOps repo URL |
| `path` | Yes | Path to manifests |
| `revision` | No | Git branch |
| `dest_namespace` | Yes | Kubernetes namespace |
| `dest_server` | Yes | Cluster API endpoint |

### Secrets

| Secret | Description |
|--------|-------------|
| `aws_role` | IAM role for cluster access |
| `argocd_token` | ArgoCD auth token |

### Example

```yaml
jobs:
  deploy_argocd:
    uses: Utrains-pipeline-templates/.github/workflows/deploy-eks-argocd.yml@v1
    with:
      cluster_name: "prod"
      region: "us-east-1"
      argocd_server: "argocd.example.com"
      argocd_app: "myapp-prod"
      repo_url: "https://github.com/org/app-config.git"
      path: "environments/prod"
      dest_namespace: "app"
      dest_server: "https://kubernetes.default.svc"
    secrets:
      aws_role: ${{ secrets.AWS_PROD_ROLE }}
      argocd_token: ${{ secrets.ARGOCD_TOKEN }}
```

---

# 🎉 End of Documentation
