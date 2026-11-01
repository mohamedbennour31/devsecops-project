FROM python:3.13-slim

WORKDIR /app

# Remove stale Debian distribution package metadata before installing upgraded wheels
RUN rm -rf /usr/lib/python3/dist-packages/setuptools* \
           /usr/lib/python3/dist-packages/urllib3* \
           /usr/lib/python3/dist-packages/msgpack*

COPY requirements.txt .
RUN python -m pip install --upgrade --no-cache-dir pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]