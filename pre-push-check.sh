
#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PROJECT="$ROOT/SecretDrop"
cd "$PROJECT"

echo "=== 1. Python syntax ==="
python -m compileall -q app run.py

echo "=== 2. Dependency consistency ==="
pip check

echo "=== 3. Unit tests ==="
python -m pytest -v

echo "=== 4. Bandit security scan ==="
bandit -r app/ -ll -iii

echo "=== 5. Flask startup ==="
python -c "from run import create_app; app = create_app({'TESTING': True}); print('Flask application initialized successfully')"

echo "=== 6. Git security review ==="
cd "$ROOT"

echo "=== 7. Dependency vulnerability audit ==="
pip-audit -r SecretDrop/requirements.txt

echo "=== 8. Pre-commit checks ==="
cd "$ROOT"
pre-commit run --all-files

echo "=== 9. YAML validation ==="
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"

echo "--- Git status ---"
git status --short

echo "--- Potentially sensitive tracked files ---"
git ls-files | grep -E '(^|/)(\.env($|\.)|.*\.(pem|key)|uploads/)' || true

echo "Review Git status before committing."
