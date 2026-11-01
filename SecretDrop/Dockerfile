FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

# Install dependencies and update packages
RUN python -m pip install --upgrade --no-cache-dir pip && \
    python -m pip install --no-cache-dir -r requirements.txt && \
    python -m pip install --upgrade --no-cache-dir "setuptools>=78.1.1" "urllib3>=2.8.0" "msgpack>=1.2.3"

# Delete stale Debian system package directories that trigger Trivy
RUN rm -rf /usr/lib/python3/dist-packages/setuptools* \
           /usr/lib/python3/dist-packages/urllib3* \
           /usr/lib/python3/dist-packages/msgpack*

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]