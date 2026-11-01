SecretDrop — Secure CI/CD PipelineA DevSecOps CI/CD pipeline built with GitHub Actions for the SecretDrop Flask application. This pipeline automatically enforces static code analysis, secret detection, dependency scanning, container vulnerability management, and dynamic application security testing (DAST) on every push and pull request.
Pipeline Architecture                
                                 ┌───────────────────────────────────────────────────────────────┐
                                 │                   GitHub Actions Pipeline                     │
                                 ├───────────────┬───────────────┬───────────────┬───────────────┤
[ Developer ] --(Push/PR)-->     │   1. SAST     │  2. Secrets   │    3. SCA     │ 4. Container  │
                                 │   (Bandit)    │  (Gitleaks)   │  (Trivy FS)   │    (Trivy)    │
                                 └───────┬───────┴───────┬───────┴───────┬───────┴───────┬───────┘
                                         │               │               │               │
                                         └───────────────┴───────┬───────┴───────────────┘
                                                                 ▼
                                                        [ Docker Build ]
                                                                 │
                                                                 ▼
                                                        [ Start Container ]
                                                                 │
                                                                 ▼
                                                        [ 5. DAST (OWASP ZAP) ]
                                                                 │
                                                                 ▼
                                                        [ Quality Gate Passed ]
Security Stages & Quality GatesThe pipeline runs sequentially inside .github/workflows/ci.yml and enforces strict quality gates before allowing code to merge:StageSecurity ToolScan TargetGate Policy / Threshold1. Unit TestingpytestTest suiteAll test cases must pass.2. SASTBanditPython source (app/)Fails build on High severity & High confidence findings (-ll -iii).3. Secret ScanningGitleaksRepository git historyZero tolerance; fails on any committed API keys, tokens, or credentials. Requires fetch-depth: 0.4. SCA (Dependencies)Trivy FSrequirements.txt / FilesystemFails on HIGH or CRITICAL vulnerability severity.5. Container SecurityTrivy ImageDocker Image (secretdrop:latest)Fails on HIGH or CRITICAL container OS or library vulnerabilities. Exemption exceptions defined in .trivyignore.6. DASTOWASP ZAPRunning App ([http://127.0.0.1:5000](http://127.0.0.1:5000))Baseline dynamic web scan; generates HTML, JSON, and Markdown vulnerability reports.Pipeline Execution FlowCheckout & Setup: Code is checked out with full git history (fetch-depth: 0) and Python environment is initialized.Test & Static Security: Unit tests (pytest), Bandit SAST analysis, and Gitleaks secret detection execute concurrently.Dependency Scanning: Trivy scans project dependencies for known CVEs.Container Build & Scan: The Flask web application is built into a local Docker image (secretdrop:latest) and scanned by Trivy Image scanner.Dynamic Security Scan: The Docker container is launched on 0.0.0.0:5000. OWASP ZAP runs an active baseline scan against the application endpoint.Artifact Archiving: ZAP security scan reports (report_html.html, report_json.json, report_md.md) are saved as GitHub Actions build artifacts.Security Policy & False-Positive ManagementZero-Trust Secret Rule: Unencrypted credentials or keys are strictly prohibited in code.Vulnerability Exceptions: Non-exploitable vulnerabilities or false positives (e.g., internal pip vendor dependencies) are documented and exempted using .trivyignore at the repository root.Local Development & TestingTo run application tests and container builds locally before pushing:Bash# Install dependencies & run unit tests
pip install -r requirements.txt
pytest

# Build local Docker image
docker build -t secretdrop:latest .

# Run application container locally
docker run -d -p 5000:5000 --name secretdrop-app secretdrop:latest
