# SecretDrop — Secure CI/CD Pipeline

A DevSecOps CI/CD pipeline built with GitHub Actions for the **SecretDrop** Flask application. This pipeline automatically enforces static code analysis, secret detection, dependency scanning, container vulnerability management, and dynamic application security testing (DAST) on every push and pull request.

---

## Pipeline Architecture

         [ Code Commit ] ➔ [ SAST & Secrets ] ➔ [ SCA Scan ] ➔ [ Docker Build ] ➔ [ Container Scan ] ➔ [ DAST (ZAP) ] ➔ [ Deploy ]

---

## Security Stages & Quality Gates

The pipeline runs sequentially inside `.github/workflows/ci.yml` and enforces strict quality gates before allowing code to merge:

| Stage | Security Tool | Scan Target | Gate Policy / Threshold |
| :--- | :--- | :--- | :--- |
| **1. Unit Testing** | `pytest` | Test suite | All test cases must pass. |
| **2. SAST** | **Bandit** | Python source (`app/`) | Fails build on High severity & High confidence findings (`-ll -iii`). |
| **3. Secret Scanning** | **Gitleaks** | Repository git history | Zero tolerance; fails on any committed API keys, tokens, or credentials. Requires `fetch-depth: 0`. |
| **4. SCA (Dependencies)** | **Trivy FS** | `requirements.txt` / Filesystem | Fails on `HIGH` or `CRITICAL` vulnerability severity. |
| **5. Container Security** | **Trivy Image** | Docker Image (`secretdrop:latest`) | Fails on `HIGH` or `CRITICAL` container OS or library vulnerabilities. Exemption exceptions defined in `.trivyignore`. |
| **6. DAST** | **OWASP ZAP** | Running App (`http://127.0.0.1:5000`) | Baseline dynamic web scan; generates HTML, JSON, and Markdown vulnerability reports. |

---

## Pipeline Execution Flow

1. **Checkout & Setup:** Code is checked out with full git history (`fetch-depth: 0`) and Python environment is initialized.
2. **Test & Static Security:** Unit tests (`pytest`), Bandit SAST analysis, and Gitleaks secret detection execute concurrently.
3. **Dependency Scanning:** Trivy scans project dependencies for known CVEs.
4. **Container Build & Scan:** The Flask web application is built into a local Docker image (`secretdrop:latest`) and scanned by Trivy Image scanner.
5. **Dynamic Security Scan:** The Docker container is launched on `0.0.0.0:5000`. OWASP ZAP runs an active baseline scan against the application endpoint.
6. **Artifact Archiving:** ZAP security scan reports (`report_html.html`, `report_json.json`, `report_md.md`) are saved as GitHub Actions build artifacts.

---

## Security Policy & False-Positive Management

* **Zero-Trust Secret Rule:** Unencrypted credentials or keys are strictly prohibited in code.
* **Vulnerability Exceptions:** Non-exploitable vulnerabilities or false positives (e.g., internal `pip` vendor dependencies) are documented and exempted using `.trivyignore` at the repository root.

---

## Local Development & Testing

To run application tests and container builds locally before pushing:

```bash
# Install dependencies & run unit tests
pip install -r requirements.txt
pytest

# Build local Docker image
docker build -t secretdrop:latest .

# Run application container locally
docker run -d -p 5000:5000 --name secretdrop-app secretdrop:latest
