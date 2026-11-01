# DevSecOps Project — Secure CI/CD Pipeline (SecretDrop)

## 1. Project Overview
This project improves CI/CD pipeline security for the **SecretDrop** application by integrating automated security checks throughout the software development lifecycle. The goal is to detect vulnerabilities early, prevent security issues from reaching production, and enforce DevSecOps best practices.

### Objectives
* Implement automated security checks in a CI/CD pipeline.
* Detect vulnerabilities in source code and dependencies.
* Identify exposed secrets in git history and commits.
* Scan Docker images for vulnerabilities.
* Test the running application dynamically for security issues.
* Configure strict security quality gates to block unsafe builds.

---

## 2. Technologies and Tools
* **GitHub Actions:** CI/CD automation pipeline.
* **Bandit:** Static Application Security Testing (SAST) for Python.
* **Gitleaks:** Automated secret detection.
* **Trivy:** Filesystem (SCA) and Docker image security scanning.
* **OWASP ZAP:** Baseline Dynamic Application Security Testing (DAST).
* **Docker & pytest:** Containerization and automated unit testing.
* **Pre-commit:** Local developer security checks.

---

## 3. Project Workflow
1. Developers push code or open a Pull Request on GitHub.
2. GitHub Actions checks out code with full history (`fetch-depth: 0`).
3. Automated unit tests (`pytest`) run and Python dependencies install.
4. **SAST (Bandit)** scans source code; **Gitleaks** scans for exposed secrets.
5. **Trivy (FS)** scans filesystem and `requirements.txt` dependencies.
6. **Docker** builds the application image (`secretdrop:latest`).
7. **Trivy (Image)** scans the container for OS/library vulnerabilities.
8. The application container starts on port `5000`.
9. **OWASP ZAP** executes a baseline DAST scan against `http://127.0.0.1:5000`.
10. Scan reports are archived as build artifacts.

---

## 4. Team Responsibilities
* **Person A — CI/CD:** GitHub Actions workflow design, build automation, scanner integration, quality gate enforcement, and branch protection.
* **Person B — Security & Application:** Application setup, local security tooling (pre-commit, Trivy, ZAP), test case validation, and report collation.

---

## 5. Security Policy & Quality Gates
The pipeline enforces strict automated gates:
* **Secrets:** Zero tolerance; any detected API keys or credentials fail the build.
* **SAST (Bandit):** Blocks on High severity / High confidence findings (`-ll -iii`).
* **SCA & Image (Trivy):** Blocks on `HIGH` and `CRITICAL` vulnerabilities.
* **False-Positive Handling:** Exemption rules are strictly tracked in `.trivyignore` (e.g., bypassing non-exploitable internal `pip` vendor metadata).

