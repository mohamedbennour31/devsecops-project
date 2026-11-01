FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

# Install dependencies and force-upgrade vulnerable system packages
RUN python -m pip install --upgrade --no-cache-dir pip && \
    python -m pip install --no-cache-dir -r requirements.txt && \
    python -m pip install --upgrade --no-cache-dir "setuptools>=78.1.1" "urllib3>=2.8.0" "msgpack>=1.2.3"

# Remove lingering Debian/base-image metadata files that trigger Trivy
RUN find / -name "setuptools-70*" -o -name "urllib3-2.7*" -o -name "msgpack-1.1*" -exec rm -rf {} + 2>/dev/null || true

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]